# Claims-to-evidence map

Midpage makes eleven specific public commitments. Some are backed by a SOC 2 Type II and
a HIPAA report, and the fact that those exist is why this document is short rather than
long. The rest are assertions with no visible control and no evidence chain — which is
not the same as being untrue, and is exactly the same as being unprovable to a buyer.

The column that matters is the last one. `attested` means the claim plausibly falls
inside the scope of an existing report. `assertion` means it appears only as a sentence
on a page.

| # | Claim | Surface | What would evidence it | Status |
|---|---|---|---|---|
| 1 | AES-256 at rest, TLS 1.2+ in transit | security | Configuration evidence sampled across the observation window | attested |
| 2 | MFA on production and any Customer Data environment | security | IdP policy export plus exception list | attested |
| 3 | Access reviews at least twice yearly | security | Two dated review artifacts per period | attested |
| 4 | Background checks and annual security training | security | HR records, completion register | attested |
| 5 | Documented, tested incident response plan with post-incident review | security | Plan, dated test, one post-incident review | attested |
| 6 | Subprocessors assessed before engagement and reassessed periodically | security | An assessment record per subprocessor, dated, with the cadence stated | **assertion** — and the cadence is undefined; see [TPRM](../01-tprm/model-provider-tier.md) |
| 7 | Advance notice before a new subprocessor processes personal data | DPA §4.2 | A notice record per subprocessor addition | **assertion** — and [F2](../05-stakeholder-management/public-claims-consistency/) is the reason to check it |
| 8 | Midpage does not train or fine-tune on customer data | security | Pipeline control plus a negative-assurance test | **assertion** |
| 9 | Model-provider agreements prohibit training on customer data | security | The clause, per provider, mapped to endpoints | **assertion** — evidence lives in someone else's contract |
| 10 | Zero Day Retention required from every model provider | data-for-legal-tech | Per-provider zero-retention enrolment plus the abuse-monitoring carve-out | **assertion**, and in tension with claim 11 |
| 11 | Model providers may retain submitted queries for up to 60 days | security | Provider terms, per endpoint | **assertion**, and in tension with claim 10 |

## What the table says

Claims 1 through 5 are the ones a SOC 2 Type II is built to cover, and they are the ones
a buyer worries about least. Claims 8 through 11 — the AI-specific ones, the ones that
are the actual reason a law firm is nervous about this category of product — are the
ones with nothing behind them but a sentence.

That inversion is the whole finding. **Midpage has evidence for the claims nobody
doubts and assertions for the claims everybody asks about.** It is also completely
normal: no framework Midpage holds has an AI criterion, so no auditor asked, so no
evidence was produced. Auditors have started scoping AI into the existing Trust Services
Criteria under risk assessment, access control, and vendor management, which means the
question arrives at the next Type II regardless.

## The cheapest path

Not ISO 42001. Not yet — certification is a twelve-to-eighteen-month project and Midpage
is nine people.

The cheap path is to convert claims 6 through 11 from sentences into records, in that
order, because each one is a small artifact rather than a programme:

1. A subprocessor assessment register with dates and a stated cadence (claim 6).
2. A notice log, retroactive where possible (claim 7).
3. A per-provider contract extract mapping the training prohibition and the retention
   term to specific endpoints (claims 9, 10, 11) — this is the artifact that resolves
   F1, and it is a reading exercise, not an engineering one.
4. A pipeline attestation for claim 8: what would have to be true for customer data to
   reach a training path, and what prevents it.

Four artifacts. Together they turn the AI commitments from the weakest part of the
public record into the strongest, and they are the deliverables that make an ISO 42001
roadmap a roadmap instead of a wish.

## Note on scope

`evidence_in_repo: none`. Nothing above is evidence. It is a map of what evidence would
look like, built from the claims Midpage publishes. Whether any of it already exists
internally is [open question 11](../00-governance/open-questions.md) — several of these
records may well exist and simply not be public, in which case the finding is narrower
and the fix is publication rather than production.
