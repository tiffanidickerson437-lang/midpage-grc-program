# Data-use commitments (F6)

Three public statements about what happens to customer data, on three surfaces, that
have to be read together — and that a law firm's outside counsel guidelines will read
together whether or not anyone at Midpage has.

## The three

**On the security page, under "No AI Model Training":**

> Midpage does not use customer data to train or fine-tune AI models.
> Midpage's agreements with AI model providers do not permit those vendors to train on
> Midpage customer data.

**In the privacy policy, under aggregate and deidentified data:**

> We may also share deidentified information about the activity of users across
> multiple customers' accounts in order to provide insights to you and other customers.

**In the privacy policy, for US residents:**

> [W]e may provide Personal Information of individuals who visit our Websites or
> otherwise provide their Personal Information for marketing purposes to third party
> partners, such as advertising partners, analytics providers, and social networks
> [...] This may be considered a data "sale" or "sharing" as those terms are defined
> under the CCPA and other applicable US privacy laws.

## Why they sit badly together

They are not contradictory. Read carefully, each has a scope the others do not touch:
training is one use, cross-customer insight generation is another, and the sale-or-
sharing disclosure is about website visitors rather than platform content. All three
can be simultaneously accurate.

The problem is that **the reader does not read carefully, and the reader who matters
reads adversarially.**

A litigator uploading a client's medical records has been told the platform does not
train on their data. Two clicks away, they read that activity across customer accounts
may be pooled into insights served to other customers, and that some personal
information may constitute a sale under the CCPA. Nothing reconciles those for them.
The natural inference — that "we don't train on it" is a narrow technical statement
concealing a broader commercial one — is almost certainly wrong and is entirely
available.

And it is not a hypothetical reader. It is question fourteen on an outside counsel
guidelines security addendum, and it is the reason a firm's general counsel refers a
tool to their malpractice carrier instead of approving it.

## What is actually missing

Not a policy change. Three artifacts, none of which exists publicly:

**A scope statement for the deidentified-insights feature.** The whole question is
whether "activity" means usage telemetry — sessions, feature counts, search volumes —
or anything derived from query content. If it is the former, saying so in one sentence
closes the issue permanently. If it is the latter, on a platform holding privileged
research, that needs a control, a legal basis, and probably a contractual opt-out
before it needs a sentence.

**A current-practice check on the sale-or-sharing disclosure.** Privacy policies
routinely carry this language as defensive boilerplate long after the practice stops.
If Midpage no longer shares with advertising partners, the disclosure is costing
enterprise deals for nothing. If it does, CPRA wants a conspicuous opt-out mechanism,
and no "Do Not Sell or Share My Personal Information" surface appears on the site.

**A single reconciled statement.** One place where a lawyer can read what happens to an
uploaded document end to end — Midpage's storage, the model provider's retention, the
training prohibition, the analytics boundary, and the deletion timeline — instead of
assembling it from a security page, a privacy policy, a DPA, and a trust center that
each answer part of it.

That last artifact is the deliverable. It is also, not coincidentally, the answer to
about a third of every enterprise security questionnaire Midpage will receive next year.

## Scope note

This section describes tension between published statements. It does not assert that
Midpage trains on customer data, sells customer data, or does anything improper with
either — nothing observable from outside supports any of those, and the security page's
commitments are unusually direct for a company this size. The finding is that the
public record does not let a careful reader confirm it.
