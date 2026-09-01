# Deliverables index

Everything in this repository, and what each thing is for.

## The instruments

Three tools. Run them in thirty seconds with no key and no network call.

| File | Finding | What it compares |
|---|---|---|
| [`check_retention.py`](../05-stakeholder-management/public-claims-consistency/check_retention.py) | F1 | Four public surfaces across four data paths |
| [`subprocessor_consistency.py`](../05-stakeholder-management/public-claims-consistency/subprocessor_consistency.py) | F2 | The DPA-named subprocessor list against the trust center |
| [`check_metrics.py`](../05-stakeholder-management/public-claims-consistency/check_metrics.py) | F3 | Two first-party traction figures |

Their observation files — [`retention-claims.yaml`](../05-stakeholder-management/public-claims-consistency/retention-claims.yaml),
[`subprocessors.yaml`](../05-stakeholder-management/public-claims-consistency/subprocessors.yaml),
[`metrics.yaml`](../05-stakeholder-management/public-claims-consistency/metrics.yaml) —
record what each page said on 1 September 2026, with the quote that supports it.

Their reports are rendered, never hand-written:
[retention](../05-stakeholder-management/public-claims-consistency/retention-findings.md) ·
[subprocessors](../05-stakeholder-management/public-claims-consistency/subprocessor-findings.md) ·
[metrics](../05-stakeholder-management/public-claims-consistency/metric-findings.md).
CI regenerates all three and fails if any is stale.

## The test suites

112 tests across four suites. Every checker carries a **control test** (clean input must
produce zero findings) and a **mutation guard** (gut the comparator and the suite must go
red).

| File | Tests |
|---|---|
| [`test_check_retention.py`](../05-stakeholder-management/public-claims-consistency/test_check_retention.py) | 33 |
| [`test_subprocessor_consistency.py`](../05-stakeholder-management/public-claims-consistency/test_subprocessor_consistency.py) | 29 |
| [`test_check_metrics.py`](../05-stakeholder-management/public-claims-consistency/test_check_metrics.py) | 31 |
| [`test_check_action_pins.py`](../.github/test_check_action_pins.py) | 19 |

## The repository's own controls

Everything [`SECURITY.md`](../SECURITY.md) claims is enforced by something that runs on
every push, not asserted in prose.

| File | What it is |
|---|---|
| [`check_action_pins.py`](../.github/check_action_pins.py) | Enforces the SHA-pinning control on every workflow, and refuses to pass when the workflow directory is empty |
| [`tests.yml`](../.github/workflows/tests.yml) | Hash-verified install, the pinning check, all four suites, and a render-staleness gate. No step may swallow a failure |
| [`codeql.yml`](../.github/workflows/codeql.yml) | `security-extended`, across Python and the workflow files themselves, weekly and on push |
| [`dependency-review.yml`](../.github/workflows/dependency-review.yml) | Blocks a PR introducing a vulnerable or badly-licensed dependency, at `low` severity |
| [`dependabot.yml`](../.github/dependabot.yml) | Actions and pip, weekly — the cost of pinning to SHAs is that something has to update them |

## The written work

| Document | What it is |
|---|---|
| [Public surface map](../00-governance/public-surface-map.md) | Every source, every date. The sourcing spine — if a claim is not traceable here, it does not belong in this repository. |
| [Open questions](../00-governance/open-questions.md) | Thirteen things not answerable from outside, written as questions rather than inferred past. |
| [Model-provider tier](../01-tprm/model-provider-tier.md) | Where a standard SaaS questionnaire stops working, and what the tier-1 review has to cover instead. |
| [EU establishment](../02-ai-governance/eu-establishment/) | **F4.** A Berlin office against a US-export data-protection posture. |
| [Data-use commitments](../02-ai-governance/data-use-commitments.md) | **F6.** Three public statements about customer data that outside counsel will read together. |
| [Model routing change management](../03-secure-development/model-routing-change-management.md) | Model routing as a governed change type, with the advance-notice gate first. |
| [Claims-to-evidence map](../04-evidence-and-audit/claims-to-evidence.md) | Eleven public commitments; five attested, six assertions — and the six are the AI ones. |
| [Audit clock](../04-evidence-and-audit/audit-clock.md) | When the SOC 2 Type II window closes — not publicly determinable, which is the finding. Also establishes that the security page's own "Last updated" stamp is stale across a revision that added a compliance claim. |
| [Trust collateral](../05-stakeholder-management/trust-collateral.md) | **F5** and **F7.** A compliance category error on a sales page; no end-user docs and no changelog. |
| [30 · 60 · 90](../30-60-90/) | The first quarter, sequenced by what unblocks revenue. |
| [The config](../generated/companies/midpage/midpage.config.yaml) | One file, every value marked verified / filed / inferred / deliberately unset. |
| [Engine bridge](../generated/engine-bridge.md) | What the engine renders unchanged, what it cannot render from outside, and the three checkers this instance added back. |

## Ground rules, restated

1. **Public sources only.** Every claim traces to the surface map with a check date.
2. **Gaps are the work, never the criticism.**
3. **Evidence is computed, never authored.** `evidence_in_repo: none`.
4. **Live pages change.** Re-run the checkers before asserting anything from them.
