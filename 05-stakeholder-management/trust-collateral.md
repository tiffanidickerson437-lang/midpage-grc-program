# Trust collateral (F5, F7)

Two findings that cost nothing to fix and are noticed by exactly the people you would
rather not have noticing.

---

## F5 — "SOC 2 Type II certified"

On `midpage.ai/data-for-legal-tech`, in the data-quality section:

> Compliance already handled. SOC 2 Type II certified, HIPAA audited, and Zero Day
> Retention required from every model provider we use.

There is no such thing as SOC 2 certification. SOC 2 is an **attestation** engagement
under AICPA standards: a CPA firm issues an opinion on management's description of
controls and their operating effectiveness. Nobody is certified. There is likewise no
HIPAA certification or accreditation regime — a HIPAA report is an assessment against a
rule, not a mark conferred by a body.

The trust center gets this right. The security page gets this right — "independently
validated through annual SOC 2 Type II and HIPAA audits" is exactly correct. Only the
sales-facing page slips.

**Why it is worth a line item.** This is not pedantry about terminology. The audience
for `/data-for-legal-tech` is other legal-technology companies buying a data feed, and
their diligence goes to counsel. Counsel knows the difference between an attestation
and a certification, because the difference is what they are paid to know. A vendor who
writes "certified" reads one of two ways: careless about compliance language, or
willing to round up. Neither is what the sentence was trying to convey, and the sentence
was two words from being unimprovable.

**Fix:** "SOC 2 Type II attested, HIPAA assessed." One deploy.

---

## F7 — No end-user documentation, and no changelog

`docs.midpage.ai` exists and is good. It is also entirely developer-facing:

| Section | Contents |
|---|---|
| Getting Started | Introduction, Database Replica |
| Integration | MCP, Cases API, Laws API |
| Data Model | Schema, HTML Content Format, Format Variations, Citator |

Every page is for someone integrating the corpus. There is nothing for the person using
the product — no getting-started for the web application, nothing on projects or
project-level instructions, nothing on thread length, context limits, or how to carry
work between sessions.

The material exists. The blog carries 41 posts, 16 of them tagged Tutorials, including
practical ones on the grid view and on drafting. But they are filed in a marketing blog,
in reverse-chronological order, with no index inside the product and no route from the
application to any of them.

There is also no changelog. `midpage.ai/changelog` returns 404. `updates.midpage.ai`
redirects to the blog. Nine Product Updates posts exist, interleaved with legal analysis
and company news, and there is nothing to subscribe to. Users find out the product
changed by opening it and noticing.

**Why this is in a compliance repository.** Three reasons, and only the third is
obvious:

*It is questionnaire load.* "Describe your customer-facing documentation and change
notification process" is a standard enterprise questionnaire item. The current answer is
a blog URL.

*It is a data-handling comprehension problem.* Users of a legal research tool need to
know what persists between sessions and what does not, because that determines what they
can safely upload. The retention answers exist across four surfaces (see
[F1](public-claims-consistency/)) and none of them is in the product, in language a
litigator reads before uploading a client file.

*It is support cost at nine people.* Every question answered by hand in a support
conversation is a question a documentation page would have answered at zero marginal
cost, on a team where support and engineering are the same people.

**Fix:** a user-docs section under `docs.midpage.ai`, an index of the existing tutorials,
one page on data handling written for a lawyer rather than for counsel, and a changelog
with an RSS feed. None of it is new writing except the data-handling page. Most of it is
routing content that already exists to where people can find it.

---

## Provenance

Both findings are observations of public pages, recorded in the
[surface map](../00-governance/public-surface-map.md) with the date they were read. F7
in particular is written from the outside — from what the documentation site and sitemap
show — and not from anything observed inside a Midpage account.
