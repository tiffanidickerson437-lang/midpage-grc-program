# First-party metrics — findings (F3)

Rendered by `check_metrics.py --render` from [`metrics.yaml`](metrics.yaml). Do not edit by hand — re-run the tool.

## Figures observed

| Surface | Party | Checked | Figure | Compared |
|---|---|---|---|---|
| [homepage](https://www.midpage.ai/) | first | 2026-09-01 | 200,000+ | yes |
| [data-for-legal-tech](https://www.midpage.ai/data-for-legal-tech) | first | 2026-09-01 | 150,000+ | yes |
| [semrush-via-crunchbase](https://www.crunchbase.com/organization/midpage-ai) | third | 2026-09-01 | 102,768 | no |

### Excluded from the comparison, and why

- **semrush-via-crunchbase** — Measures monthly web visits to the domain, not unique visitors who read cases. Recorded as context only; the checker excludes it from the comparison.

## Findings

| # | Type | Metric | Detail |
|---|---|---|---|
| 1 | DIVERGENT_FIRST_PARTY | monthly-unique-visitors | Monthly unique visitors: homepage states 200,000+, data-for-legal-tech states 150,000+ — 33% apart, both live on 2026-09-01 |
| 2 | DEFINITION_UNSTATED | monthly-unique-visitors | Monthly unique visitors is published on data-for-legal-tech, homepage with no stated population, window, or measurement source |

Neither figure is challenged here. Which one is right, and by what definition, is a question for whoever owns the claim.
