# Engine bridge

How the [compliance-program engine](https://github.com/tiffanidickerson437-lang/compliance-program)
maps onto Midpage, what it renders unchanged, and what it cannot render from outside.

The engine is a controls-as-code GRC program: one SCF-mapped control set, OSCAL-validated
profiles for thirteen frameworks, FAIR quantification, policy-as-code, and human-gated
AI in the drafting paths but never in the pass/fail path. This repository is what comes
out when it is aimed at Midpage with `midpage.config.yaml` as the input — plus three
instruments the engine did not have, written because Midpage's public surfaces raised
questions the generic engine had no checker for.

## What renders straight through

| Engine component | Applies to Midpage as |
|---|---|
| `02-controls/profiles/soc2.profile.oscal.json` | Held. The scope boundary across five product surfaces is the open question, not the criteria. |
| `02-controls/profiles/hipaa.profile.oscal.json` | Held. The BAA chain through four model providers is where it stops being routine. |
| `02-controls/profiles/gdpr.profile.oscal.json` | The Berlin office turns this from an export profile into an establishment profile. Same controls, different trigger article. |
| `02-controls/profiles/eu-ai-act.profile.oscal.json` | Provider-side obligations, plus the Annex III argument for administration-of-justice contexts. |
| `02-controls/profiles/nist-ai-rmf.profile.oscal.json` | The right working frame at nine people: free, non-certifying, and maps onto ISO 42001 later. |
| `02-controls/profiles/pci.profile.oscal.json` | Almost certainly SAQ A via Stripe. The profile exists to produce the memo, not a programme. |
| `02-controls/profiles/iso42001.profile.oscal.json` | Roadmap only. Certification at this size would be the wrong project. |
| `03-tprm/vendor-tiering-model.md` | Applies directly, with [one tier the model does not currently have](../01-tprm/model-provider-tier.md). |
| `04-ai-governance/*` | The whole section is the engagement. Nothing renders without inputs from inside. |
| `07-stakeholder-management/sales-faq.yaml` | Becomes the questionnaire answer bank in [days 1–30](../30-60-90/). |

## What the engine could not render, and why

The engine's richest sections — the FAIR risk register, the control library with
evidence schemas, the auditor narratives, the POA&M-as-issues workflow — all take
**internal state** as input. Control implementation status, incident history, asset
inventory, risk appetite. None of it is observable from outside a company, and rendering
those sections from public pages would produce documents that look authoritative and are
fabricated.

So they are absent here. `evidence_in_repo: none` is not modesty; it is the reason
everything else in this repository can be re-run by a stranger.

## What this instance added back

Three checkers the engine did not have, written for questions Midpage's own surfaces
raised:

**`check_retention.py`** — a four-path retention comparator with a dependency model. The
engine's claims checker compared certification *sets* across surfaces; that shape cannot
express "no retention here, sixty days one hop downstream, and one surface says so while
another doesn't." The `depends_on` / `discloses_dependency` pair is the new idea, and it
is what lets the tool distinguish an honest claim from a silent one instead of flagging
both.

**`check_metrics.py`** — first-party figure comparison with an *enforced* incomparability
rule. A surface excluded from the comparison must state why, and the validator refuses to
load it otherwise. Written after noticing how easy it would be to compare a Semrush
number against a marketing claim and call the difference a finding.

**`subprocessor_consistency.py`** — the engine had nothing that weighted one disclosure
surface above another. This version records *authority*: one list is named in a contract
that carries an advance-notice promise, the other is the surface auditors read. Direction
matters, so the tool reports it.

All three belong upstream. The retention dependency model in particular generalises to
any company whose confidentiality promise passes through a model provider, which by now
is most of them.

## Prior instances of the same method

[mattermost-grc-manager-program](https://github.com/tiffanidickerson437-lang/mattermost-grc-manager-program) ·
[plaid-grc-engineering-program](https://github.com/tiffanidickerson437-lang/plaid-grc-engineering-program) ·
[jasper-grc-lead-program](https://github.com/tiffanidickerson437-lang/jasper-grc-lead-program)

Each was rendered for a company from one config, with instruments written for whatever
that company's public record actually raised. This one differs in a single respect:
there is no job posting to match against. Midpage has no compliance role open. The
frame is the seat that does not exist yet.
