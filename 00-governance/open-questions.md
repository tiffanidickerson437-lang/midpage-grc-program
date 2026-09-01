# Open questions

Things that cannot be answered from outside, ordered by how much the answer changes.
Each one is a question for a person, not a gap to be inferred past. An assessment that
guesses at these and presents the guesses as findings is worse than one that lists them.

---

**1. What is the Berlin office?**
Entity, headcount, function, and — the part that decides everything downstream —
whether decisions about the purposes and means of processing are taken there. Every
other question in [`02-ai-governance/eu-establishment/`](../02-ai-governance/eu-establishment/)
waits on this one.

**2. Which subprocessor list is authoritative?**
Eighteen providers on the list the DPA names, fifteen on the trust center. Pinecone,
Datadog, and Intercom appear only on the first. Either the trust center is stale, or
three vendors are listed contractually that are not in service. Both answers are fine;
not knowing which is not.

**3. Was advance notice given for Pinecone, Datadog, and Intercom?**
DPA §4.2 promises reasonable advance notice before a new subprocessor processes
customer personal data. Whether that promise was met for each of the three is a
records question with a yes-or-no answer.

**4. What does "Zero Day Retention" actually cover?**
Which providers, under which contract, on which endpoints, with what evidence. The
marketing page says every provider. The security page says up to sixty days. Both may
be true of different paths — but nobody outside can tell, and the reconciliation is a
document review, not an opinion.

**5. Does the hosted MCP server's "no data retention" claim survive the model hop?**
Midpage may retain nothing while the provider behind it retains for sixty days. If so,
the claim is true and incomplete, which is the most expensive kind of true.

**6. Where does PHI actually enter, and how far does it travel?**
The trust center discloses personal health information. On a litigation research
platform that presumably means medical records uploaded in personal injury, medical
malpractice, workers' compensation, and disability matters. The BAA question then runs
down the whole model-provider chain — and the answer determines whether the HIPAA
attestation covers what people assume it covers.

**7. What is the PCI scope?**
The trust center discloses credit card information; Stripe is a disclosed subprocessor.
That is very probably SAQ A, and probably a short memo. There is no published scoping
determination, so the short memo does not exist to hand anyone.

**8. What is the cross-customer deidentified insight feature, concretely?**
The privacy policy reserves the right to share deidentified activity data across
multiple customers' accounts to provide insights. For a platform holding privileged
legal research, the difference between aggregate usage counts and anything derived from
query content is the entire question — and outside counsel guidelines will ask it in
those words.

**9. Is the CCPA sale-or-sharing disclosure current?**
The privacy policy states that providing personal information to advertising partners,
analytics providers, and social networks may constitute a "sale" or "sharing." If that
is boilerplate that no longer describes practice, it is costing deals for nothing. If it
is accurate, it needs an opt-out surface and a mapped control.

**10. Which of the five multibillion-dollar data customers are under an enterprise
agreement with security terms?**
Two are public — Perplexity and Noxtua, per Midpage's own post. The security addenda
attached to those contracts, and the questionnaire load they generate, set the real
compliance calendar. Nothing about that is visible from outside.

**11. Is the SOC 2 scope the whole product?**
Web app, plugins, hosted MCP server, SQL read replica, and the public case-law pages are
five different surfaces. A Type II covering some of them is normal and fine — but the
scope boundary is what an enterprise reviewer needs and cannot currently see.

**12. What is the model-routing change process?**
Four model providers, an integration surface across three assistant platforms, and
public commitments that ride on provider contracts. Swapping a model touches the
no-training promise, the subprocessor list, the retention claim, and contract
representations at once. There is a designed answer in
[`03-secure-development/`](../03-secure-development/); whether it matches the real one
is question twelve.

**13. Who owns any of this today?**
No security, compliance, or privacy role appears in the org, and diligence routes to a
shared inbox. The honest possibility is that the answer is "the founder, between other
things," which at nine people is a reasonable place to have arrived at and an
unreasonable place to stay.
