#!/usr/bin/env python3
"""Generic discounted-cash-flow (DCF) valuation.

For revenue/FCF-positive companies. Reads a JSON assumptions file, discounts
projected free cash flows plus a Gordon-growth terminal value to a present
enterprise value, then backs out equity value and per-share intrinsic value.
Also prints a discount-rate x terminal-growth sensitivity grid.

Assumptions file (see companies/<slug>/valuation/dcf.example.json):
{
  "currency": "CAD",
  "shares_outstanding": 215654785,
  "net_debt": -4360663,          // total_debt - total_cash (negative = net cash)
  "discount_rate": 0.12,         // WACC
  "terminal_growth": 0.025,
  "fcf": [10.0, 12.0, 14.0, 16.0, 18.0]   // projected FCF per year, in millions
}

`fcf` values are in millions of `currency`; net_debt/result are converted
consistently (net_debt is taken in absolute currency units).

Usage:
    python tools/dcf.py companies/<slug>/valuation/dcf.json
"""
import argparse
import json
import sys
from pathlib import Path


def dcf_value(fcf, discount_rate, terminal_growth, net_debt, shares):
    """Return (enterprise_value, equity_value, per_share) in absolute units.

    fcf is a list in millions; result scales to absolute currency units.
    """
    if discount_rate <= terminal_growth:
        raise ValueError("discount_rate must exceed terminal_growth")
    pv_fcf = 0.0
    for i, cf in enumerate(fcf, start=1):
        pv_fcf += cf / (1 + discount_rate) ** i
    # Terminal value at end of final year via Gordon growth, then discounted.
    tv = fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_tv = tv / (1 + discount_rate) ** len(fcf)
    ev_millions = pv_fcf + pv_tv
    ev = ev_millions * 1_000_000
    equity = ev - net_debt
    per_share = equity / shares if shares else float("nan")
    return ev, equity, per_share


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("config", help="path to DCF assumptions JSON")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    required = ["shares_outstanding", "net_debt", "discount_rate",
                "terminal_growth", "fcf"]
    missing = [k for k in required if k not in cfg]
    if missing:
        sys.exit(f"error: config missing keys: {missing}")

    cur = cfg.get("currency", "")
    r = cfg["discount_rate"]
    g = cfg["terminal_growth"]
    shares = cfg["shares_outstanding"]
    net_debt = cfg["net_debt"]
    fcf = cfg["fcf"]

    ev, equity, ps = dcf_value(fcf, r, g, net_debt, shares)
    print(f"DCF valuation ({cur})")
    print(f"  projected FCF (M): {fcf}")
    print(f"  discount rate {r:.1%}, terminal growth {g:.1%}, "
          f"net debt {net_debt:,.0f}, shares {shares:,.0f}")
    print(f"  -> enterprise value: {ev:,.0f}")
    print(f"  -> equity value:     {equity:,.0f}")
    print(f"  -> per share:        {ps:,.2f} {cur}")

    # Sensitivity grid: per-share value across r and g.
    print("\n  Sensitivity — per-share value (rows=discount rate, cols=terminal growth):")
    r_range = [round(r + d, 4) for d in (-0.02, -0.01, 0.0, 0.01, 0.02)]
    g_range = [round(g + d, 4) for d in (-0.01, -0.005, 0.0, 0.005, 0.01)]
    header = "    r\\g  " + "".join(f"{gg:>9.1%}" for gg in g_range)
    print(header)
    for rr in r_range:
        cells = []
        for gg in g_range:
            try:
                _, _, p_s = dcf_value(fcf, rr, gg, net_debt, shares)
                cells.append(f"{p_s:>9.2f}")
            except ValueError:
                cells.append(f"{'n/a':>9}")
        print(f"    {rr:>5.1%}" + "".join(cells))


if __name__ == "__main__":
    main()
