"""Determinism: the same frozen evidence must always produce the same results."""

from __future__ import annotations

import json
from pathlib import Path

from results import build

RESULTS_FILE = Path(__file__).resolve().parent.parent / "output" / "results.json"


def test_two_runs_agree() -> None:
    """Nothing in the derivation depends on time, randomness or dict order."""
    first = json.dumps(build(), sort_keys=True)
    second = json.dumps(build(), sort_keys=True)
    assert first == second


def test_the_committed_results_match_a_fresh_run() -> None:
    """``output/results.json`` cannot drift away from the code that built it."""
    committed = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    assert committed == json.loads(json.dumps(build()))
