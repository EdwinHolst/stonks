---
name: research-company
description: Stand up a new company research folder in this stonks repo — create the folder from the standard template, web-research the business and listing, fill overview.md/sources.md/notes.md, and pull financial statements with tools/fetch_financials.py. Use when the user wants to start researching a new stock/company or refresh an existing company's data.
---

# Research a company

Bootstraps (or refreshes) a company's research folder following this repo's
conventions. Read `docs.md` first if unsure of current conventions.

## Inputs needed
- Company name and its **listing**: exchange + ticker. The yfinance ticker
  format matters (TSX Venture = `.V` suffix, e.g. `LIB.V`; NASDAQ/NYSE = bare,
  e.g. `MRLN`). If ambiguous, ask the user to confirm — one question at a time.

## Steps

1. **Pick the folder slug** (kebab-case, e.g. `liberty-stream`). If it doesn't
   exist under `companies/`, create the standard template:
   ```
   companies/<slug>/
     overview.md  financials/  valuation/  notes.md  sources.md
   ```

2. **Web research** the company. Capture into `overview.md`:
   - Ticker(s) & exchange(s), sector/industry, HQ, CEO, former names.
   - Business model (how it makes money), what stage it's at.
   - A short summary + a snapshot table (price, market cap, shares,
     revenue/TTM, net income, EPS, P/E, beta, 52w range, next earnings).
   Record every URL used in `sources.md` as markdown links, grouped by
   Data providers / Company / News & filings.

3. **Pull financials** with the existing tool (use the repo venv):
   ```bash
   . .venv/bin/activate
   python tools/fetch_financials.py <ticker> <slug>
   ```
   This writes `snapshot.csv`, `income.csv`, `balance-sheet.csv`,
   `cash-flow.csv` into `companies/<slug>/financials/`.

4. **Record data caveats** in `notes.md`: fiscal-year-end changes, pre-revenue
   status, currency (multiple listings → multiple currencies — pick a primary),
   dilution, and any open items to research from filings.

5. **Report** what was created/updated and flag anything that needs the user's
   judgement (ambiguous ticker, stale data, suspected data errors).

## Conventions (from docs.md)
- Default data format CSV, but stay format-agnostic.
- Don't invent business facts — only record what sourced research supports.
- If you do something here you'd repeat for other companies and it isn't yet a
  tool/skill, propose concretizing it (Python → `tools/`, Claude workflow →
  a new skill).
