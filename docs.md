# Stonks — Project Docs

This file documents the purpose, structure, and decisions behind this repository so we don't have to re-derive them each session.

## Purpose

A workspace for investigating stocks: building evaluation models, summarizing
company data, and creating tools to speed up the research process.

## Repository structure

```
stonks/
  docs.md            # this file — process, decisions, conventions
  requirements.txt   # Python deps (yfinance, pandas)
  .venv/             # local virtualenv (gitignored)
  tools/             # Python tools (see tools/README.md)
    fetch_financials.py    # pull fundamentals + statements (CSV)
    dcf.py                 # generic DCF (FCF-positive companies)
    comps.py               # peer-multiples valuation
    scenario_valuation.py  # early-stage / pre-revenue scenario model
    templates/             # example assumption JSONs (dcf, scenario)
  .claude/skills/    # Claude-driven repeatable workflows (skills)
    research-company/SKILL.md
  companies/         # one subfolder per company we research
    merlin/
    liberty-stream/
```

## Skills (Claude workflows)

- **research-company** — bootstrap/refresh a company folder: template +
  web research → overview/sources/notes + run `fetch_financials.py`.

## Tooling setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

Note: this system's `python3` has no `pip`; use the venv (`venv` module works).

## Workflow conventions

- When setting up or changing the process, ask the user **one question at a time**.
- Record every decision here in docs.md so the question process isn't repeated.
- **Reusable assets — two kinds:**
  - **Python scripts** → `tools/` — for mechanical / data work (fetching
    prices, statements, computing DCF/comps). Default language: Python.
  - **Claude skills** → `.claude/skills/` — for repeatable *Claude-driven*
    workflows we'd run for many companies (e.g. "research a company overview",
    "build a DCF write-up"). Whenever we do something with Claude that we'd
    want to repeat for another company, concretize it into a skill.
- Build company models with a representative example first (currently
  **LibertyStream**), extracting tools/skills as repeatable patterns emerge.

## Open questions / decisions

Decisions will be appended below as they are made.

### Pending
- _(none)_

### Decided
- 2026-06-09: Parent folder is `companies/`, one subfolder per company.
- 2026-06-09: Ask one question at a time; document decisions in docs.md.
- 2026-06-09: Per-company folder layout:
  - `overview.md`   — business model, sector, summary
  - `financials/`   — raw financial data
  - `valuation/`    — evaluation models
  - `notes.md`      — ongoing research notes
  - `sources.md`    — links / references
- 2026-06-09: Data format — **CSV** is the default for raw financial data,
  but the structure stays **format-agnostic**: `financials/` may also hold
  JSON, Markdown, or other formats. Tooling should not assume CSV-only.
- 2026-06-09: Valuation models — primary focus is **DCF** and **Comparables
  (multiples)**. Open to **custom** scoring models later. (DDM not a priority.)
- 2026-06-09: Valuation approach = **option C**: build generic DCF + comps
  tooling for normal (revenue/FCF-positive) companies, PLUS a separate
  **scenario** template for early-stage / pre-revenue names (project future
  production × price → revenue → EBITDA → exit multiple → discount back).
  LibertyStream is pre-revenue, so the scenario model is what applies to it.
  Tools: `tools/dcf.py`, `tools/comps.py`, `tools/scenario_valuation.py`.
  Per-company assumptions live as JSON in `companies/<slug>/valuation/`.
- 2026-06-09: Tooling language — **Python** (pandas, yfinance, etc.).
- 2026-06-09: Company listings:
  - **Merlin Inc** — NASDAQ: MRLN (folder `companies/merlin/`)
  - **LibertyStream Infrastructure Partners Inc** — CVE (TSX Venture): LIB
    (folder `companies/liberty-stream/`)
  - **Sustainion Group AB** — Spotlight Stock Market (XSAT): SUSG / SUSG.ST
    (folder `companies/sustainion/`)
