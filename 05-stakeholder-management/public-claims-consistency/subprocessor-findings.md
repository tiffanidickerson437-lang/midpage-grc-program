# Subprocessor disclosure — findings (F2)

Rendered by `subprocessor_consistency.py --render` from [`subprocessors.yaml`](subprocessors.yaml). Do not edit by hand — re-run the tool.

## The commitment

> Midpage maintains a list of its Sub-processors at https://www.midpage.ai/subprocessors. Midpage will provide reasonable advance notice (via updates to such list or email notification) before allowing any new Sub-processor to Process Customer Personal Data.

DPA section 4.2, effective 2026-04-28. That clause is what makes the rows below a question about a promise rather than a question about tidiness.

## Surfaces compared

| Surface | Authority | Checked | Providers listed |
|---|---|---|---|
| [dpa-list](https://www.midpage.ai/subprocessors) | contractual | 2026-09-01 | 18 |
| [trust-center](https://trust.midpage.ai/subprocessors) | assurance | 2026-09-01 | 15 |

## Findings

| # | Type | Provider | Detail |
|---|---|---|---|
| 1 | UNDISCLOSED | Datadog | Datadog is on the contractual list (dpa-list) and absent from the assurance surface (trust-center) |
| 2 | UNDISCLOSED | Intercom | Intercom is on the contractual list (dpa-list) and absent from the assurance surface (trust-center) |
| 3 | UNDISCLOSED | Pinecone | Pinecone is on the contractual list (dpa-list) and absent from the assurance surface (trust-center) |

Which list is correct is not observable from outside. Reconciling them, and deciding whether the advance-notice promise was met for each provider, is work for someone inside.
