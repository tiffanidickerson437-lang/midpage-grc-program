# Retention claims — findings (F1)

Rendered by `check_retention.py --render` from [`retention-claims.yaml`](retention-claims.yaml). Do not edit by hand — re-run the tool.

Each row below describes disagreement between Midpage's own public surfaces. None of it describes Midpage's actual retention, which is not observable from outside.

## Surfaces compared

| Surface | Audience | Checked | Paths addressed |
|---|---|---|---|
| [security-page](https://www.midpage.ai/security) | assurance | 2026-09-01 | web-app, plugins, model-providers |
| [data-for-legal-tech](https://www.midpage.ai/data-for-legal-tech) | marketing | 2026-09-01 | model-providers, mcp-server |
| [privacy-policy](https://www.midpage.ai/privacy-policy) | legal | 2026-09-01 | web-app |
| [trust-center](https://trust.midpage.ai/) | assurance | 2026-09-01 | web-app |

## Findings

| # | Type | Path | Detail |
|---|---|---|---|
| 1 | CONTRADICTION | model-providers | Third-party model providers receiving submitted queries: security-page asserts 'bounded' (60 days), data-for-legal-tech asserts 'zero' |
| 2 | PERIOD_ABSENT | web-app | Web application storage (Midpage's own systems): trust-center is an assurance surface and states no period, while privacy-policy, security-page state 60 days |
| 3 | INHERITED_GAP | mcp-server | Hosted MCP server offered to data customers: data-for-legal-tech claims 'none' on a path that depends on Third-party model providers receiving submitted queries, which security-page bounds — and the surface does not say so |
| 4 | BACKUP_CARVEOUT | web-app | Web application storage (Midpage's own systems): privacy-policy states 60 days but carries an exception with no stated horizon |

The fix for every row is a decision by the claim owner, then a monitor — never a silent edit by a checker.
