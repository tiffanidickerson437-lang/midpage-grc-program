#!/usr/bin/env python3
"""Tests for check_action_pins.py.

Same standard as every other checker here: a control test (clean input must produce
zero findings) and a mutation guard (gut the comparator and this suite must go red).

There is also a live test asserting that this repository's own workflows pass. That
one is the point of the whole file — a control that is stated in SECURITY.md and
enforced nowhere is the defect this repository was built to point at.

Run: python3 -m pytest .github/test_check_action_pins.py -q
"""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_action_pins as p  # noqa: E402

WORKFLOWS = os.path.join(HERE, "workflows")

CLEAN = """
jobs:
  test:
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
"""


# --------------------------------------------------------------------------
# Control and mutation guard
# --------------------------------------------------------------------------

def test_control_properly_pinned_workflow_produces_no_findings():
    assert p.scan_text(CLEAN, "clean.yml") == []


def test_mutation_guard_gutting_the_sha_pattern_turns_this_suite_red(monkeypatch):
    """Loosen the SHA test to match anything and the tag finding must disappear.

    If this passes with the pattern gutted, the check is decorative."""
    tagged = "      - uses: actions/checkout@v7\n"
    assert [f["type"] for f in p.scan_text(tagged, "w.yml")] == ["UNPINNED"]

    import re
    monkeypatch.setattr(p, "SHA", re.compile(r".*"))
    monkeypatch.setattr(p, "VERSION_COMMENT", re.compile(r".*"))
    assert p.scan_text(tagged, "w.yml") == [], "the SHA pattern must be load-bearing"


# --------------------------------------------------------------------------
# This repository's own workflows
# --------------------------------------------------------------------------

def test_this_repository_pins_every_action():
    files, findings = p.scan_dir(WORKFLOWS)
    assert files, "no workflow files found — this check must not pass vacuously"
    assert findings == [], "\n".join(
        "%s:%d %s — %s" % (f["file"], f["line"], f["ref"], f["detail"])
        for f in findings
    )


def test_this_repository_has_more_than_one_workflow():
    """Guards against a future edit that deletes workflows and leaves a green check."""
    assert len(p.workflow_files(WORKFLOWS)) >= 2


# --------------------------------------------------------------------------
# Defect classes
# --------------------------------------------------------------------------

@pytest.mark.parametrize("line, expected", [
    ("      - uses: actions/checkout@v7", "UNPINNED"),
    ("      - uses: actions/checkout@main", "UNPINNED"),
    ("      - uses: actions/checkout@3d3c42e", "UNPINNED"),
    ("      - uses: actions/checkout", "UNRESOLVED"),
    ("      - uses: docker://alpine:3.20", "UNPINNED"),
])
def test_defect_classes(line, expected):
    findings = p.scan_text(line + "\n", "w.yml")
    assert [f["type"] for f in findings] == [expected]


def test_pinned_but_unlabelled_is_reported():
    line = "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
    assert [f["type"] for f in p.scan_text(line, "w.yml")] == ["UNLABELLED"]


def test_local_action_is_not_a_third_party_to_pin():
    assert p.scan_text("      - uses: ./.github/actions/thing\n", "w.yml") == []


def test_container_action_with_a_digest_passes():
    line = "      - uses: docker://alpine@sha256:" + "a" * 64 + "\n"
    assert p.scan_text(line, "w.yml") == []


def test_quoted_reference_is_parsed():
    line = '      - uses: "actions/checkout@v7"\n'
    assert [f["type"] for f in p.scan_text(line, "w.yml")] == ["UNPINNED"]


def test_uppercase_sha_is_not_accepted():
    """Git object names are lowercase hex. An uppercase string is not a SHA, and
    accepting one would mean the pattern is looser than it looks."""
    line = "      - uses: actions/checkout@" + "A" * 40 + " # v7\n"
    assert [f["type"] for f in p.scan_text(line, "w.yml")] == ["UNPINNED"]


def test_line_numbers_are_reported():
    text = "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@v7\n"
    assert p.scan_text(text, "w.yml")[0]["line"] == 4


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_strict_exits_zero_on_this_repository():
    assert p.main(["--dir", WORKFLOWS, "--strict"]) == 0


def test_missing_directory_exits_one_rather_than_passing_vacuously(tmp_path, capsys):
    assert p.main(["--dir", str(tmp_path / "nope"), "--strict"]) == 1
    assert "NO WORKFLOWS FOUND" in capsys.readouterr().out


def test_strict_exits_two_on_a_bad_workflow(tmp_path):
    d = tmp_path / "workflows"
    d.mkdir()
    (d / "bad.yml").write_text("      - uses: actions/checkout@v7\n", encoding="utf-8")
    assert p.main(["--dir", str(d), "--strict"]) == 2


def test_default_run_exits_zero_even_with_findings(tmp_path):
    d = tmp_path / "workflows"
    d.mkdir()
    (d / "bad.yml").write_text("      - uses: actions/checkout@v7\n", encoding="utf-8")
    assert p.main(["--dir", str(d)]) == 0
