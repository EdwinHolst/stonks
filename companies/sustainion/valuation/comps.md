# Sustainion — Comparable-Company Valuation

*Run date: 2026-06-10. All figures SEK. Source: yfinance / stockanalysis.com.*

## Peer multiples

| Company | Mkt cap (BSEK) | P/E | EV/EBITDA | EV/Rev | P/B | EBIT% |
|---|---:|---:|---:|---:|---:|---:|
| OEM International | 22.7 | 36.3× | 26.2× | 4.1× | 7.5× | 15.4% |
| AQ Group | 20.7 | 30.1× | n/a | n/a | 4.4× | 6.9% |
| Momentum Group | 5.6 | 30.8× | 17.8× | 2.0× | 6.6× | 7.6% |
| Alligo | 6.7 | 23.2× | 12.3× | 1.1× | 2.2× | 7.3% |
| Xano | 2.9 | 16.9× | 9.7× | 1.1× | 1.5× | 7.7% |
| Profilgruppen | 0.7 | 7.4× | 4.0× | 0.4× | 1.0× | 8.3% |
| Duroc | 0.7 | n/a | 28.2× | 0.4× | 0.7× | −6.5% |
| **Sustainion (SUSG)** | **0.4** | **12.7×** | **8.8×** | **0.8×** | **1.8×** | **4.5%** |

*Peer median (all 7, as computed by comps.py):*

| Multiple | Peer median | Implied price | vs 1.78 SEK |
|---|---:|---:|---:|
| P/E | 26.6× | 3.73 SEK | +110% |
| EV/EBITDA | 15.1× | 3.34 SEK | +88% |
| EV/Revenue | 1.09× | 2.51 SEK | +41% |
| P/B | 2.21× | 2.23 SEK | +25% |

**Median of implied prices: 2.92 SEK (+64%)**

## Interpretation

### Outliers to set aside

Two peers distort the median in opposite directions:

- **Duroc** — EV/EBITDA of 28.2× on a company running −6.5% EBIT margins means the multiple is mechanically inflated (near-zero EBITDA denominator). It is also in portfolio transition mode, divesting fibre businesses. Exclude from EV/EBITDA.
- **Profilgruppen** — An aluminium extrusion mono-product business in a cyclical trough. P/E of 7.4× and EV/EBITDA of 4.0× reflect sector cyclicality, not a steady-state roll-up multiple. Informative as a floor, not a comp.
- **OEM International and Momentum Group** — Both are high-quality niche distributors with 7–15% EBIT margins and multi-decade track records, earning a deserved premium. Sustainion at 4.5% EBIT doesn't belong in the same bracket yet.

### Tightest comps

The two companies with the most similar profile to Sustainion — size, model, margin level — are **Alligo** and **Xano**:

| Multiple | Alligo | Xano | Median | Implied price | vs 1.78 |
|---|---:|---:|---:|---:|---:|
| P/E | 23.2× | 16.9× | 20.1× | 2.82 SEK | +58% |
| EV/EBITDA | 12.3× | 9.7× | 11.0× | 2.23 SEK | +25% |
| EV/Revenue | 1.1× | 1.1× | 1.10× | 2.51 SEK | +41% |
| P/B | 2.2× | 1.5× | 1.85× | 1.87 SEK | +5% |

**Median of these implied prices: ~2.36 SEK (+33%)**

Note: Alligo is partly not applicable as the user flagged — it is a wholesale distribution group, less acquisition-driven than Sustainion. Xano is precision manufacturing, not holding. Both are fair reference points but neither is a clean read.

### The margin gap is the core issue

Sustainion's 4.5% EBIT margin vs. 7–8% for Alligo/Xano/Momentum explains most of the valuation gap. At peer-level margins on current revenue (~538 MSEK), Sustainion would generate ~37–42 MSEK EBIT vs. the ~24 MSEK it currently earns. Closing that gap — through mix improvement in the acquired businesses, operating leverage on the new cost base, or higher-margin acquisitions — is the central re-rating lever.

### Summary

| Scenario | Basis | Implied price | vs 1.78 |
|---|---|---:|---:|
| Full peer median (7 peers) | comps.py output | 2.92 SEK | +64% |
| Tightest comps (Alligo + Xano) | median of 4 multiples | ~2.36 SEK | +33% |
| P/B floor (Profilgruppen trough) | 1.0× P/B | ~1.01 SEK | −43% |
| Current price | — | 1.78 SEK | — |

**Conclusion:** On the most relevant small-cap Swedish industrial comps, Sustainion appears ~25–40% undervalued today, with upside to ~2.3–2.9 SEK if margins converge toward peer levels. The discount is rational given the recency of the Ströman Maskin acquisition and the thin current margin profile — it is a show-me story. The P/B floor (~1.0×, Profilgruppen in a downcycle) gives a rough downside scenario around 1.00 SEK.

## Caveats

- Run-rate EBITDA may be higher than FY2025 reported, since Ströman Maskin contributed only part-year. True EV/EBITDA on full-year run-rate is likely closer to 7–8×, which is below even Xano.
- AQ Group missing EV/EBITDA data from yfinance — would be a useful additional data point.
- No dividend; no forward EPS estimate available via yfinance.
- Next step: scenario model on normalised margins (`tools/scenario_valuation.py`).
