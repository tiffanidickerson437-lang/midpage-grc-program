# The model-provider tier

Where a standard SaaS vendor questionnaire stops being useful.

## The shape of the problem

Midpage discloses eighteen subprocessors. Sixteen of them are ordinary SaaS: hosting,
auth, billing, error capture, analytics, databases, orchestration. A tiered intake
model handles those well, and the usual questionnaire asks the usual questions.

Four are model providers — **Anthropic, Google, OpenAI, Mistral** — plus **Cohere** for
hosted index search. Those five sit in a different tier for four reasons, none of which
a standard SIG-Lite reaches:

**They receive the sensitive payload directly.** Not metadata about it, not a hash of
it: the submitted query, the uploaded brief, the medical record attached to a personal
injury matter. Everything the platform's confidentiality promise is about passes
through them.

**The commitment rides on their contract, not on Midpage's controls.** "Midpage's
agreements with AI model providers do not permit those vendors to train on Midpage
customer data" is a statement about someone else's paper. No Midpage-side control can
evidence it. Only the contract can, and only if someone reads it against the claim.

**Their terms move.** Retention windows, abuse-monitoring carve-outs, zero-retention
eligibility, and regional routing all change on provider timelines, without a change
control on Midpage's side. A vendor review that is annual is, for this tier, a review
that is wrong for eleven months.

**One of them is in the EU and one is in Canada.** Mistral (EU) and Cohere (Canada) put
transfer analysis inside the model tier rather than beside it — which matters
differently again if the [Berlin office](../02-ai-governance/eu-establishment/) is an
establishment.

## What the tier-1 review has to cover

A questionnaire that stops at "is the vendor SOC 2" answers none of the below.

| Question | Why it is in this tier and not the standard one |
|---|---|
| Zero-retention eligibility, per provider, per endpoint | It is usually a contract tier or an enrolment, not a default. Which endpoints are covered is the whole claim. |
| Abuse-monitoring retention carve-outs | Most providers reserve a retention window for safety review even under zero-retention terms. That window is where "zero" and "up to 60 days" stop contradicting each other — or don't. |
| Training prohibition: contract clause, not policy page | A published policy is revocable. A negotiated clause is the evidence. |
| Sub-processing by the provider | The chain does not stop at the model vendor. |
| Regional routing and data residency | Determines whether a query from an EU user leaves the EEA, and by what instrument. |
| BAA availability and scope | If PHI reaches the tier at all, this is the question that decides whether the HIPAA attestation means what a reader assumes. |
| Notice on material terms change | Without it, the annual review is the detection mechanism, and eleven months is the detection latency. |
| Model deprecation and forced migration | A provider retiring a model forces a change to a governed surface on the provider's schedule. See [model routing](../03-secure-development/model-routing-change-management.md). |

## The reassessment cadence problem

Midpage's security page commits to reassessing subprocessors "periodically." For
sixteen of the eighteen, annual is right. For the model tier, an annual cadence cannot
detect a mid-year change in retention terms — and the public claim that would become
untrue is one of the load-bearing ones.

The cheap fix is not a faster full reassessment. It is a **term-change monitor**: a
short, dated record per provider of the specific clauses the public claims depend on,
re-read on a quarterly cadence, with a diff. That is a few hours a quarter, and it is
the difference between finding out from your own monitor and finding out from a
customer's security review.

## What this section is not

It is not an assessment of any provider. Nothing here says Anthropic, Google, OpenAI,
Mistral, or Cohere handles data badly — they are, individually, among the more
scrutinised processors in the market. The finding is about **the tier's review
mechanics**, which is a Midpage-side question and the only kind this repository is in a
position to raise.
