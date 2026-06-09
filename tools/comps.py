#!/usr/bin/env python3
"""Comparable-company (multiples) valuation.

Fetches valuation multiples for a target and a set of peers via yfinance,
computes the peer median for each multiple, and applies it to the target's
own fundamentals to derive an implied per-share value.

Multiples used: trailing P/E, EV/EBITDA, EV/Revenue, Price/Book.

Usage:
    python tools/comps.py <target_ticker> <peer1,peer2,...> [--out PATH]

Example:
    python tools/comps.py MRLN AAPL,MSFT,GOOG --out companies/merlin/valuation/comps.csv

Notes:
- Multiples are only meaningful where the target has the matching positive
  metric (e.g. P/E needs positive EPS). Pre-revenue / loss-making targets will
  show n/a for most multiples — use scenario_valuation.py for those instead.
- Tickers use yfinance format (TSX Venture = `.V` suffix).
"""
import argparse
import statistics
import sys
from pathlib import Path

MULTIPLES = {
    "trailingPE": ("trailingEps", "P/E"),
    "enterpriseToEbitda": ("ebitda", "EV/EBITDA"),
    "enterpriseToRevenue": ("totalRevenue", "EV/Revenue"),
    "priceToBook": ("bookValue", "P/B"),  # bookValue is per-share
}


def _num(x):
    return x if isinstance(x, (int, float)) and x == x else None  # filters NaN/None


def implied_price(multiple_name, peer_multiple, info):
    """Implied per-share price from a peer multiple applied to the target."""
    shares = _num(info.get("sharesOutstanding"))
    net_debt = (_num(info.get("totalDebt")) or 0) - (_num(info.get("totalCash")) or 0)
    if multiple_name == "trailingPE":
        eps = _num(info.get("trailingEps"))
        return peer_multiple * eps if eps and eps > 0 else None
    if multiple_name == "priceToBook":
        bv = _num(info.get("bookValue"))
        return peer_multiple * bv if bv and bv > 0 else None
    if multiple_name == "enterpriseToEbitda":
        ebitda = _num(info.get("ebitda"))
        if not (ebitda and ebitda > 0 and shares):
            return None
        ev = peer_multiple * ebitda
        return (ev - net_debt) / shares
    if multiple_name == "enterpriseToRevenue":
        rev = _num(info.get("totalRevenue"))
        if not (rev and rev > 0 and shares):
            return None
        ev = peer_multiple * rev
        return (ev - net_debt) / shares
    return None


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target", help="target ticker (yfinance format)")
    p.add_argument("peers", help="comma-separated peer tickers")
    p.add_argument("--out", help="optional CSV output path")
    args = p.parse_args()

    import yfinance as yf
    import pandas as pd

    peers = [s.strip() for s in args.peers.split(",") if s.strip()]
    target_info = yf.Ticker(args.target).info or {}
    cur = target_info.get("currency", "")
    price = target_info.get("currentPrice") or target_info.get("regularMarketPrice")

    # Collect peer multiples.
    peer_mults = {m: [] for m in MULTIPLES}
    skipped = []
    for sym in peers:
        try:
            info = yf.Ticker(sym).info or {}
        except Exception as e:
            skipped.append(f"{sym} ({type(e).__name__})")
            continue
        if not info.get("longName") and not info.get("shortName"):
            skipped.append(f"{sym} (no data)")
            continue
        for m in MULTIPLES:
            v = _num(info.get(m))
            if v is not None and v > 0:
                peer_mults[m].append(v)

    rows = []
    for m, (_, label) in MULTIPLES.items():
        vals = peer_mults[m]
        median = statistics.median(vals) if vals else None
        impl = implied_price(m, median, target_info) if median is not None else None
        rows.append({
            "multiple": label,
            "peer_median": round(median, 2) if median is not None else None,
            "n_peers": len(vals),
            "implied_price": round(impl, 2) if impl is not None else None,
        })

    df = pd.DataFrame(rows)
    impls = [r["implied_price"] for r in rows if r["implied_price"] is not None]
    print(f"Comparables for {args.target} ({cur}) — current price {price}")
    used = [s for s in peers if f"{s} (no data)" not in skipped
            and not any(x.startswith(s + " (") for x in skipped)]
    print(f"  peers used: {', '.join(used) or '(none)'}")
    if skipped:
        print(f"  peers skipped: {', '.join(skipped)}")
    print(df.to_string(index=False))
    if impls:
        print(f"\n  implied price range: {min(impls):.2f} – {max(impls):.2f} {cur} "
              f"(median {statistics.median(impls):.2f})")
        if price:
            mid = statistics.median(impls)
            print(f"  vs current {price}: {'upside' if mid > price else 'downside'} "
                  f"{(mid/price - 1):+.1%}")
    else:
        print("\n  no usable multiples for this target "
              "(likely pre-revenue / unprofitable — use scenario_valuation.py)")

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False)
        print(f"\n  wrote {out}")


if __name__ == "__main__":
    main()
