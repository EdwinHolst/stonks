# tools/

Python tools for the stock-research workflow. Default language is Python
(see `../docs.md`). Reusable *Claude-driven* workflows live as skills under
`../.claude/skills/` instead.

## Setup

```bash
# from repo root
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Tools

### fetch_financials.py
Fetch fundamentals + financial statements for a ticker via yfinance and save
them as CSV into a company's `financials/` folder.

```bash
python tools/fetch_financials.py <ticker> <company-folder> [--quarterly]

# examples
python tools/fetch_financials.py LIB.V liberty-stream
python tools/fetch_financials.py MRLN merlin
```

Writes `snapshot.csv`, `income.csv`, `balance-sheet.csv`, `cash-flow.csv`.
Ticker format is yfinance's (TSX Venture = `.V` suffix, e.g. `LIB.V`).

### dcf.py
Generic discounted-cash-flow valuation for revenue/FCF-positive companies.
Reads a JSON assumptions file, discounts projected FCF + Gordon terminal value,
prints per-share value and a discount-rate × terminal-growth sensitivity grid.

```bash
python tools/dcf.py companies/<slug>/valuation/dcf.json
```
Template: `tools/templates/dcf.example.json`.

### comps.py
Comparable-company (multiples) valuation. Pulls peer multiples (P/E, EV/EBITDA,
EV/Revenue, P/B) via yfinance, takes the peer median, applies to the target.

```bash
python tools/comps.py <target> <peer1,peer2,...> [--out PATH]
python tools/comps.py LIB.V ALB,SQM --out companies/liberty-stream/valuation/comps.csv
```
Bad/delisted peer tickers are skipped. Pre-revenue targets yield n/a — use
`scenario_valuation.py` instead.

### scenario_valuation.py
Scenario model for early-stage / pre-revenue companies. Each scenario runs a
**year-by-year production ramp**: per year revenue = production × price,
EBITDA = revenue × margin, FCF = EBITDA − capex (discounted), plus a terminal
exit value (final-year EBITDA × exit multiple). FX (CAD/USD) is explicit and
prices may be given in USD. Probability-weights bear/base/bull into an expected
per-share value.

```bash
python tools/scenario_valuation.py companies/<slug>/valuation/scenario.json
python tools/scenario_valuation.py companies/<slug>/valuation/scenario.json --detail
```
`--detail` prints the yearly ramp table per scenario.
Template: `tools/templates/scenario.example.json`.

## Pick the right valuation tool
- Profitable / FCF-positive → `dcf.py` (intrinsic) + `comps.py` (relative).
- Pre-revenue / early-stage → `scenario_valuation.py`.
