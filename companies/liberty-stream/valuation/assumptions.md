# LibertyStream — Valuation Assumptions & Findings

> ⚠️ **Illustrative.** These inputs are first-pass estimates to exercise the
> scenario model, not researched conclusions. Refine each from company filings,
> the Select Water Solutions agreement, and lithium-price forecasts before
> drawing investment conclusions.

## Company-level inputs
| Input | Value | Basis |
|---|---|---|
| Currency | CAD | Primary listing LIB.V (TSXV) |
| Net debt | -4,360,663 (net cash) | yfinance: totalDebt 2,791,965 − totalCash 7,152,628 |
| Current price | 1.06 CAD | yfinance snapshot 2026-06-09 |
| Discount rate | 18% | High, reflecting early-stage execution + lithium-price risk |

## Production anchors (sourced — the announced 3-stage roadmap)
- Pilot automated refining unit: **~10 tpa** now (field-scale, Dec 2025).
- **Stage 1: up to 1,000 tpa**, commissioning by **Dec 2026**.
- **Stage 2: +1,000 tpa** (2nd facility) on/before **June 2027** → ~2,000 tpa.
- **Stage 3: from July 2027**, "**at least two additional**" 1,000-tpa
  facilities across Howard/Martin/Midland/Upton/Glasscock Counties → ~4,000 tpa.
- Each commercial unit is **~1,000 tpa**. **Committed capacity ≈ 4,000 tpa.**
- Blue-sky **potential ~220,000 tpa LCE** (aspirational; NOT a scenario).

## Lithium pricing (sourced, re-anchored Jun 2026)
Battery-grade lithium carbonate — NOT the cheaper technical grade. Re-anchored
after an initial draft used trough-era prices that were far too low.
- **Current spot (China benchmark, early Jun 2026):** CNY ~170,000–180,000/t,
  off a two-year high of CNY 200,500 (13 May 2026). At ~7.15 CNY/USD ≈
  **US$24,000–25,000/t** (peak ≈ US$28k in May).
- **Bernstein forecast:** ~$12k avg (2025) → **$20k (2026)** → **$25k (2027)**.
- **Consensus:** structural **deficit** late-2026/2027, elevated prices through
  2030; but lithium is highly cyclical (was ~$80k in 2022, ~$10k in 2024).
- **Anchoring rule (through-cycle band):** bear = downcycle/incentive
  **$15k**, base = mid-cycle / Bernstein-2026 **$20k**, bull = tight-market /
  Bernstein-2027 / spot-held **$25k**. FX **~1.37 CAD/USD**.
- Note: margins held flat across scenarios, but with largely fixed per-tonne
  opex, higher prices would **expand** margins (operating leverage) — so the
  EBITDA assumption is conservative at the base/bull prices.

## Scenarios (in scenario.json) — year-by-year ramp
Now modeled as a **production ramp** (`tools/scenario_valuation.py` discounts
each year's FCF = EBITDA − capex, plus a terminal exit value). FX = 1.37 CAD/USD,
applied explicitly; prices below in USD/t. Run with `--detail` for yearly tables.

Discount rate **10%** — assumes execution risk is captured via the scenario
probabilities, so it is NOT also loaded into the rate (avoids double-counting).
This is low for a micro-cap developer (15–25% typical); it is a deliberate
choice tied to the probability weighting.

| Scenario | Prob | Ramp (tpa by year) | Price USD/t | Opex USD/t | Eff. margin | Exit EV/EBITDA | Shares at exit |
|---|---|---|---|---|---|---|---|
| bear | 40% | y1 1,000 → y2 2,000 | 15,000 | 7,000 | ~53% | 8× | 280M |
| base | 40% | y1 1,000 → y2 2,000 → y3 4,000 | 20,000 | 7,000 | ~65% | 12× | 340M |
| bull | 20% | y1 1,000 → y2 3,000 → y3 6,000 → y4 10,000 | 25,000 | 7,000 | ~72% | 15× | 420M |

Margin is now **derived** from `EBITDA = (price − opex) × tonnes`, not assumed.
Opex US$7,000/t is based on the company's disclosed ~**US$6.2k/t** operating
cost (press release, ~Jun 2026), rounded up. Because opex per tonne is ~fixed,
margin **expands** with price (operating leverage) — 53%/65%/72%.

Exit EV/EBITDA raised from 6/8/9× to **8/12/15×**: the earlier figures
implicitly treated the terminal year as no-growth, but each ramp is still
growing fast at exit and has the 220k-tpa runway beyond — a buyer/market pays
up for that. Higher multiples for the higher-growth cases.

Rationale:
- **Ramp, not a single year** — production builds Stage by Stage; interim FCF
  (net of capex) is now credited, then a terminal EV on the final-year EBITDA.
- **bear** ≈ Stages 1–2 (2,000 tpa); **base** ≈ full announced roadmap
  (4,000 tpa); **bull** assumes expansion **beyond** the announced stages
  (~10 facilities) — still only ~5% of the 220k blue-sky.
- Dilution 215.6M → 280–420M shares to fund the build-out.

### Opex vs. capex — what they mean
These two inputs model **different** cash flows and don't overlap:
- **Opex (per tonne)** = cost of *running* production — reagents, energy,
  labour, processing. `EBITDA = (price − opex) × tonnes`, before interest/tax/
  D&A. Now set to **US$7,000/t** from the company's disclosed ~US$6.2k/t.
- **capex** = cash to *build* new capacity (DLE + refining units).
  `FCF = EBITDA − capex` each ramp year.
- **No double-count:** EBITDA is *before* depreciation, so subtracting build
  capex doesn't hit the same dollar twice. The model *omits* tax, working
  capital, interest, and post-ramp sustaining capex — the exit multiple is
  assumed to price those in.
- ⚠️ capex (CAD 4–12M/yr) is still an **invented placeholder** — no filed
  figure. And the US$6.2k/t opex may exclude **corporate SG&A** and sustaining
  capex (see Limitations).

## Headline finding (discount 10%, exit 8/12/15×, opex US$7k/t)
- Probability-weighted intrinsic value ≈ **2.47 CAD/share** vs **1.06** market →
  **~+133% UPSIDE**. (Per scenario: bear 0.61, base 2.16, bull 6.83.)
- Adding the real ~US$7k/t opex lifted derived margins to **53/65/72%** (vs the
  earlier invented 20/30/40%), roughly doubling the value again. Even the
  **bear** case (0.61) is now ~58% of the market price, and **base** (2.16) is
  ~2× it.
- ⚠️ **Terminal value dominates heavily.** At 10% discount + high multiples the
  exit value swamps ramp cash flows — bull = CAD 2,527M terminal PV vs 336M
  from ramp FCF (~88% terminal). The result rests largely on the
  **exit-multiple assumption** and on lithium prices **staying elevated**, not
  on near-term cash generation.
- Comps (`comps.csv`) remain **n/a** (no revenue/EBITDA/EPS) — confirms
  multiples don't fit a pre-revenue name (yet).
- **Highest-sensitivity levers (in order):** lithium price and exit EV/EBITDA,
  then discount rate, then production scale. opex/capex/FX secondary now that
  opex is grounded. See **Limitations** for what's still unverified.

## Limitations

Every input below is **not yet grounded** — either not researched, or no public
figure exists. Listed roughly by impact on the valuation. The headline figure
should be read as *conditional on these*, not as a point estimate.

### Assumptions with no/weak public basis (we invented them)
- **Capex (CAD 4–12M/yr per ~1,000-tpa unit)** — pure placeholder; no filed
  build-cost figure. Affects ramp FCF (minor) more than terminal value.
- **Exit EV/EBITDA (8/12/15×)** — judgment, not benchmarked to clean comps
  (peer lithium multiples are cyclically distorted; target has no EBITDA).
  Terminal value is ~88% of the answer, so this is a top-2 swing factor.
- **Discount rate (10%)** — chosen low on the rationale that risk sits in the
  scenario probabilities; not derived from a WACC build-up. Aggressive for a
  micro-cap developer.
- **Scenario probabilities (40/40/20)** — subjective; not from any base-rate
  analysis of comparable DLE ramps.
- **Shares at exit / dilution (215.6M → 280–420M)** — guessed; no disclosed
  capital-raise plan or equity-funding schedule.
- **Bull-case production (10,000 tpa) and base steady-state (4,000 tpa beyond
  what's commissioned)** — extrapolations beyond the *committed* roadmap.

### Assumptions partially grounded but uncertain
- **Opex US$7k/t** — based on a disclosed ~US$6.2k/t (press release). Unclear
  whether it is all-in: likely **excludes corporate SG&A** and sustaining
  capex, and may be at pilot scale / a single facility. If it understates true
  cost, margins (53/65/72%) are overstated.
- **Lithium price band (US$15/20/25k)** — anchored to current spot + analyst
  forecasts, but lithium is extremely cyclical (was ~$80k in 2022, ~$10k in
  2024). Holding $20–25k through the ramp is a strong assumption; the result is
  highly sensitive to it.
- **FX (1.37 CAD/USD)** — current rate held constant; no forward/hedging view.
- **Ramp timing** — Stage 1 (Dec 2026) / Stage 2 (Jun 2027) are company dates,
  but hitting *nameplate* output on schedule is assumed, not guaranteed.

### Model structure simplifications
- **No income tax** modelled (EBITDA → FCF directly). Overstates value.
- **No working capital** or interest modelled.
- **Terminal value** assumes the final-year EBITDA is sustainable in perpetuity
  at the chosen multiple; ignores resource depletion and post-ramp sustaining
  capex.
- **Net debt (-4.36M)** is a yfinance snapshot and will move with every raise.

### To refine next (highest value first)
1. Filed/guided **per-stage capex** and the **funding/dilution** plan.
2. Whether the ~US$6.2k/t opex is **all-in** (incl. SG&A, sustaining capex).
3. **Offtake/contract pricing** vs spot (their purchase orders may fix price).
4. A defensible **exit multiple** from cleaner peer analysis.
5. After-tax modelling and a realistic **timeline to multi-facility scale**.
