# LibertyStream — Valuation

LibertyStream is **pre-revenue** (DLE lithium scale-up), so DCF and P/E comps
don't apply yet. Primary method here is the **scenario model**
(`tools/scenario_valuation.py`).

## Files
- `scenario.json` — scenario assumptions (bear/base/bull). **Illustrative** —
  see `assumptions.md`.
- `assumptions.md` — sourcing & justification for every input, plus findings.
- `comps.csv` — peer-multiple output (mostly n/a; kept to show comps don't fit).

## Run
```bash
. .venv/bin/activate
python tools/scenario_valuation.py companies/liberty-stream/valuation/scenario.json
python tools/comps.py LIB.V ALB,SQM --out companies/liberty-stream/valuation/comps.csv
```
