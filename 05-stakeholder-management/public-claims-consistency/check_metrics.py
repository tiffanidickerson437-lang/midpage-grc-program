#!/usr/bin/env python3
"""First-party traction metric consistency check (finding F3).

Two live Midpage marketing pages state two different figures for the same quantity.
The homepage says 200k+ unique monthly visitors read cases on Midpage; the legal-tech
data page says 150K+ monthly unique visitors to Midpage content. Both were live on
2026-09-01.

This is in a compliance repository, not a marketing one, for a specific reason. A
reviewer who catches a marketing page contradicting another marketing page starts
discounting every unattested number on the site — including the ones in the security
section, which are the numbers that cost money to be wrong about. Claims hygiene is a
revenue control before it is a taste question.

Two defect classes:

  DIVERGENT_FIRST_PARTY  two first-party surfaces state different values for the same
                         metric, with no reconciling definition
  DEFINITION_UNSTATED    a metric flagged as needing a definition is published without
                         a population, a window, or a measurement source

Third-party figures are recorded in the data file for context and are excluded from
the comparison by an explicit `comparable: false`. Semrush measures site visits;
Midpage's pages claim unique visitors who read cases. Those are different quantities,
and a tool that compared them anyway would be manufacturing a finding to look sharp.
The exclusion is enforced here rather than trusted to the reader.

Usage:
  python3 check_metrics.py            # report, exit 0
  python3 check_metrics.py --strict   # exit 2 on findings
  python3 check_metrics.py --check    # validate the data file only
  python3 check_metrics.py --render   # rewrite metric-findings.md
  python3 check_metrics.py --data PATH

Exit codes: 0 clean/reported | 1 invalid data | 2 findings under --strict.
No network call, no API key, no model in any code path.
"""

import argparse
import os
import sys

from _claims_common import (
    DataError,
    load_yaml,
    require_https_url,
    require_iso_date,
    require_lowercase_slug,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(HERE, "metrics.yaml")
REPORT = os.path.join(HERE, "metric-findings.md")

VALID_PARTY = {"first", "third"}
VALID_AUDIENCE = {"marketing", "analyst", "assurance", "legal"}


def load(path):
    data = load_yaml(path)
    validate(data)
    return data


def comparable(surface):
    return surface["party"] == "first" and surface.get("comparable") is not False


def validate(data):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise DataError("schema_version must be 1")

    metrics = data.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        raise DataError("metrics registry missing or empty")
    for mid, meta in metrics.items():
        if not isinstance(meta, dict) or not str(meta.get("label", "")).strip():
            raise DataError("metric %r: label missing" % mid)

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) < 2:
        raise DataError("need at least two surfaces to compare")

    seen = set()
    first_party = 0
    for s in surfaces:
        sid = s.get("id", "?")
        for field in ("id", "url", "party", "audience", "checked", "figures"):
            if not s.get(field):
                raise DataError("surface %r: %s missing" % (sid, field))
        require_lowercase_slug(s["id"])
        require_https_url(sid, s["url"])
        if s["id"] in seen:
            raise DataError("duplicate surface id %r" % sid)
        seen.add(s["id"])
        if s["party"] not in VALID_PARTY:
            raise DataError("surface %r: party must be one of %s"
                            % (sid, sorted(VALID_PARTY)))
        if s["audience"] not in VALID_AUDIENCE:
            raise DataError("surface %r: audience must be one of %s"
                            % (sid, sorted(VALID_AUDIENCE)))
        require_iso_date(sid, s["checked"])

        # comparable must be an actual boolean. A quoted "false" is truthy and would
        # silently bypass both this exclusion check and comparable() below.
        if "comparable" in s and not isinstance(s["comparable"], bool):
            raise DataError("surface %r: comparable must be a boolean" % sid)

        # An excluded surface must say why. Silent exclusions are how a comparison
        # quietly becomes whatever its author wanted it to be.
        if s.get("comparable") is False and \
                not str(s.get("incomparable_because", "")).strip():
            raise DataError("surface %r: comparable:false requires "
                            "incomparable_because" % sid)

        # Count surfaces that will actually be compared, not just party=='first' —
        # a first-party surface excluded via comparable:false must not count toward
        # the "we have a real comparison" gate below.
        if comparable(s):
            first_party += 1

        if not isinstance(s["figures"], list) or not s["figures"]:
            raise DataError("surface %r: figures must be a non-empty list" % sid)
        for f in s["figures"]:
            if not isinstance(f, dict):
                raise DataError("surface %r: figures must be mappings" % sid)
            if f.get("metric") not in metrics:
                raise DataError("surface %r: unknown metric %r" % (sid, f.get("metric")))
            v = f.get("value")
            # bool is an int subclass; a figure of `true` must not read as 1.
            if not isinstance(v, int) or isinstance(v, bool) or v <= 0:
                raise DataError("surface %r, metric %r: value must be a positive "
                                "integer" % (sid, f["metric"]))
            if not str(f.get("quote", "")).strip():
                raise DataError("surface %r, metric %r: quote missing"
                                % (sid, f["metric"]))

    if first_party < 2:
        raise DataError("need at least two first-party surfaces; the comparison this "
                        "tool makes is between what the company says and what the "
                        "company says elsewhere")


def find(data):
    """Return the findings. Deterministic: same observations, same output."""
    findings = []
    metrics = data["metrics"]

    by_metric = {}
    for s in data["surfaces"]:
        if not comparable(s):
            continue
        for f in s["figures"]:
            by_metric.setdefault(f["metric"], []).append((s, f))

    for mid in sorted(by_metric):
        entries = by_metric[mid]
        label = metrics[mid]["label"]

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                s1, f1 = entries[i]
                s2, f2 = entries[j]
                if f1["value"] == f2["value"]:
                    continue
                lo, hi = sorted((f1["value"], f2["value"]))
                spread = (hi - lo) / float(lo) * 100.0
                findings.append({
                    "type": "DIVERGENT_FIRST_PARTY",
                    "metric": mid,
                    "detail": "%s: %s states %s, %s states %s — %.0f%% apart, both "
                              "live on %s"
                              % (label, s1["id"], _fmt(f1), s2["id"], _fmt(f2),
                                 spread, s1["checked"]),
                })

        if metrics[mid].get("definition_required"):
            findings.append({
                "type": "DEFINITION_UNSTATED",
                "metric": mid,
                "detail": "%s is published on %s with no stated population, window, "
                          "or measurement source"
                          % (label, ", ".join(sorted(s["id"] for s, _ in entries))),
            })

    return findings


def _fmt(f):
    return "%s%s" % ("{:,}".format(f["value"]), f.get("qualifier") or "")


def render_report(data, findings):
    lines = [
        "# First-party metrics — findings (F3)",
        "",
        "Rendered by `check_metrics.py --render` from [`metrics.yaml`](metrics.yaml)."
        " Do not edit by hand — re-run the tool.",
        "",
        "## Figures observed",
        "",
        "| Surface | Party | Checked | Figure | Compared |",
        "|---|---|---|---|---|",
    ]
    for s in data["surfaces"]:
        for f in s["figures"]:
            lines.append("| [%s](%s) | %s | %s | %s | %s |"
                         % (s["id"], s["url"], s["party"], s["checked"], _fmt(f),
                            "yes" if comparable(s) else "no"))
    excluded = [s for s in data["surfaces"] if not comparable(s)]
    if excluded:
        lines += ["", "### Excluded from the comparison, and why", ""]
        for s in excluded:
            reason = str(s.get("incomparable_because")
                         or "third-party surface").strip().replace("\n", " ")
            lines.append("- **%s** — %s" % (s["id"], reason))
    lines += ["", "## Findings", ""]
    if not findings:
        lines.append("None. Every first-party surface states the same value for each"
                     " metric.")
    else:
        lines.append("| # | Type | Metric | Detail |")
        lines.append("|---|---|---|---|")
        for n, f in enumerate(findings, 1):
            lines.append("| %d | %s | %s | %s |"
                         % (n, f["type"], f["metric"], f["detail"]))
    lines += [
        "",
        "Neither figure is challenged here. Which one is right, and by what"
        " definition, is a question for whoever owns the claim.",
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
        n = sum(len(s["figures"]) for s in data["surfaces"])
        c = sum(1 for s in data["surfaces"] if comparable(s))
        print("VALID — %d surfaces (%d compared), %d figures."
              % (len(data["surfaces"]), c, n))
        return 0

    findings = find(data)

    if args.render:
        with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(data, findings))
        print("rendered %s (%d findings)" % (os.path.basename(REPORT), len(findings)))
        return 0

    c = sum(1 for s in data["surfaces"] if comparable(s))
    print("First-party metrics — %d of %d surfaces compared"
          % (c, len(data["surfaces"])))
    if not findings:
        print("  no findings: first-party surfaces agree.")
        return 0
    for f in findings:
        print("  [%-21s] %s" % (f["type"], f["detail"]))
    print("%d finding(s). Neither figure is challenged — only the disagreement."
          % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
