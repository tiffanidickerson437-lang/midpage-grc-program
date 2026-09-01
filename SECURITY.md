# Security policy

This repository ships compliance tooling. A defect in a checker here is not a normal
bug — a validator that silently stops validating reports "clean" forever after, and
anyone relying on it inherits that silence. Please report problems rather than filing
them as feature requests.

## Reporting a vulnerability

**Use GitHub's private vulnerability reporting** — the *Report a vulnerability* button
under the repository's Security tab. That opens a private advisory only maintainers can
see.

Please do not open a public issue for a security defect until it has been fixed.

If private reporting is unavailable to you, email **tiffanidickerson437@gmail.com**
with `SECURITY` in the subject line.

**What to expect:** an acknowledgement within 5 business days, an assessment within 10,
and credit in the advisory unless you ask otherwise. This is a personal project, not a
funded program — these are best-effort targets, stated as such rather than dressed up
as an SLA.

## What counts as a security issue here

Beyond the usual, these are specifically in scope because of what this repository is:

| Class | Why it matters |
|---|---|
| **A checker that passes invalid input** | The repository's claim rests on the checkers failing closed. A false negative is the highest-severity defect class here. |
| **A checker that can be neutered without turning its own suite red** | Every checker carries a mutation guard for exactly this reason. A gap in that guard is a real finding. |
| **A comparison that silently excludes a surface** | `check_metrics.py` refuses to load an excluded surface that does not say why it is excluded. Any route around that turns a comparison into whatever its author wanted. |
| **A path where an observation can drift without its date changing** | The observation files record what a page said, and when. Any route to editing a quote while keeping its `checked` date is a data-integrity defect. |
| **Dependency or workflow supply-chain issues** | Actions are pinned to full commit SHAs and `requirements.txt` is hash-pinned; a tag-based reference or an unhashed line slipping in is a finding. |

## What is out of scope

- **Anything about Midpage's actual security posture.** This repository contains no
  Midpage evidence, no credentials, no account data, and no non-public information. The
  author is a paying Midpage subscriber; every observation here comes from a page any
  member of the public can open. If you believe something in this repository reveals
  non-public information about Midpage, that is in scope and urgent — report it by the
  route above and it will be removed.
- **Findings that are simply out of date.** Live pages change. A report that a
  committed observation no longer matches the page is not a vulnerability; it is the
  expected reason to re-run the checkers and update the `checked` date.
- **Disagreement with a finding's conclusion.** The instruments report that public
  surfaces disagree with each other. They do not assert what is true. If you think a
  finding is wrong on the merits, open an issue — that is a discussion, not an
  advisory.
