#!/usr/bin/env python3
"""Tests for check_metrics.py.

Control test: first-party surfaces stating the same value must produce zero findings.
Mutation guard: force every surface to compare — including the third-party one whose
definition differs — and the suite must go red, proving the exclusion is enforced by
code rather than by good intentions in a comment.

Run: python3 -m pytest test_check_metrics.py -q
"""

import copy
import datetime as _dt
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_metrics as m  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "metrics.yaml")


@pytest.fixture
def real():
    return m.load(REAL)


def _clean():
    """Two first-party surfaces agreeing. The control."""
    return {
        "schema_version": 1,
        "metrics": {
            "monthly-unique-visitors": {
                "label": "Monthly unique visitors",
                "definition_required": False,
            },
        },
        "surfaces": [
            {"id": "page-one", "url": "https://example.test/one", "party": "first",
             "audience": "marketing", "checked": "2026-09-01",
             "figures": [{"metric": "monthly-unique-visitors", "value": 150000,
                          "qualifier": "+", "quote": "150K+ monthly unique visitors"}]},
            {"id": "page-two", "url": "https://example.test/two", "party": "first",
             "audience": "marketing", "checked": "2026-09-01",
             "figures": [{"metric": "monthly-unique-visitors", "value": 150000,
                          "qualifier": "+", "quote": "150K+ monthly unique visitors"}]},
        ],
    }


# --------------------------------------------------------------------------
# Control and mutation guard
# --------------------------------------------------------------------------

def test_control_agreeing_surfaces_produce_no_findings():
    data = _clean()
    m.validate(data)
    assert m.find(data) == []


def test_mutation_guard_forcing_everything_to_compare_turns_this_suite_red(
        real, monkeypatch):
    """The Semrush row measures a different quantity and is excluded on purpose.
    Compare it anyway and extra findings appear — which is precisely the
    manufactured finding this tool refuses to make."""
    baseline = len([f for f in m.find(real)
                    if f["type"] == "DIVERGENT_FIRST_PARTY"])

    monkeypatch.setattr(m, "comparable", lambda _s: True)
    forced = len([f for f in m.find(real)
                  if f["type"] == "DIVERGENT_FIRST_PARTY"])
    assert forced > baseline, "the incomparable exclusion must be load-bearing"


# --------------------------------------------------------------------------
# The real observations
# --------------------------------------------------------------------------

def test_real_observations_validate(real):
    assert real["schema_version"] == 1


def test_the_two_first_party_figures_are_reported_as_divergent(real):
    hits = [f for f in m.find(real) if f["type"] == "DIVERGENT_FIRST_PARTY"]
    assert len(hits) == 1
    assert "200,000+" in hits[0]["detail"] and "150,000+" in hits[0]["detail"]


def test_the_third_party_figure_is_excluded_and_says_why(real):
    excluded = [s for s in real["surfaces"] if not m.comparable(s)]
    assert excluded, "the Semrush row must be present and excluded"
    for s in excluded:
        assert str(s.get("incomparable_because", "")).strip()


def test_definition_gap_is_reported(real):
    assert any(f["type"] == "DEFINITION_UNSTATED" for f in m.find(real))


def test_findings_are_deterministic(real):
    assert m.find(real) == m.find(m.load(REAL))


def test_every_figure_carries_a_quote(real):
    for s in real["surfaces"]:
        for f in s["figures"]:
            assert f["quote"].strip(), "%s/%s" % (s["id"], f["metric"])


def test_checked_dates_are_not_in_the_future(real):
    today = _dt.date.today()
    for s in real["surfaces"]:
        assert _dt.date.fromisoformat(str(s["checked"])) <= today, s["id"]


def test_spread_is_computed_off_the_smaller_figure(real):
    """200,000 against 150,000 is a 33% spread, not 25%. Reporting the smaller
    number would understate the gap in the company's own favour."""
    hit = [f for f in m.find(real) if f["type"] == "DIVERGENT_FIRST_PARTY"][0]
    assert "33% apart" in hit["detail"]


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("mutate, fragment", [
    (lambda d: d.update({"schema_version": 2}), "schema_version"),
    (lambda d: d.update({"metrics": {}}), "metrics registry"),
    (lambda d: d.update({"surfaces": d["surfaces"][:1]}), "at least two surfaces"),
    (lambda d: d["surfaces"][0].update({"id": "Page One"}), "lowercase slug"),
    (lambda d: d["surfaces"][0].update({"url": "http://example.test/one"}), "https://"),
    (lambda d: d["surfaces"][1].update({"id": "page-one"}), "duplicate surface id"),
    (lambda d: d["surfaces"][0].update({"party": "second"}), "party"),
    (lambda d: d["surfaces"][0].update({"checked": "2026/09/01"}), "ISO date"),
    (lambda d: d["surfaces"][0]["figures"][0].update({"metric": "ghost"}),
     "unknown metric"),
    (lambda d: d["surfaces"][0]["figures"][0].update({"value": -1}),
     "positive integer"),
    (lambda d: d["surfaces"][0]["figures"][0].update({"value": True}),
     "positive integer"),
    (lambda d: d["surfaces"][0]["figures"][0].update({"quote": " "}), "quote"),
])
def test_validation_rejects(mutate, fragment):
    data = _clean()
    mutate(data)
    with pytest.raises(m.DataError) as e:
        m.validate(data)
    assert fragment in str(e.value)


def test_silent_exclusion_is_rejected():
    """comparable:false without a reason is how a comparison quietly becomes
    whatever its author wanted it to be."""
    data = _clean()
    data["surfaces"].append({
        "id": "analyst", "url": "https://example.test/analyst", "party": "third",
        "audience": "analyst", "checked": "2026-09-01", "comparable": False,
        "figures": [{"metric": "monthly-unique-visitors", "value": 100000,
                     "qualifier": "", "quote": "100,000 visits"}],
    })
    with pytest.raises(m.DataError) as e:
        m.validate(data)
    assert "incomparable_because" in str(e.value)


def test_one_first_party_surface_is_not_a_comparison():
    data = _clean()
    data["surfaces"][1]["party"] = "third"
    data["surfaces"][1]["comparable"] = False
    data["surfaces"][1]["incomparable_because"] = "different definition"
    with pytest.raises(m.DataError) as e:
        m.validate(data)
    assert "two first-party surfaces" in str(e.value)


def test_yaml_boolean_value_does_not_read_as_one():
    parsed = yaml.safe_load("value: yes")
    assert parsed["value"] is True
    data = _clean()
    data["surfaces"][0]["figures"][0]["value"] = parsed["value"]
    with pytest.raises(m.DataError):
        m.validate(data)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_check_flag_validates(capsys):
    assert m.main(["--data", REAL, "--check"]) == 0
    assert "VALID" in capsys.readouterr().out


def test_strict_exits_two():
    assert m.main(["--data", REAL, "--strict"]) == 2


def test_default_run_exits_zero():
    assert m.main(["--data", REAL]) == 0


def test_invalid_data_exits_one(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("schema_version: 7\n", encoding="utf-8")
    assert m.main(["--data", str(bad)]) == 1


def test_render_shows_the_exclusion_and_its_reason(tmp_path, monkeypatch):
    out = tmp_path / "metric-findings.md"
    monkeypatch.setattr(m, "REPORT", str(out))
    assert m.main(["--data", REAL, "--render"]) == 0
    text = out.read_text(encoding="utf-8")
    assert "Excluded from the comparison" in text
    assert "semrush-via-crunchbase" in text


def test_loading_does_not_mutate_the_observations(real):
    snapshot = copy.deepcopy(real)
    m.find(real)
    assert real == snapshot
