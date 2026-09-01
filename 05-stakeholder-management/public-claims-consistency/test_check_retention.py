#!/usr/bin/env python3
"""Tests for check_retention.py.

Two of these matter more than the rest.

The CONTROL test feeds the checker a set of surfaces that agree, and requires zero
findings. Without it, a checker that returned a finding for every input would pass
every other test in this file.

The MUTATION GUARD gets a comparator gutted to always-pass and requires this suite to
go red. A test suite that stays green while the thing it tests has been disabled is
decoration. Run it and watch:

    python3 -c "import check_retention as c; c.INCOMPATIBLE = set()" ; \
        python3 -m pytest test_check_retention.py   # the guard fails

Run: python3 -m pytest test_check_retention.py -q
"""

import copy
import datetime as _dt
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_retention as c  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "retention-claims.yaml")


@pytest.fixture
def real():
    return c.load(REAL)


def _clean():
    """Surfaces that agree with each other. The control case."""
    return {
        "schema_version": 1,
        "paths": {
            "web-app": {"label": "Web application storage"},
            "model-providers": {"label": "Model providers"},
        },
        "surfaces": [
            {
                "id": "page-one", "url": "https://example.test/one",
                "audience": "marketing", "checked": "2026-09-01",
                "assertions": [
                    {"path": "web-app", "disposition": "bounded", "days": 60,
                     "quote": "deleted within 60 days"},
                    {"path": "model-providers", "disposition": "bounded", "days": 60,
                     "quote": "providers may retain up to 60 days"},
                ],
            },
            {
                "id": "page-two", "url": "https://example.test/two",
                "audience": "assurance", "checked": "2026-09-01",
                "assertions": [
                    {"path": "web-app", "disposition": "bounded", "days": 60,
                     "quote": "deleted within 60 days"},
                ],
            },
        ],
    }


# --------------------------------------------------------------------------
# Control
# --------------------------------------------------------------------------

def test_control_agreeing_surfaces_produce_no_findings():
    """If this ever fails, every other assertion in this file is worthless."""
    c.validate(_clean())
    assert c.find(_clean()) == []


# --------------------------------------------------------------------------
# Mutation guard
# --------------------------------------------------------------------------

def test_mutation_guard_gutting_the_comparator_turns_this_suite_red(real,
                                                                   monkeypatch):
    """Disable the incompatibility table and the contradiction must disappear.

    This is the test that proves the CONTRADICTION finding is produced by the
    comparator and not by a hard-coded string somewhere.
    """
    before = [f for f in c.find(real) if f["type"] == "CONTRADICTION"]
    assert before, "the real observations must contain a contradiction to guard"

    monkeypatch.setattr(c, "INCOMPATIBLE", set())
    after = [f for f in c.find(real) if f["type"] == "CONTRADICTION"]
    assert after == [], "gutting INCOMPATIBLE must remove the contradiction findings"


# --------------------------------------------------------------------------
# The real observations
# --------------------------------------------------------------------------

def test_real_observations_validate(real):
    assert real["schema_version"] == 1
    assert len(real["surfaces"]) >= 2


def test_zdr_versus_sixty_days_is_reported(real):
    hits = [f for f in c.find(real)
            if f["type"] == "CONTRADICTION" and f["path"] == "model-providers"]
    assert len(hits) == 1
    assert "zero" in hits[0]["detail"] and "60 days" in hits[0]["detail"]


def test_disclosed_dependency_is_not_a_finding(real):
    """The security page's plugin claim discloses the downstream dependency in the
    same sentence. That is the honest construction and must not be flagged."""
    gaps = [f for f in c.find(real) if f["type"] == "INHERITED_GAP"]
    assert all(f["path"] != "plugins" for f in gaps)


def test_undisclosed_dependency_is_a_finding(real):
    gaps = [f for f in c.find(real) if f["type"] == "INHERITED_GAP"]
    assert any(f["path"] == "mcp-server" for f in gaps)


def test_disclosure_flag_alone_flips_the_finding():
    """Same shape, one boolean apart. Isolates what the finding actually turns on."""
    data = _clean()
    data["surfaces"][1]["assertions"].append({
        "path": "model-providers", "disposition": "none",
        "depends_on": "model-providers", "discloses_dependency": False,
        "quote": "no retention",
    })
    # 'none' vs 'bounded' on the same path is also a contradiction; isolate the gap.
    gaps = [f for f in c.find(data) if f["type"] == "INHERITED_GAP"]
    assert len(gaps) == 1

    data["surfaces"][1]["assertions"][-1]["discloses_dependency"] = True
    gaps = [f for f in c.find(data) if f["type"] == "INHERITED_GAP"]
    assert gaps == []


def test_findings_are_deterministic(real):
    assert c.find(real) == c.find(c.load(REAL))


def test_every_assertion_carries_a_quote(real):
    for s in real["surfaces"]:
        for a in s["assertions"]:
            assert a["quote"].strip(), "%s/%s" % (s["id"], a["path"])


def test_checked_dates_are_not_in_the_future(real):
    today = _dt.date.today()
    for s in real["surfaces"]:
        assert _dt.date.fromisoformat(str(s["checked"])) <= today, s["id"]


# --------------------------------------------------------------------------
# Validation — the checker must refuse bad input rather than guess past it
# --------------------------------------------------------------------------

@pytest.mark.parametrize("mutate, fragment", [
    (lambda d: d.update({"schema_version": 2}), "schema_version"),
    (lambda d: d.update({"paths": {}}), "paths registry"),
    (lambda d: d.update({"surfaces": d["surfaces"][:1]}), "at least two surfaces"),
    (lambda d: d["surfaces"][0].update({"id": "Page One"}), "lowercase slug"),
    (lambda d: d["surfaces"][0].update({"url": "http://example.test/one"}), "https://"),
    (lambda d: d["surfaces"][1].update({"id": "page-one"}), "duplicate surface id"),
    (lambda d: d["surfaces"][0].update({"audience": "internal"}), "audience"),
    (lambda d: d["surfaces"][0].update({"checked": "01-09-2026"}), "ISO date"),
    (lambda d: d["surfaces"][0]["assertions"][0].update({"path": "nope"}),
     "unknown path"),
    (lambda d: d["surfaces"][0]["assertions"][0].update({"disposition": "maybe"}),
     "disposition"),
    (lambda d: d["surfaces"][0]["assertions"][0].update({"quote": "   "}), "quote"),
    (lambda d: d["surfaces"][0]["assertions"][0].pop("days"), "positive integer"),
    (lambda d: d["surfaces"][0]["assertions"][0].update({"days": True}),
     "positive integer"),
    (lambda d: d["surfaces"][0]["assertions"][0].update({"depends_on": "ghost"}),
     "unknown path"),
])
def test_validation_rejects(mutate, fragment):
    data = _clean()
    mutate(data)
    with pytest.raises(c.DataError) as e:
        c.validate(data)
    assert fragment in str(e.value)


def test_depends_on_without_an_explicit_disclosure_flag_is_rejected():
    data = _clean()
    data["surfaces"][0]["assertions"][1]["depends_on"] = "model-providers"
    with pytest.raises(c.DataError) as e:
        c.validate(data)
    assert "discloses_dependency" in str(e.value)


def test_yaml_boolean_days_does_not_read_as_one_day():
    """`days: yes` parses to True, and True == 1. A silent one-day retention period
    is exactly the kind of defect this repository exists to catch."""
    parsed = yaml.safe_load("days: yes")
    assert parsed["days"] is True
    data = _clean()
    data["surfaces"][0]["assertions"][0]["days"] = parsed["days"]
    with pytest.raises(c.DataError):
        c.validate(data)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_check_flag_validates_and_exits_zero(capsys):
    assert c.main(["--data", REAL, "--check"]) == 0
    assert "VALID" in capsys.readouterr().out


def test_strict_exits_two_when_there_are_findings():
    assert c.main(["--data", REAL, "--strict"]) == 2


def test_default_run_exits_zero_even_with_findings():
    assert c.main(["--data", REAL]) == 0


def test_invalid_data_exits_one(tmp_path, capsys):
    bad = tmp_path / "bad.yaml"
    bad.write_text("schema_version: 9\n", encoding="utf-8")
    assert c.main(["--data", str(bad)]) == 1
    assert "INVALID" in capsys.readouterr().out


def test_render_writes_every_finding(tmp_path, monkeypatch, real):
    out = tmp_path / "retention-findings.md"
    monkeypatch.setattr(c, "REPORT", str(out))
    assert c.main(["--data", REAL, "--render"]) == 0
    text = out.read_text(encoding="utf-8")
    for f in c.find(real):
        assert f["type"] in text
    for s in real["surfaces"]:
        assert s["url"] in text


def test_render_of_clean_data_says_so(tmp_path, monkeypatch):
    src = tmp_path / "clean.yaml"
    src.write_text(yaml.safe_dump(_clean()), encoding="utf-8")
    out = tmp_path / "out.md"
    monkeypatch.setattr(c, "REPORT", str(out))
    assert c.main(["--data", str(src), "--render"]) == 0
    assert "None." in out.read_text(encoding="utf-8")


def test_loading_does_not_mutate_the_observations(real):
    snapshot = copy.deepcopy(real)
    c.find(real)
    assert real == snapshot
