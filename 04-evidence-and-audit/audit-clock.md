# The audit clock

When does Midpage's SOC 2 Type II observation window close, and when does the report go
stale? This is the first question a Series A diligence team asks and the first question
an enterprise reviewer asks, and it is worth knowing the answer before either of them
does.

**Short version: it is not publicly determinable, and that is itself the finding.**

## What is actually stated

| Source | What it says |
|---|---|
| [`/security`](https://www.midpage.ai/security) | "independently validated through annual SOC 2 Type II and HIPAA audits" |
| [`/dpa`](https://www.midpage.ai/dpa) | "an independent third-party SOC 2 Type II audit on at least an annual basis"; "audits conducted no less than annually" |
| [`trust.midpage.ai`](https://trust.midpage.ai/) | SOC 2 listed under Compliance. The SOC 2 Type II Report and HIPAA Auditor's Report are available on request |

No public surface states an observation period, a report date, or an expiry. The trust
center's document entries carry no report-period field and no dated update feed. So a
prospective enterprise customer cannot tell whether the report they are about to request
covers last quarter or covers a window that closed fourteen months ago.

That is a normal gap and a cheap one to close. Vanta trust centers support a dated
update post; one line — *"Our current SOC 2 Type II covers [period]; the next report is
expected [month]"* — removes the question from every future security review.

## The observation worth acting on: the security page's own date is stale

`/security` displays **"Last updated · April 2026"**. It is not.

Three Wayback snapshots — [12 May](http://web.archive.org/web/20260512071711/https://www.midpage.ai/security),
[14 May](http://web.archive.org/web/20260514045749/https://www.midpage.ai/security), and
[3 July 2026](http://web.archive.org/web/20260703170754/https://www.midpage.ai/security)
— all read "independently validated through **an annual SOC 2 Type II audit**." No
HIPAA. No auditor badges. No trust-center link.

The live page on 1 September 2026 reads "annual SOC 2 Type II **and HIPAA** audits,"
carries auditor badges, and links to the trust center — while still displaying "Last
updated · April 2026."

So the page was materially revised sometime after 3 July 2026, and the stamp was not
touched. The revision **added a compliance claim**, which is the category of change the
stamp exists to date.

This is small, free to fix, and it matters for a specific reason: a "last updated" stamp
is a control assertion. A reviewer who checks it against the Wayback Machine — which
takes about ninety seconds, and which diligence teams do — finds that the page's own
metadata is unreliable, and then reads every other assertion on it more skeptically. The
fix is one line in a CMS.

## Best inference on the cycle, with the reasoning shown

Two readings fit the public record. Neither is established; both are recorded so the
question can be asked directly rather than guessed at.

**Reading A — the window closes around January or February.** Midpage
[announced SOC 2 Type I in October 2023](http://web.archive.org/web/20240425145744/https://www.midpage.ai/blog/midpage-is-now-soc-2-type-i-certified).
A typical first Type II window runs about three months from there, and a "Type 2" page
was live by [3 March 2024](http://web.archive.org/web/20240303132837/https://www.midpage.ai/blog/midpage-is-now-soc-2-type-2-certified).
An annual anniversary then lands in January or February, which would put the next window
close in Q1 2027 and the current report going stale shortly after.

**Reading B — the window closes around May or June.** The trust center's own resource
description states a web application penetration test "conducted June 2–4, 2026." A
penetration test immediately before a window closes is a common sequence, and it is the
only dated audit-adjacent activity Midpage publishes. On its own it is weak evidence —
a pen test can sit anywhere in a year — but it is stated rather than inferred, which is
more than Reading A can say for its own anchor.

**Caveat on Reading A that matters:** the 2024 "Type 2" post carries the same body text
as the Type I post and the same displayed date. The title changed; the words did not.
That may be nothing more than a marketing edit, but it means the March 2024 page is weak
evidence for a Type II having actually been issued by then, and Reading A rests on it.

**What resolves it:** one question to `legal@midpage.ai`, or one line published on the
trust center. It is [open question 14](../00-governance/open-questions.md).

## Two dated facts that are stated, not inferred

Both come from the trust center's own resource descriptions:

- **Penetration test:** "Authenticated third-party assessment of app.midpage.ai
  conducted June 2–4, 2026."
- **Cyber liability insurance:** "coverage effective February 13, 2026 through February
  13, 2027."

The insurance renewal date is worth a calendar entry on its own. It is the one hard,
dated compliance deadline visible from outside, and it arrives before either candidate
audit window.

## A note on method

Nothing here rests on anything but rendered page text and archived copies of it. Vanta
trust centers expose more than they display — internal identifiers, ordering, timestamps
— and inferring dates from that machinery would have produced a tighter answer than the
one above. It is deliberately not used. A finding a company cannot reproduce by looking
at its own pages is a finding that has to be defended before it can be acted on, and
this repository is not worth reading if its author will reach for that.

## Sources

Every URL above is in the [public surface map](../00-governance/public-surface-map.md).
Nothing here characterises Midpage's auditor, and no finding on this page depends on
one.
