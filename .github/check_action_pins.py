#!/usr/bin/env python3
"""Every GitHub Action in this repository must be pinned to a full commit SHA.

SECURITY.md states this as a control: "Actions are pinned to full commit SHAs; a
tag-based reference slipping in is a finding." A stated control with nothing enforcing
it is the exact defect this repository exists to point at, so this enforces it.

A tag is a mutable pointer. `actions/checkout@v7` resolves to whatever the tag points
at today, which means a compromised or re-pointed tag executes in a workflow that has
`contents: read` and, for CodeQL, `security-events: write`. A 40-character commit SHA
is immutable. That is the whole argument, and it is why Dependabot is configured for
the github-actions ecosystem: pinning is the control, and the cost of the control is
that nothing updates unless something updates it.

Three defect classes:

  UNPINNED     a `uses:` reference that is not a 40-hex commit SHA (a tag, a branch,
               or a partial SHA)
  UNLABELLED   pinned correctly, but with no trailing `# vX.Y.Z` comment — a reviewer
               cannot tell what version a bare SHA is without leaving the diff
  UNRESOLVED   a `uses:` line this checker could not parse at all, which is treated as
               a failure rather than skipped

Usage:
  python3 .github/check_action_pins.py            # report, exit 0
  python3 .github/check_action_pins.py --strict   # exit 2 on findings (CI gating)
  python3 .github/check_action_pins.py --dir PATH

Exit codes: 0 clean/reported | 1 no workflows found | 2 findings under --strict.
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.join(HERE, "workflows")

# `uses:` value, then optionally whitespace and a trailing comment.
USES = re.compile(r"^\s*-?\s*uses:\s*(?P<ref>\S+)\s*(?P<comment>#.*)?$")
SHA = re.compile(r"^[0-9a-f]{40}$")
VERSION_COMMENT = re.compile(r"#\s*v?\d+(\.\d+)*", re.I)


def workflow_files(directory):
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, n)
        for n in os.listdir(directory)
        if n.endswith((".yml", ".yaml"))
    )


def scan_text(text, name):
    """Return findings for one workflow file. Pure: no I/O, so it is testable."""
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = USES.match(line)
        if not m:
            continue
        ref = m.group("ref").strip("\"'")
        comment = m.group("comment") or ""

        # A local composite action lives in this repository and is covered by the same
        # review as everything else here. There is no third party to pin.
        if ref.startswith("./"):
            continue

        # docker://image@sha256:... is a different pinning scheme; require a digest.
        if ref.startswith("docker://"):
            if "@sha256:" not in ref:
                findings.append({
                    "type": "UNPINNED", "file": name, "line": lineno, "ref": ref,
                    "detail": "container action without an @sha256: digest",
                })
            continue

        if "@" not in ref:
            findings.append({
                "type": "UNRESOLVED", "file": name, "line": lineno, "ref": ref,
                "detail": "no @ref at all — cannot tell what this resolves to",
            })
            continue

        version = ref.rsplit("@", 1)[1]
        if not SHA.match(version):
            findings.append({
                "type": "UNPINNED", "file": name, "line": lineno, "ref": ref,
                "detail": "pinned to %r, which is mutable; use a full 40-character "
                          "commit SHA" % version,
            })
            continue

        if not VERSION_COMMENT.search(comment):
            findings.append({
                "type": "UNLABELLED", "file": name, "line": lineno, "ref": ref,
                "detail": "pinned correctly but carries no `# vX.Y.Z` comment — a "
                          "reviewer cannot read a bare SHA",
            })

    return findings


def scan_dir(directory):
    files = workflow_files(directory)
    findings = []
    for path in files:
        with open(path, encoding="utf-8") as fh:
            findings.extend(scan_text(fh.read(), os.path.basename(path)))
    return files, findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", default=DEFAULT_DIR)
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 when there are findings")
    args = ap.parse_args(argv)

    files, findings = scan_dir(args.dir)

    if not files:
        print("NO WORKFLOWS FOUND in %s — this check cannot pass vacuously."
              % args.dir)
        return 1

    print("Action pinning — %d workflow file(s) scanned" % len(files))
    if not findings:
        print("  every `uses:` is pinned to a full commit SHA and labelled.")
        return 0
    for f in findings:
        print("  [%-10s] %s:%d  %s — %s"
              % (f["type"], f["file"], f["line"], f["ref"], f["detail"]))
    print("%d finding(s)." % len(findings))
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
