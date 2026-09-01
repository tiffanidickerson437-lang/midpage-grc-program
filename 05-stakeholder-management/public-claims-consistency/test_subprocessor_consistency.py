#!/usr/bin/env python3
"""Tests for subprocessor_consistency.py.

Control test: two surfaces listing the same providers must produce zero findings.
Mutation guard: gut the alias map and the suite goes red, proving the alias
resolution is load-bearing rather than ornamental.

Run: python3 -m pytest test_subprocessor_consistency.py -q
"""

import copy
import datetime as _dt
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import subprocessor_consistency as s  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "subprocessors.yaml")


@pytest.fixture
def real():
    return s.load(REAL)


def _clean():
    """Two surfaces disclosing the same set, spelled differently. The control."""
    return {
        "schema_version": 1,
        "tier": "all disclosed subprocessors",
        "commitment": {
            "source": "https://example.test/dpa",
            "effective": "2026-04-28",
            "clause": "4.2",
            "quote": "Midpage maintains a list of its Sub-processors at ...",
        },
        "aliases": {"neondb": "neon"},
        "surfaces": [
            {"id": "dpa-list", "url": "https://example.test/subprocessors",
             "checked": "2026-09-01", "authority": "contractual",
             "note": "the list the DPA points at",
             "providers": ["OpenAI", "NeonDB", "Vercel"]},
            {"id": "trust-center", "url": "https://trust.example.test/subprocessors",
             "checked": "2026-09-01", "authority": "assurance",
             "note": "the Vanta panel",
             "providers": ["Neon", "openai", "Vercel"]},
        ],
    }


# --------------------------------------------------------------------------
# Control and mutation guard
# --------------------------------------------------------------------------

def test_control_matching_surfaces_produce_no_findings():
    data = _clean()
    s.validate(data)
    assert s.find(data) == []


def test_mutation_guard_gutting_alias_resolution_turns_this_suite_red(monkeypatch):
    """With aliases disabled, NeonDB and Neon read as two different vendors and the
    control case starts producing phantom findings. If this passes with the alias
    map removed, alias resolution is doing nothing."""
    data = _clean()
    assert s.find(data) == []

    monkeypatch.setattr(s, "canonical", lambda name, _d: str(name).strip().lower())
    assert s.find(data) != [], "alias resolution must be load-bearing"


# --------------------------------------------------------------------------
# The real observations
# --------------------------------------------------------------------------

def test_real_observations_validate(real):
    assert len(real["surfaces"]) == 2


def test_the_three_undisclosed_providers_are_reported(real):
    names = {f["provider"] for f in s.find(real) if f["type"] == "UNDISCLOSED"}
    assert names == {"Pinecone", "Datadog", "Intercom"}


def test_nothing_is_uncommitted(real):
    """Everything on the trust center is also on the contractual list. If that ever
    stops being true, the gap has changed direction and the finding must be re-read
    before it is asserted anywhere."""
    assert [f for f in s.find(real) if f["type"] == "UNCOMMITTED"] == []


def test_spelling_drift_is_not_a_missing_vendor(real):
    """'Neon'/'NeonDB', 'Cohere'/'Cohere API', 'Mistral'/'Mistral AI', 'prefect'/
    'Prefect' appear with different spellings across the two pages and must not
    inflate the finding count."""
    names = {f["provider"].lower() for f in s.find(real)}
    for drifted in ("neon", "neondb", "cohere", "cohere api",
                    "mistral", "mistral ai", "prefect"):
        assert drifted not in names


def test_findings_are_deterministic(real):
    assert s.find(real) == s.find(s.load(REAL))


def test_commitment_predates_the_observation(real):
    eff = _dt.date.fromisoformat(str(real["commitment"]["effective"]))
    for surf in real["surfaces"]:
        assert eff <= _dt.date.fromisoformat(str(surf["checked"]))


def test_checked_dates_are_not_in_the_future(real):
    today = _dt.date.today()
    for surf in real["surfaces"]:
        assert _dt.date.fromisoformat(str(surf["checked"])) <= today, surf["id"]


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("mutate, fragment", [
    (lambda d: d.update({"schema_version": 2}), "schema_version"),
    (lambda d: d.update({"tier": "  "}), "tier missing"),
    (lambda d: d.pop("commitment"), "commitment block"),
    (lambda d: d["commitment"].update({"clause": ""}), "clause"),
    (lambda d: d["commitment"].update({"effective": "28-04-2026"}), "ISO date"),
    (lambda d: d.update({"surfaces": d["surfaces"][:1]}), "exactly two surfaces"),
    (lambda d: d["surfaces"][0].update({"id": "DPA List"}), "lowercase slug"),
    (lambda d: d["surfaces"][0].update({"url": "http://example.test/x"}), "https://"),
    (lambda d: d["surfaces"][0].update({"authority": "vibes"}), "authority"),
    (lambda d: d["surfaces"][0].update({"checked": "not-a-date"}), "ISO date"),
    (lambda d: d["surfaces"][0].update({"providers": []}), "providers"),
])
def test_validation_rejects(mutate, fragment):
    data = _clean()
    mutate(data)
    with pytest.raises(s.DataError) as e:
        s.validate(data)
    assert fragment in str(e.value)


def test_two_surfaces_of_the_same_authority_are_rejected():
    """Comparing two marketing pages to each other would produce findings that mean
    something else entirely. The scope is enforced, not assumed."""
    data = _clean()
    data["surfaces"][1]["authority"] = "contractual"
    with pytest.raises(s.DataError) as e:
        s.validate(data)
    assert "share authority" in str(e.value)


def test_duplicate_after_alias_resolution_is_rejected():
    data = _clean()
    data["surfaces"][0]["providers"].append("Neon")
    with pytest.raises(s.DataError) as e:
        s.validate(data)
    assert "twice after alias resolution" in str(e.value)


def test_yaml_boolean_provider_name_is_rejected():
    """A bare `no` in a YAML list parses to False, not the vendor 'No'."""
    parsed = yaml.safe_load("providers: [OpenAI, no]")
    assert parsed["providers"][1] is False
    data = _clean()
    data["surfaces"][0]["providers"] = parsed["providers"]
    with pytest.raises(s.DataError) as e:
        s.validate(data)
    assert "non-empty string" in str(e.value)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_check_flag_validates(capsys):
    assert s.main(["--data", REAL, "--check"]) == 0
    assert "VALID" in capsys.readouterr().out


def test_strict_exits_two():
    assert s.main(["--data", REAL, "--strict"]) == 2


def test_default_run_exits_zero():
    assert s.main(["--data", REAL]) == 0


def test_invalid_data_exits_one(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("schema_version: 3\n", encoding="utf-8")
    assert s.main(["--data", str(bad)]) == 1


def test_render_carries_the_commitment_quote(tmp_path, monkeypatch, real):
    out = tmp_path / "subprocessor-findings.md"
    monkeypatch.setattr(s, "REPORT", str(out))
    assert s.main(["--data", REAL, "--render"]) == 0
    text = out.read_text(encoding="utf-8")
    assert "midpage.ai/subprocessors" in text
    for f in s.find(real):
        assert f["provider"] in text


def test_loading_does_not_mutate_the_observations(real):
    snapshot = copy.deepcopy(real)
    s.find(real)
    assert real == snapshot
