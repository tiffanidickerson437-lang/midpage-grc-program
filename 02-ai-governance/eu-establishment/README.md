# The EU establishment question (F4)

**The finding, in one sentence:** Midpage's public data-protection machinery is built
for a US company exporting personal data out of the EEA, and Midpage appears to have an
establishment inside it.

This is the finding in this repository with the largest gap between how quiet it looks
and how much it costs to get wrong.

## What is observable

Four public facts, none of which is contested:

1. **A Berlin location.** Midpage's LinkedIn company record lists two offices. The
   primary is New York, NY. The second is **Max-Urich Straße 3, 13355 Berlin,
   Germany**.
2. **An EU subprocessor.** Mistral AI, disclosed on both subprocessor surfaces as an AI
   service provider located in the European Union, scoped to "Web + Plugins" — that is,
   in the path that carries submitted queries.
3. **A European counterparty.** Midpage's own post of 27 July 2026 names **Noxtua**,
   a Berlin-based European legal-AI company, as one of the multibillion-dollar
   organisations relying on Midpage as a legal data supplier.
4. **A German founder.** The Form D signature block names Otto Zastrow Marcks as
   director and executive officer. The seed round's lead investor is not named on any
   public surface — Midpage's own reporting describes it only as "a major legal
   publishing house" — so it is not counted as a fact here.

## What is missing from the same surfaces

- No EU or German entity is named anywhere on the privacy policy, the DPA, the trust
  center, or the security page.
- No Article 27 representative is designated.
- No lead supervisory authority is identified.
- The DPA's transfer architecture — Standard Contractual Clauses, the UK Addendum,
  Swiss FADP terms — is the architecture of an **importer**: a US processor receiving
  personal data exported from the EEA.

## Why the gap matters

If the Berlin office is an establishment in the GDPR sense — and an office where
processing happens in the context of its activities generally is — then several things
that currently read as future problems are present-tense obligations:

**Article 3(1) attaches directly.** Processing in the context of the activities of an
establishment in the Union is caught regardless of where the data subjects are. That is
a different legal footing from Article 3(2) targeting, and it changes which authority
supervises and which obligations bite first.

**The one-stop-shop analysis is owed.** Article 56 lead supervisory authority
identification requires knowing where the main establishment is — where decisions about
purposes and means are actually taken. A company with a New York headquarters and a
Berlin office has to reach a documented answer. Not reaching one is not neutral; it
means every concerned supervisory authority can act locally.

**Transfers may be running the wrong direction on paper.** SCCs govern export from the
EEA. If a German establishment is a controller or joint establishment for some
processing, some flows may need a different instrument, and some may need none — but
the current documents describe only one shape.

**The AI Act's provider obligations follow establishment, not marketing.** A provider
placing a general-purpose-AI-based system on the Union market, with an establishment in
the Union, is squarely inside the Regulation's scope. Legal-analysis tooling sold into
administration-of-justice contexts also has a real Annex III argument to work through —
that argument may well come out the right way, but it has to be made and written down,
not assumed.

**Employment and works-council obligations exist too.** They are outside this
repository's scope and are named only so the list is not mistaken for a complete one.

## What this repository does not claim

It does **not** claim Midpage is non-compliant. Establishment is a factual and legal
question that turns on what the Berlin office actually does, and that is not observable
from a LinkedIn record. It is entirely possible there is a German entity with a
compliant posture that simply is not published.

That last sentence is the finding. **An enterprise buyer, a European data customer, or
a Series A diligence team cannot tell the difference between "handled and not
published" and "not handled" — and will assume the second.** For a company whose named
European counterparty is a sovereignty-positioned legal-AI vendor, that assumption is
expensive.

## What resolving it looks like

Roughly two weeks of work, most of it interviews and document review rather than
analysis:

1. Establish what the Berlin location is — entity, headcount, function, and whether
   processing decisions are taken there.
2. Reach a documented main-establishment and lead-supervisory-authority position, or
   document that Article 3(1) does not apply and why.
3. Designate an Article 27 representative, or record why one is not required.
4. Re-run the transfer analysis against the answer, and correct the DPA schedules if
   the direction of any flow has changed.
5. Scope the AI Act: provider or deployer, per surface; the Annex III argument, written
   down; the Article 50 transparency question for generated legal analysis.
6. Publish the outcome. The publication is not cosmetic — it is the control that stops
   this becoming a question again in every future diligence cycle.

## Sources

Every item above traces to the [public surface map](../../00-governance/public-surface-map.md).
Nothing in this section relies on non-public information.
