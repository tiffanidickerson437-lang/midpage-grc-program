# Public surface map

Every claim in this repository traces to a row below. Each row is a page any member of
the public can open, with the date it was read. Nothing here comes from a Midpage
account, a support conversation, a document request, or any private channel.

Checked **1 September 2026** unless stated otherwise.

## Product and marketing

| Surface | URL | What it supplied |
|---|---|---|
| Homepage | `https://www.midpage.ai/` | Traction figures (200k+ unique monthly visitors, 10,000+ litigators, 300+ law firms, 5 multibillion-dollar data customers, 16M+ opinions); the four-platform integration story |
| Data for legal tech | `https://www.midpage.ai/data-for-legal-tech` | "Zero Day Retention required from every model provider we use"; "SOC 2 Type II certified, HIPAA audited"; the hosted MCP server's "no data retention"; 150K+ monthly unique visitors; 200K+ weekly API and MCP calls |
| Documentation | `https://docs.midpage.ai/` | Three data-access interfaces (SQL read replica, MCP, REST API); 300+ home-built scrapers running six times daily; schema, citator, and format pages — and the absence of any end-user documentation |
| Blog | `https://www.midpage.ai/blog` | 41 posts across Product Updates (9), Legal Analysis (7), Tutorials (16), Company News (6); the release history, and the absence of a changelog surface |
| Sitemap | `https://www.midpage.ai/sitemap.xml` | Confirmed the absence of `/changelog` and of any end-user docs route; confirmed `updates.midpage.ai` and `blog.midpage.ai` both resolve to `/blog` |
| Jobs | `https://www.midpage.ai/jobs` | Points to Wellfound; no security, compliance, privacy, or GRC role open |

## Assurance and legal

| Surface | URL | What it supplied |
|---|---|---|
| Security overview | `https://www.midpage.ai/security` | "Model providers may retain submitted queries for up to 60 days"; the no-training commitments; the control inventory; page self-dated April 2026 |
| Trust center | `https://trust.midpage.ai/` | Vanta-powered; SOC 2 badge; data collected (customer PII, credit card information, personal health information); control counts; three visible data-and-privacy controls, none stating a period |
| Trust center subprocessors | `https://trust.midpage.ai/subprocessors` | The 15-provider assurance list |
| Subprocessors | `https://www.midpage.ai/subprocessors` | The 18-provider list the DPA names; page self-dated 10 June 2026 |
| Data Processing Addendum | `https://www.midpage.ai/dpa` | Effective 28 April 2026; §4.2 advance-notice commitment and the subprocessor list URL; SCC, UK Addendum, and Swiss FADP definitions; controller/processor roles |
| Privacy policy | `https://www.midpage.ai/privacy-policy` | 60-day post-termination deletion with a backup carve-out; the CCPA sale/sharing disclosure; cross-customer deidentified insights; the `midpage.ai/subprocessors` URL; registered contact address at 190 Bowery, New York, NY 10012 |

## Corporate record

| Surface | URL | What it supplied |
|---|---|---|
| SEC EDGAR — CIK 0002067400 | `https://data.sec.gov/submissions/CIK0002067400.json` | Legal name Midpage AI Inc.; Delaware; one filing on record — Form D, 28 May 2025, accession 0002067400-25-000001 |
| Form D primary document | `https://www.sec.gov/Archives/edgar/data/2067400/000206740025000001/xslFormDX01/primary_doc.xml` | $6,443,350 sold, equity only, Rule 506(b); Wilmington DE address; Otto Zastrow Marcks as director and executive officer |
| LinkedIn company record | `https://www.linkedin.com/company/midpage` | Employee count 9; two office locations — New York, NY and Max-Urich Straße 3, 13355 Berlin, Germany; the 27 July 2026 post naming Perplexity and Noxtua among the data customers |
| Crunchbase | `https://www.crunchbase.com/organization/midpage-ai` | Semrush-sourced monthly web visits (102,768, +86.99% MoM); funding round of $6.4M dated 28 June 2025 |

## What is deliberately not here

- **No Midpage account data.** The author holds a paid Midpage subscription. Nothing
  observed inside the product, in a support conversation, or in any account-gated
  surface appears anywhere in this repository. That boundary is the reason the findings
  below can be re-run by anyone.
- **No auditor commentary.** Midpage's auditor is named on their security page. This
  repository takes no position on any audit firm, and does not repeat market
  allegations about firms in this sector. None of the findings need it.
- **No requested documents.** The trust center gates the SOC 2 Type II report and the
  HIPAA auditor's report behind a request form. Neither was requested, and neither
  informs anything here.

## Re-checking

Live pages change without notice, and a finding that was true in September and asserted
in November is not a finding. Every observation carries a `checked` date in its
observation file, and the instruments exist so an observation can be **re-run** rather
than remembered:

```bash
python3 05-stakeholder-management/public-claims-consistency/check_retention.py
python3 05-stakeholder-management/public-claims-consistency/subprocessor_consistency.py
python3 05-stakeholder-management/public-claims-consistency/check_metrics.py
```

If a page has moved on, the correct action is to re-observe it and update the entry
with a new `checked` date — never to edit a quote so it still supports the finding.
