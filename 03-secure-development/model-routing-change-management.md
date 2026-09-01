# Model routing as a governed change type

Midpage routes across four model providers and ships into three assistant platforms
plus its own web app. Swapping, adding, or re-routing a model is currently — as far as
any public surface shows — an engineering change. It is also, simultaneously, a change
to four governed things:

1. **The no-training commitment**, which is a statement about a specific provider's
   contract.
2. **The subprocessor disclosure**, which carries a contractual advance-notice promise
   under DPA §4.2.
3. **The retention claim**, which differs per provider and per endpoint.
4. **Transfer posture**, when the provider is in another jurisdiction — Mistral in the
   EU, Cohere in Canada.

A change that touches all four and is reviewed as a code change will pass code review
every time and still leave three public commitments stale.

## The design

Not a new process. A new **change type**, with a gate on the existing one.

```
model-routing change
  ├─ trigger:   new provider · new model on an existing provider · re-route
  │             · provider deprecation forcing migration · regional routing change
  ├─ gate 1:    is the provider on the disclosed subprocessor list?
  │               no  → advance notice obligation fires BEFORE the change ships
  │               yes → continue
  ├─ gate 2:    does the provider's retention posture match the public claim
  │             for this endpoint?
  │               no  → the claim changes, or the change does not ship
  ├─ gate 3:    does a training prohibition exist in contract for this endpoint?
  │               no  → the no-training claim does not cover this path
  ├─ gate 4:    jurisdiction — does this change where data goes?
  │               yes → transfer instrument re-checked
  └─ record:    dated entry naming provider, endpoint, retention, prohibition,
                jurisdiction, and the surfaces updated
```

Gate 1 is the one that has teeth, because it is the only gate attached to a promise
Midpage has already made in writing. The other three prevent a public claim going
quietly stale.

## Why the notice gate has to come first

DPA §4.2 promises *advance* notice. A process that updates the subprocessor page after
the routing change ships has not met that commitment — it has documented missing it.
The gate is cheap precisely because it is early: the notice obligation is trivial to
satisfy before a change and impossible to satisfy after.

The current divergence between the two subprocessor surfaces
([F2](../05-stakeholder-management/public-claims-consistency/)) is what this gate is
designed to prevent. Three providers appear on the contractual list and not on the
assurance surface. Whether that is staleness or a missed notice is
[open question 3](../00-governance/open-questions.md) — but a change type with gate 1
in it produces the answer as a by-product instead of requiring an investigation.

## The record is the point

One dated line per change, in a file, is the whole evidence artifact:

```yaml
- date: 2026-09-01
  change: "route long-context drafting to <provider>/<model>"
  provider: <provider>
  endpoint: <endpoint>
  retention: "zero-day, per <contract reference>; abuse-monitoring carve-out <n> days"
  training_prohibition: "contract §<n>"
  jurisdiction: US
  surfaces_updated: [subprocessors, security]
  notice: "advance notice sent <date>"
```

When an auditor asks how the no-training claim is controlled, or an enterprise customer
asks which model saw their document, that file is the answer. Without it the answer is
a conversation with an engineer, reconstructed, months later — which is not an answer
that survives a Type II observation window.

## Cost

Roughly a day to design against the real pipeline, and a few minutes per change after
that. It is the cheapest control in this repository and it protects the three most
expensive claims on the site.
