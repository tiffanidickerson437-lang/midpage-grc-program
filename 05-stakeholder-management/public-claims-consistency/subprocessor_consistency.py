#!/usr/bin/env python3
"""Subprocessor disclosure consistency check (finding F2).

Midpage discloses its subprocessors in two public places. Section 4.2 of the Data
Processing Addendum names one of them by URL as the list, and attaches a contractual
promise to it: reasonable advance notice before any new subprocessor processes
customer personal data. The other is the Vanta-powered trust center — the surface an
enterprise reviewer or an auditor actually opens.

The tool compares the observations committed in subprocessors.yaml and reports every
provider that appears on one surface and not the other. It reports divergence between
Midpage's own disclosures; it cannot say which list is right. That the contractual
list is the longer one is what makes the direction of the gap worth a human's
attention, so the tool reports direction explicitly.

Two defect classes, both live on 2026-09-01:

  UNDISCLOSED   a provider on the contractual list, absent from the assurance surface
  UNCOMMITTED   a provider on the assurance surface, absent from the contractual list

Names are compared after alias resolution and case folding, so "Neon" and "NeonDB"
are one provider. Spelling drift between two pages is a documentation defect worth
noticing, but it is not a missing vendor, and a checker that conflated the two would
inflate its own findings.

Usage:
  python3 subprocessor_consistency.py            # report, exit 0
  python3 subprocessor_consistency.py --strict   # exit 2 on findings
  python3 subprocessor_consistency.py --check    # validate the data file only
  python3 subprocessor_consistency.py --render   # rewrite subprocessor-findings.md
  python3 subprocessor_consistency.py --data PATH

Exit codes: 0 clean/reported | 1 invalid data | 2 findings under --strict.
No network call, no API key, no model in any code path.
"""

import argparse
import datetime as _dt
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(HERE, "subprocessors.yaml")
REPORT = os.path.join(HERE, "subprocessor-findings.md")

VALID_AUTHORITY = {"contractual", "assurance"}


class DataError(ValueError):
    pass


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    validate(data)
    return data


def validate(data):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise DataError("schema_version must be 1")
    if not str(data.get("tier", "")).strip():
        raise DataError("tier missing — a comparison without a scope is unfalsifiable")

    commitment = data.get("commitment")
    if not isinstance(commitment, dict):
        raise DataError("commitment block missing — the DPA clause is what makes this "
                        "a finding rather than a typo")
    for field in ("source", "effective", "clause", "quote"):
        if not str(commitment.get(field, "")).strip():
            raise DataError("commitment: %s missing" % field)
    try:
        _dt.date.fromisoformat(str(commitment["effective"]))
    except ValueError:
        raise DataError("commitment: effective is not an ISO date")

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) != 2:
        raise DataError("exactly two surfaces are compared; got %r"
                        % (len(surfaces) if isinstance(surfaces, list) else surfaces))

    seen_ids, seen_authority = set(), set()
    for s in surfaces:
        sid = s.get("id", "?")
        for field in ("id", "url", "checked", "authority", "note", "providers"):
            if not s.get(field):
                raise DataError("surface %r: %s missing" % (sid, field))
        if not re.fullmatch(r"[a-z0-9-]+", str(s["id"])):
            raise DataError("surface id %r must be a lowercase slug" % sid)
        if not str(s["url"]).startswith("https://"):
            raise DataError("surface %r: url must be https://" % sid)
        if s["id"] in seen_ids:
            raise DataError("duplicate surface id %r" % sid)
        seen_ids.add(s["id"])
        if s["authority"] not in VALID_AUTHORITY:
            raise DataError("surface %r: authority must be one of %s"
                            % (sid, sorted(VALID_AUTHORITY)))
        if s["authority"] in seen_authority:
            raise DataError("two surfaces share authority %r — the comparison only "
                            "means something across a contractual/assurance pair"
                            % s["authority"])
        seen_authority.add(s["authority"])
        try:
            _dt.date.fromisoformat(str(s["checked"]))
        except ValueError:
            raise DataError("surface %r: checked is not an ISO date" % sid)
        if not isinstance(s["providers"], list) or not s["providers"]:
            raise DataError("surface %r: providers must be a non-empty list" % sid)
        normalised = []
        for p in s["providers"]:
            # YAML turns bare `on`/`no` into booleans; a provider name is a string.
            if not isinstance(p, str) or not p.strip():
                raise DataError("surface %r: provider %r is not a non-empty string"
                                % (sid, p))
            key = canonical(p, data)
            if key in normalised:
                raise DataError("surface %r: %r appears twice after alias resolution"
                                % (sid, p))
            normalised.append(key)

    aliases = data.get("aliases") or {}
    if not isinstance(aliases, dict):
        raise DataError("aliases must be a mapping")
    for k, v in aliases.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise DataError("alias %r -> %r: both sides must be strings" % (k, v))


def canonical(name, data):
    """Fold a page's spelling to a comparison key."""
    key = re.sub(r"\s+", " ", str(name)).strip().lower()
    aliases = {str(k).strip().lower(): str(v).strip().lower()
               for k, v in (data.get("aliases") or {}).items()}
    return aliases.get(key, key)


def _display(data, surface, key):
    """The page's own spelling for a canonical key, for reporting."""
    for p in surface["providers"]:
        if canonical(p, data) == key:
            return p
    return key


def find(data):
    """Return the findings. Deterministic: same observations, same output."""
    by_authority = {s["authority"]: s for s in data["surfaces"]}
    contractual = by_authority["contractual"]
    assurance = by_authority["assurance"]

    c_keys = {canonical(p, data) for p in contractual["providers"]}
    a_keys = {canonical(p, data) for p in assurance["providers"]}

    findings = []
    for key in sorted(c_keys - a_keys):
        findings.append({
            "type": "UNDISCLOSED",
            "provider": _display(data, contractual, key),
            "detail": "%s is on the contractual list (%s) and absent from the "
                      "assurance surface (%s)"
                      % (_display(data, contractual, key),
                         contractual["id"], assurance["id"]),
        })
    for key in sorted(a_keys - c_keys):
        findings.append({
            "type": "UNCOMMITTED",
            "provider": _display(data, assurance, key),
            "detail": "%s is on the assurance surface (%s) and absent from the "
                      "contractual list (%s), which the DPA names as the list"
                      % (_display(data, assurance, key),
                         assurance["id"], contractual["id"]),
        })
    return findings


def render_report(data, findings):
    by_authority = {s["authority"]: s for s in data["surfaces"]}
    c, a = by_authority["contractual"], by_authority["assurance"]
    lines = [
        "# Subprocessor disclosure — findings (F2)",
        "",
        "Rendered by `subprocessor_consistency.py --render` from"
        " [`subprocessors.yaml`](subprocessors.yaml)."
        " Do not edit by hand — re-run the tool.",
        "",
        "## The commitment",
        "",
        "> %s" % data["commitment"]["quote"].strip().replace("\n", " "),
        "",
        "DPA section %s, effective %s. That clause is what makes the rows below a"
        " question about a promise rather than a question about tidiness."
        % (data["commitment"]["clause"], data["commitment"]["effective"]),
        "",
        "## Surfaces compared",
        "",
        "| Surface | Authority | Checked | Providers listed |",
        "|---|---|---|---|",
        "| [%s](%s) | %s | %s | %d |" % (c["id"], c["url"], c["authority"],
                                          c["checked"], len(c["providers"])),
        "| [%s](%s) | %s | %s | %d |" % (a["id"], a["url"], a["authority"],
                                          a["checked"], len(a["providers"])),
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("None. Both surfaces disclose the same set after alias"
                     " resolution.")
    else:
        lines.append("| # | Type | Provider | Detail |")
        lines.append("|---|---|---|---|")
        for n, f in enumerate(findings, 1):
            lines.append("| %d | %s | %s | %s |"
                         % (n, f["type"], f["provider"], f["detail"]))
    lines += [
        "",
        "Which list is correct is not observable from outside. Reconciling them, and"
        " deciding whether the advance-notice promise was met for each provider, is"
        " work for someone inside.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--render", action="store_true")
    args = ap.parse_args(argv)

    try:
        data = load(args.data)
    except DataError as e:
        print("INVALID data: %s" % e)
        return 1

    if args.check:
        counts = ", ".join("%s=%d" % (s["id"], len(s["providers"]))
                           for s in data["surfaces"])
        print("VALID — 2 surfaces (%s), tier %r." % (counts, data["tier"]))
        return 0

    findings = find(data)

    if args.render:
        with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(data, findings))
        print("rendered %s (%d findings)" % (os.path.basename(REPORT), len(findings)))
        return 0

    counts = " vs ".join("%s %d" % (s["id"], len(s["providers"]))
                         for s in data["surfaces"])
    print("Subprocessor disclosure — %s" % counts)
    if not findings:
        print("  no findings: both surfaces disclose the same set.")
        return 0
    for f in findings:
        print("  [%-12s] %s" % (f["type"], f["detail"]))
    print("%d finding(s). Which list is right is a question for someone inside."
          % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
