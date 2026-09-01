#!/usr/bin/env python3
"""Retention claims consistency checker (finding F1).

Midpage tells its readers four things about how long a submitted query survives, on
four different public surfaces. The tool compares the observations committed in
retention-claims.yaml and reports every place two surfaces answer the same question
differently.

It never decides what Midpage's actual retention is. It cannot — that answer lives in
model-provider contracts nobody outside the company has read. It reports that the
public surfaces disagree, which is a fact about the pages, and routes it to the claim
owner. Nothing here edits a page or gates a deploy.

Four defect classes, each live on 2026-09-01:

  CONTRADICTION   two surfaces give incompatible dispositions for the same data path
                  ("Zero Day Retention required from every model provider we use"
                  against "Model providers may retain submitted queries for up to
                  60 days")
  INHERITED_GAP   a surface claims no retention on a path that rides on a downstream
                  path another surface bounds, without disclosing the dependency
                  (the hosted MCP server "has no data retention")
  PERIOD_ABSENT   the assurance surface addresses a path but states no period, while
                  other surfaces state one — the reader most likely to need the number
                  is the one least likely to find it
  BACKUP_CARVEOUT a bounded period whose own caveat has no horizon, so the stated
                  maximum is not in fact a maximum

A disclosed dependency is not a defect. The security page says plugin workflows "may
still share submitted queries with model providers" in the same sentence as its
no-storage claim; that is the honest construction, and the checker is built to tell it
apart from the marketing page's silent one. If it could not, its findings would be
pattern-matching rather than analysis.

Usage:
  python3 check_retention.py             # report findings, exit 0 (routes a human)
  python3 check_retention.py --strict    # exit 2 when there are findings (CI gating)
  python3 check_retention.py --check     # validate the observations only
  python3 check_retention.py --render    # rewrite retention-findings.md
  python3 check_retention.py --data PATH # run against a different observation file

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
DEFAULT_DATA = os.path.join(HERE, "retention-claims.yaml")
REPORT = os.path.join(HERE, "retention-findings.md")

VALID_DISPOSITIONS = {"zero", "none", "bounded", "stored", "unspecified"}
VALID_AUDIENCES = {"marketing", "assurance", "legal"}

# Which pairs of dispositions cannot both describe the same path. "zero" is a claim
# that nobody retains anything; "bounded" is a claim that somebody retains it for a
# stated period. Those are not two views of one fact.
INCOMPATIBLE = {
    frozenset({"zero", "bounded"}),
    frozenset({"zero", "stored"}),
    frozenset({"none", "bounded"}),
    frozenset({"none", "stored"}),
}


class DataError(ValueError):
    """The observation file is malformed. A checker that guesses past bad input is a
    checker whose findings cannot be trusted, so this always stops the run."""


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    validate(data)
    return data


def validate(data):
    if not isinstance(data, dict):
        raise DataError("root must be a mapping")
    if data.get("schema_version") != 1:
        raise DataError("schema_version must be 1")

    paths = data.get("paths")
    if not isinstance(paths, dict) or not paths:
        raise DataError("paths registry missing or empty")
    for pid, meta in paths.items():
        if not isinstance(meta, dict) or not str(meta.get("label", "")).strip():
            raise DataError("path %r: label missing" % pid)

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or len(surfaces) < 2:
        raise DataError("need at least two surfaces to compare")

    seen = set()
    for s in surfaces:
        if not isinstance(s, dict):
            raise DataError("surface entries must be mappings")
        sid = s.get("id", "?")
        for field in ("id", "url", "audience", "checked", "assertions"):
            if not s.get(field):
                raise DataError("surface %r: %s missing" % (sid, field))
        if not re.fullmatch(r"[a-z0-9-]+", str(s["id"])):
            raise DataError("surface id %r must be a lowercase slug — ids land "
                            "verbatim in rendered markdown" % sid)
        if not str(s["url"]).startswith("https://"):
            raise DataError("surface %r: url must be https:// — an observation of a "
                            "non-TLS page is not the observation this file claims, "
                            "and the url lands in a rendered markdown link" % sid)
        if s["id"] in seen:
            raise DataError("duplicate surface id %r" % sid)
        seen.add(s["id"])
        if s["audience"] not in VALID_AUDIENCES:
            raise DataError("surface %r: audience must be one of %s"
                            % (sid, sorted(VALID_AUDIENCES)))
        try:
            _dt.date.fromisoformat(str(s["checked"]))
        except ValueError:
            raise DataError("surface %r: checked is not an ISO date" % sid)

        if not isinstance(s["assertions"], list) or not s["assertions"]:
            raise DataError("surface %r: assertions must be a non-empty list" % sid)
        for a in s["assertions"]:
            if not isinstance(a, dict):
                raise DataError("surface %r: assertions must be mappings" % sid)
            if a.get("path") not in paths:
                raise DataError("surface %r: unknown path %r" % (sid, a.get("path")))
            if a.get("disposition") not in VALID_DISPOSITIONS:
                raise DataError("surface %r, path %r: disposition must be one of %s"
                                % (sid, a["path"], sorted(VALID_DISPOSITIONS)))
            if not str(a.get("quote", "")).strip():
                raise DataError("surface %r, path %r: quote missing — an observation "
                                "without the words that support it is a memory, not "
                                "an observation" % (sid, a["path"]))
            if a["disposition"] == "bounded":
                days = a.get("days")
                # bool is an int subclass; `days: yes` must not read as 1 day.
                if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
                    raise DataError("surface %r, path %r: bounded disposition needs a "
                                    "positive integer `days`" % (sid, a["path"]))
            if a.get("depends_on") is not None and a["depends_on"] not in paths:
                raise DataError("surface %r, path %r: depends_on names unknown path %r"
                                % (sid, a["path"], a["depends_on"]))
            if a.get("depends_on") is not None:
                if not isinstance(a.get("discloses_dependency"), bool):
                    raise DataError("surface %r, path %r: depends_on requires an "
                                    "explicit boolean discloses_dependency — the "
                                    "whole finding turns on it"
                                    % (sid, a["path"]))


def _assertions(data):
    """Flatten to (surface, assertion) pairs, in file order."""
    for s in data["surfaces"]:
        for a in s["assertions"]:
            yield s, a


def find(data):
    """Return the findings. Deterministic: same observations, same output."""
    findings = []
    labels = {pid: meta["label"] for pid, meta in data["paths"].items()}

    by_path = {}
    for s, a in _assertions(data):
        by_path.setdefault(a["path"], []).append((s, a))

    for path in sorted(by_path):
        entries = by_path[path]

        # CONTRADICTION — pairwise, deterministic order.
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                s1, a1 = entries[i]
                s2, a2 = entries[j]
                pair = frozenset({a1["disposition"], a2["disposition"]})
                if pair in INCOMPATIBLE:
                    findings.append({
                        "type": "CONTRADICTION",
                        "path": path,
                        "detail": "%s: %s asserts '%s'%s, %s asserts '%s'%s"
                                  % (labels[path],
                                     s1["id"], a1["disposition"], _period(a1),
                                     s2["id"], a2["disposition"], _period(a2)),
                    })

        # PERIOD_ABSENT — an assurance surface silent on a period others state.
        stated = [(s, a) for s, a in entries if a["disposition"] == "bounded"]
        for s, a in entries:
            if a["disposition"] == "unspecified" and stated and \
                    s["audience"] == "assurance":
                findings.append({
                    "type": "PERIOD_ABSENT",
                    "path": path,
                    "detail": "%s: %s is an assurance surface and states no period, "
                              "while %s state %s"
                              % (labels[path], s["id"],
                                 ", ".join(sorted(x["id"] for x, _ in stated)),
                                 ", ".join(sorted({"%d days" % b["days"]
                                                   for _, b in stated}))),
                })

    # INHERITED_GAP — a no-retention claim riding on a bounded downstream path,
    # without saying so.
    bounded_paths = {a["path"] for _, a in _assertions(data)
                     if a["disposition"] == "bounded"}
    for s, a in _assertions(data):
        dep = a.get("depends_on")
        if not dep or a["disposition"] not in ("zero", "none"):
            continue
        if dep in bounded_paths and not a.get("discloses_dependency"):
            holders = sorted({x["id"] for x, b in _assertions(data)
                              if b["path"] == dep and b["disposition"] == "bounded"})
            findings.append({
                "type": "INHERITED_GAP",
                "path": a["path"],
                "detail": "%s: %s claims '%s' on a path that depends on %s, which %s "
                          "bounds — and the surface does not say so"
                          % (labels[a["path"]], s["id"], a["disposition"],
                             labels[dep], ", ".join(holders)),
            })

    # BACKUP_CARVEOUT — a stated maximum with an unbounded exception attached.
    for s, a in _assertions(data):
        if a["disposition"] == "bounded" and str(a.get("caveat", "")).strip():
            findings.append({
                "type": "BACKUP_CARVEOUT",
                "path": a["path"],
                "detail": "%s: %s states %d days but carries an exception with no "
                          "stated horizon" % (labels[a["path"]], s["id"], a["days"]),
            })

    return findings


def _period(a):
    return " (%d days)" % a["days"] if a["disposition"] == "bounded" else ""


def render_report(data, findings):
    lines = [
        "# Retention claims — findings (F1)",
        "",
        "Rendered by `check_retention.py --render` from"
        " [`retention-claims.yaml`](retention-claims.yaml)."
        " Do not edit by hand — re-run the tool.",
        "",
        "Each row below describes disagreement between Midpage's own public surfaces."
        " None of it describes Midpage's actual retention, which is not observable"
        " from outside.",
        "",
        "## Surfaces compared",
        "",
        "| Surface | Audience | Checked | Paths addressed |",
        "|---|---|---|---|",
    ]
    for s in data["surfaces"]:
        paths = ", ".join(a["path"] for a in s["assertions"])
        lines.append("| [%s](%s) | %s | %s | %s |"
                     % (s["id"], s["url"], s["audience"], s["checked"], paths))
    lines += ["", "## Findings", ""]
    if not findings:
        lines.append("None. Every surface answers each path the same way.")
    else:
        lines.append("| # | Type | Path | Detail |")
        lines.append("|---|---|---|---|")
        for n, f in enumerate(findings, 1):
            lines.append("| %d | %s | %s | %s |"
                         % (n, f["type"], f["path"], f["detail"]))
    lines += [
        "",
        "The fix for every row is a decision by the claim owner, then a monitor —"
        " never a silent edit by a checker.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--check", action="store_true",
                    help="validate the observations and exit")
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 when there are findings")
    ap.add_argument("--render", action="store_true",
                    help="rewrite retention-findings.md")
    args = ap.parse_args(argv)

    try:
        data = load(args.data)
    except DataError as e:
        print("INVALID observations: %s" % e)
        return 1

    if args.check:
        n = sum(len(s["assertions"]) for s in data["surfaces"])
        print("VALID — %d surfaces, %d assertions, %d paths, every reference resolves."
              % (len(data["surfaces"]), n, len(data["paths"])))
        return 0

    findings = find(data)

    if args.render:
        with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(data, findings))
        print("rendered %s (%d findings)" % (os.path.basename(REPORT), len(findings)))
        return 0

    print("Retention claims — %d surfaces compared" % len(data["surfaces"]))
    if not findings:
        print("  no findings: every surface answers each path the same way.")
        return 0
    for f in findings:
        print("  [%-15s] %s" % (f["type"], f["detail"]))
    print("%d finding(s). Each routes to the claim owner — nothing here edits a page."
          % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
