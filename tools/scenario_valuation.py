#!/usr/bin/env python3
"""Scenario-based valuation for early-stage / pre-revenue companies.

When a company has little or no revenue (e.g. a DLE lithium developer like
LibertyStream), DCF and P/E comps don't apply. Instead each scenario models a
**year-by-year production ramp** and discounts the resulting cash flows plus a
terminal exit value back to today:

    for each ramp year y (1..N):
        revenue_y = production_y * price_cad           (price_cad = price_usd * fx)
        ebitda_y  = revenue_y * ebitda_margin
        fcf_y     = ebitda_y - capex_y
        pv_y      = fcf_y / (1 + discount_rate) ** y
    terminal EV = ebitda_N * exit_ev_ebitda  (or revenue_N * exit_ev_revenue)
    pv_terminal = terminal_EV / (1 + discount_rate) ** N
    equity      = sum(pv_y) + pv_terminal - net_debt
    per_share   = equity / shares_at_exit

Scenarios are probability-weighted into an expected value per share.
`fx` makes the CAD/USD assumption explicit; prices may be given in USD
(`price_per_tonne_usd`) or directly in the report currency (`price_per_tonne`).
A per-year `price_per_tonne_usd`/`price_per_tonne` inside a ramp entry overrides
the scenario-level price for that year.

Profitability can be given EITHER as cash opex per tonne (preferred, more
fundamental: `opex_per_tonne_usd` or `opex_per_tonne`, resolvable at config /
scenario / ramp-entry level) so `EBITDA = (price - opex) * tonnes`, OR as a flat
`ebitda_margin` per scenario so `EBITDA = revenue * margin`. opex takes
precedence when both are present. With fixed per-tonne opex, EBITDA margin rises
with price (operating leverage) — which a flat margin misses.

Assumptions file (see companies/<slug>/valuation/scenario.json and
tools/templates/scenario.example.json):
{
  "currency": "CAD",
  "fx": 1.37,                       // report-currency units per USD (CAD/USD)
  "net_debt": -4360663,
  "current_price": 1.06,
  "discount_rate": 0.18,
  "scenarios": [
    {"name": "base", "prob": 0.4,
     "price_per_tonne_usd": 11700, "ebitda_margin": 0.30,
     "exit_ev_ebitda": 8, "shares_at_exit": 340000000,
     "ramp": [
       {"year": 1, "production_tonnes": 1000, "capex": 4000000},
       {"year": 2, "production_tonnes": 2000, "capex": 4000000},
       {"year": 3, "production_tonnes": 4000, "capex": 8000000}
     ]}
  ]
}

ALL scenario inputs are user assumptions — justify them in the company's
valuation write-up, don't treat them as facts.

Usage:
    python tools/scenario_valuation.py companies/<slug>/valuation/scenario.json
"""
import argparse
import json
import sys
from pathlib import Path


def _price_cad(entry, scenario, fx):
    """Resolve a year's price in report currency, honoring per-year overrides."""
    if "price_per_tonne" in entry:
        return entry["price_per_tonne"]
    if "price_per_tonne_usd" in entry:
        return entry["price_per_tonne_usd"] * fx
    if "price_per_tonne" in scenario:
        return scenario["price_per_tonne"]
    if "price_per_tonne_usd" in scenario:
        return scenario["price_per_tonne_usd"] * fx
    raise ValueError(f"scenario '{scenario['name']}': no price_per_tonne[_usd]")


def _opex_cad(entry, scenario, cfg, fx):
    """Resolve a year's cash opex per tonne in report currency, or None.

    Lookup order: ramp entry -> scenario -> config-level default. Prefer this
    (a more fundamental input) over a flat ebitda_margin when present.
    """
    for src in (entry, scenario, cfg):
        if "opex_per_tonne" in src:
            return src["opex_per_tonne"]
        if "opex_per_tonne_usd" in src:
            return src["opex_per_tonne_usd"] * fx
    return None


def value_scenario(s, discount_rate, net_debt, fx, cfg):
    ramp = s["ramp"]
    if not ramp:
        raise ValueError(f"scenario '{s['name']}': empty ramp")
    margin = s.get("ebitda_margin")
    years = [e["year"] for e in ramp]
    n = max(years)

    pv_fcf = 0.0
    rows = []
    final = None
    for e in ramp:
        y = e["year"]
        tonnes = e["production_tonnes"]
        price = _price_cad(e, s, fx)
        revenue = tonnes * price
        opex_pt = _opex_cad(e, s, cfg, fx)
        if opex_pt is not None:
            opex = tonnes * opex_pt
            ebitda = revenue - opex
        elif margin is not None:
            opex = revenue * (1 - margin)
            ebitda = revenue * margin
        else:
            raise ValueError(f"scenario '{s['name']}': need opex_per_tonne[_usd] "
                             f"or ebitda_margin")
        capex = e.get("capex", 0)
        fcf = ebitda - capex
        pv = fcf / (1 + discount_rate) ** y
        pv_fcf += pv
        rows.append({"year": y, "production": tonnes, "revenue": revenue,
                     "opex": opex, "ebitda": ebitda, "capex": capex,
                     "fcf": fcf, "pv": pv})
        if y == n:
            final = {"revenue": revenue, "ebitda": ebitda}

    if "exit_ev_ebitda" in s:
        terminal_ev = final["ebitda"] * s["exit_ev_ebitda"]
    elif "exit_ev_revenue" in s:
        terminal_ev = final["revenue"] * s["exit_ev_revenue"]
    else:
        raise ValueError(f"scenario '{s['name']}': need exit_ev_ebitda or exit_ev_revenue")
    pv_terminal = terminal_ev / (1 + discount_rate) ** n

    equity = pv_fcf + pv_terminal - net_debt
    per_share = equity / s["shares_at_exit"]
    return {"rows": rows, "n": n, "pv_fcf": pv_fcf, "terminal_ev": terminal_ev,
            "pv_terminal": pv_terminal, "equity": equity,
            "per_share": per_share}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("config", help="path to scenario assumptions JSON")
    p.add_argument("--detail", action="store_true",
                   help="print the year-by-year ramp table for each scenario")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    for k in ("discount_rate", "net_debt", "scenarios"):
        if k not in cfg:
            sys.exit(f"error: config missing key: {k}")

    cur = cfg.get("currency", "")
    fx = cfg.get("fx", 1.0)
    r = cfg["discount_rate"]
    net_debt = cfg["net_debt"]
    price = cfg.get("current_price")
    scenarios = cfg["scenarios"]

    total_prob = sum(s.get("prob", 0) for s in scenarios)
    if abs(total_prob - 1.0) > 1e-6:
        print(f"  warning: scenario probabilities sum to {total_prob:.2f}, not 1.0\n")

    print(f"Scenario valuation ({cur}) — discount rate {r:.1%}, "
          f"net debt {net_debt:,.0f}, FX {fx} {cur}/USD")
    print(f"  {'scenario':<8}{'prob':>6}{'yrs':>5}{'endTPA':>8}"
          f"{'PV cf(M)':>10}{'PV term(M)':>11}{'$/sh today':>12}")
    expected = 0.0
    details = []
    for s in scenarios:
        v = value_scenario(s, r, net_debt, fx, cfg)
        expected += s.get("prob", 0) * v["per_share"]
        end_tpa = v["rows"][-1]["production"]
        print(f"  {s['name']:<8}{s.get('prob', 0):>6.0%}{v['n']:>5}{end_tpa:>8.0f}"
              f"{v['pv_fcf']/1e6:>10.1f}{v['pv_terminal']/1e6:>11.1f}"
              f"{v['per_share']:>12.2f}")
        details.append((s, v))

    print(f"\n  probability-weighted value: {expected:,.2f} {cur} / share")
    if price:
        print(f"  current price {price} {cur}: "
              f"{'UPSIDE' if expected > price else 'DOWNSIDE'} "
              f"{(expected/price - 1):+.0%}")

    if args.detail:
        for s, v in details:
            tot_rev = sum(r["revenue"] for r in v["rows"])
            tot_ebitda = sum(r["ebitda"] for r in v["rows"])
            eff_margin = tot_ebitda / tot_rev if tot_rev else 0
            print(f"\n  --- {s['name']} ramp (effective EBITDA margin "
                  f"{eff_margin:.0%}) ---")
            print(f"    {'yr':>3}{'tpa':>8}{'rev(M)':>10}{'opex(M)':>9}"
                  f"{'EBITDA(M)':>11}{'capex(M)':>10}{'FCF(M)':>10}{'PV(M)':>9}")
            for row in v["rows"]:
                print(f"    {row['year']:>3}{row['production']:>8.0f}"
                      f"{row['revenue']/1e6:>10.1f}{row['opex']/1e6:>9.1f}"
                      f"{row['ebitda']/1e6:>11.1f}"
                      f"{row['capex']/1e6:>10.1f}{row['fcf']/1e6:>10.1f}"
                      f"{row['pv']/1e6:>9.1f}")
            print(f"    terminal EV (M): {v['terminal_ev']/1e6:.1f} "
                  f"-> PV {v['pv_terminal']/1e6:.1f}")


if __name__ == "__main__":
    main()
