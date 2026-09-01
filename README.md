# Midpage's compliance function, as code

**Describes Midpage in one config file, aims a working GRC engine at the surfaces
Midpage already publishes, and ships seven findings — three of them machine-checked by
instruments in this repository, with tests that attack their own checkers.**

[![tests](https://github.com/tiffanidickerson437-lang/midpage-grc-program/actions/workflows/tests.yml/badge.svg)](../../actions/workflows/tests.yml)
[![sources](https://img.shields.io/badge/sources-public%20only%20%C2%B7%20checked%201%20Sep%202026-1b1d22)](00-governance/public-surface-map.md)
[![engine](https://img.shields.io/badge/engine-compliance--program-2b5cff)](https://github.com/tiffanidickerson437-lang/compliance-program)
[![evidence](https://img.shields.io/badge/evidence__in__repo-none-6b7280)](#ground-rules)

**▶ [The walkthrough](https://tiffanidickerson437-lang.github.io/midpage-a41f7c/)** —
the same argument on one page, addressed to the founder.

## Run it — 30 seconds, no key, no network

```bash
git clone https://github.com/tiffanidickerson437-lang/midpage-grc-program
cd midpage-grc-program && pip install pyyaml
cd 05-stakeholder-management/public-claims-consistency

python3 check_retention.py
python3 subprocessor_consistency.py
python3 check_metrics.py
```

```
Retention claims — 4 surfaces compared
  [CONTRADICTION  ] Third-party model providers receiving submitted queries:
                    security-page asserts 'bounded' (60 days),
                    data-for-legal-tech asserts 'zero'
  [INHERITED_GAP  ] Hosted MCP server: data-for-legal-tech claims 'none' on a path
                    that depends on model providers, which security-page bounds —
                    and the surface does not say so
  ...
4 finding(s). Each routes to the claim owner — nothing here edits a page.

Subprocessor disclosure — dpa-list 18 vs trust-center 15
  [UNDISCLOSED ] Datadog is on the contractual list and absent from the trust center
  [UNDISCLOSED ] Intercom is on the contractual list and absent from the trust center
  [UNDISCLOSED ] Pinecone is on the contractual list and absent from the trust center
```

Then attack the checkers themselves — **93 tests** across three suites. Every checker
carries a **control test** (clean input must produce zero findings) and a **mutation
guard** (gut a comparator to always-pass and its own suite turns red). Same inputs, same
output, every run. No model in the pass/fail path.

```bash
pip install -r requirements-dev.txt
python3 -m pytest -q
```

---

This is what the first quarter of owning compliance at Midpage looks like, built
entirely from what Midpage already publishes. Midpage is nine people with SOC 2 Type II,
a HIPAA attestation, eighteen subprocessors, four model providers, personal health
information, cardholder data, and privileged attorney work product moving through all of
it — and **no security, compliance, or privacy headcount at all.** Diligence routes to a
shared inbox.

That is not carelessness. It is the correct trade for a company that went from pre-
traction to $3M ARR on seed money. The bill for it comes due at the Series A, and
[the Series A has not been filed yet](00-governance/public-surface-map.md) — one Form D,
May 2025, nothing since. This repository is the operated version of the function, not a
document about one.

### The short version, in four lines

- **Three of Midpage's own surfaces give three different answers about how long a
  submitted query survives**, including a blanket zero-retention claim on one page and a
  sixty-day retention statement on another.
  [Machine-checked (F1).](05-stakeholder-management/public-claims-consistency/)
- **The subprocessor list the DPA contractually points at has three vendors the trust
  center does not show** — Pinecone, Datadog, and Intercom — against a §4.2 promise of
  advance notice. [Machine-checked (F2).](05-stakeholder-management/public-claims-consistency/)
- **There is a Berlin office, and the entire public data-protection posture is built for
  a US company exporting out of the EEA.** No EU entity, no Article 27 representative, no
  lead supervisory authority — with an EU model provider and a named European data
  customer. [The largest finding here.](02-ai-governance/eu-establishment/)
- **Evidence exists for the claims nobody doubts and assertions for the claims everybody
  asks about.** Five of eleven public commitments fall inside an existing report; the six
  that don't are the AI ones. [The map.](04-evidence-and-audit/claims-to-evidence.md)

## The findings

| # | Finding | Where |
|---|---|---|
| F1 | Four surfaces, four different answers on retention: zero-day required from every model provider, up to sixty days, no retention on the MCP server, no period at all on the trust center | [checker + report](05-stakeholder-management/public-claims-consistency/) |
| F2 | The DPA-named subprocessor list carries 18 providers; the trust center shows 15. Pinecone, Datadog, and Intercom appear only on the contractual one | [checker](05-stakeholder-management/public-claims-consistency/) |
| F3 | Two live marketing pages state two different monthly-visitor figures, 33% apart, neither defined | [checker](05-stakeholder-management/public-claims-consistency/) |
| F4 | A Berlin office against an export-shaped GDPR posture; no EU entity, no Art. 27 representative, no lead supervisory authority published | [readiness assessment](02-ai-governance/eu-establishment/) |
| F5 | "SOC 2 Type II certified" on the sales page — SOC 2 is an attestation; the security page and trust center both get this right | [trust collateral](05-stakeholder-management/trust-collateral.md) |
| F6 | A disclosed CCPA sale-or-sharing, and cross-customer deidentified insight sharing, on a platform holding privileged work product | [data-use commitments](02-ai-governance/data-use-commitments.md) |
| F7 | No end-user documentation and no changelog: `docs.midpage.ai` is developer-only, sixteen tutorials sit unindexed in a marketing blog | [trust collateral](05-stakeholder-management/trust-collateral.md) |

## The pillars

| | Pillar | What is in it |
|---|---|---|
| 00 | [Governance](00-governance/) | Surface map and thirteen open questions — the research position, auditable |
| 01 | [TPRM](01-tprm/) | The model-provider tier: where a standard SaaS questionnaire stops working |
| 02 | [AI governance](02-ai-governance/) | The EU establishment question; three data-use commitments in tension |
| 03 | [Secure development](03-secure-development/) | Model routing as a governed change type, notice gate first |
| 04 | [Evidence & audit](04-evidence-and-audit/) | Eleven public claims mapped to the evidence each would need |
| 05 | [Stakeholder management](05-stakeholder-management/) | F1–F3 checkers, F5 and F7; claims hygiene as a revenue control |
| — | [30 · 60 · 90](30-60-90/) | Sequenced by what unblocks revenue, sized for nine people |
| — | [The config](generated/companies/midpage/midpage.config.yaml) | One file, every value marked verified / filed / inferred / deliberately unset |
| — | [Engine bridge](generated/engine-bridge.md) | How the [engine](https://github.com/tiffanidickerson437-lang/compliance-program) maps on, and the three checkers this instance added back |

## Ground rules

1. **Public sources only** — every claim traces to the
   [surface map](00-governance/public-surface-map.md) with a check date. The author is a
   **paying Midpage subscriber**, disclosed
   [in the config](generated/companies/midpage/midpage.config.yaml) precisely because
   **no account data, support correspondence, or in-product observation is used anywhere
   in this repository.**
2. **Gaps are the work, never the criticism.**
3. **Evidence is computed, never authored.** `evidence_in_repo: none` — the instruments
   run against committed, dated observations of public pages, and no output should be
   read as if they touched a Midpage system.
4. **Live pages change without notice.** A finding that was true in September and
   asserted in November is not a finding; the checkers exist so the observation can be
   re-run, not remembered.
5. **No third party is characterised.** Midpage's auditor is named on their own security
   page and is deliberately absent from this repository. None of the seven findings needs
   an opinion about an audit firm, and this repository does not offer one.

Prior instances of the same method:
[mattermost-grc-manager-program](https://github.com/tiffanidickerson437-lang/mattermost-grc-manager-program) ·
[plaid-grc-engineering-program](https://github.com/tiffanidickerson437-lang/plaid-grc-engineering-program) ·
[jasper-grc-lead-program](https://github.com/tiffanidickerson437-lang/jasper-grc-lead-program)

---

Not affiliated with, endorsed by, or sponsored by Midpage AI Inc. No Midpage trademark
or logo is used. This is an independent work product. See
[`docs/deliverables.md`](docs/deliverables.md) for the deliverables index and
[`SECURITY.md`](SECURITY.md) for the security policy.
