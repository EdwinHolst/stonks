#!/usr/bin/env python3
"""Fetch fundamentals and financial statements for a ticker via yfinance.

Saves into a company's `financials/` folder:
  - snapshot.csv        key metrics (one row, long format: metric,value)
  - income.csv          income statement (annual)
  - balance-sheet.csv   balance sheet (annual)
  - cash-flow.csv       cash flow statement (annual)

CSV is the default format (see docs.md), one file per statement.

Usage:
    python tools/fetch_financials.py <ticker> <company-folder> [--quarterly]

Examples:
    python tools/fetch_financials.py LIB.V liberty-stream
    python tools/fetch_financials.py MRLN merlin

Ticker format is yfinance's: TSX Venture uses a `.V` suffix (LIB.V),
NASDAQ/NYSE use the bare symbol (MRLN).
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPANIES_DIR = REPO_ROOT / "companies"

# Subset of yfinance `info` keys we capture as the snapshot.
SNAPSHOT_KEYS = [
    "longName", "symbol", "currency", "exchange", "sector", "industry",
    "currentPrice", "regularMarketPrice", "previousClose",
    "marketCap", "sharesOutstanding", "enterpriseValue",
    "totalRevenue", "netIncomeToCommon", "trailingEps", "forwardEps",
    "trailingPE", "forwardPE", "enterpriseToEbitda", "enterpriseToRevenue",
    "priceToBook", "totalCash", "totalDebt", "freeCashflow", "beta",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "dividendYield",
]


def fetch(ticker: str, folder: str, quarterly: bool = False) -> None:
    import yfinance as yf  # imported lazily so --help works without deps

    dest = COMPANIES_DIR / folder / "financials"
    if not dest.parent.exists():
        sys.exit(f"error: company folder not found: {dest.parent}")
    dest.mkdir(parents=True, exist_ok=True)

    t = yf.Ticker(ticker)
    info = t.info or {}
    if not info.get("longName") and not info.get("shortName"):
        sys.exit(f"error: no data returned for ticker '{ticker}' "
                 f"(check the symbol / yfinance suffix)")

    # --- snapshot (long format: metric,value) ---
    import pandas as pd
    rows = [(k, info.get(k)) for k in SNAPSHOT_KEYS]
    snap = pd.DataFrame(rows, columns=["metric", "value"])
    snap_path = dest / "snapshot.csv"
    snap.to_csv(snap_path, index=False)

    # --- statements ---
    statements = {
        "income.csv": t.quarterly_financials if quarterly else t.financials,
        "balance-sheet.csv": t.quarterly_balance_sheet if quarterly else t.balance_sheet,
        "cash-flow.csv": t.quarterly_cashflow if quarterly else t.cashflow,
    }
    written = [snap_path.name]
    for fname, df in statements.items():
        if df is None or df.empty:
            print(f"  (skipped {fname}: no data)")
            continue
        # Columns are period-end Timestamps; make them tidy date strings.
        df = df.copy()
        df.columns = [str(getattr(c, "date", lambda: c)()) for c in df.columns]
        df.index.name = "line_item"
        df.to_csv(dest / fname)
        written.append(fname)

    print(f"{info.get('longName')} ({ticker}) — {info.get('currency')}")
    print(f"  price={info.get('currentPrice') or info.get('regularMarketPrice')} "
          f"mktcap={info.get('marketCap')}")
    print(f"  wrote {len(written)} file(s) to {dest.relative_to(REPO_ROOT)}/:")
    for w in written:
        print(f"    - {w}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ticker", help="yfinance ticker, e.g. LIB.V or MRLN")
    p.add_argument("folder", help="company subfolder under companies/, e.g. liberty-stream")
    p.add_argument("--quarterly", action="store_true", help="fetch quarterly statements")
    args = p.parse_args()
    fetch(args.ticker, args.folder, args.quarterly)


if __name__ == "__main__":
    main()
