"""Conjunto 5 - measured power in the MLPerf Inference: Datacenter ledger."""

from __future__ import annotations

import mlperf
import pytest

RESULT = mlperf.compute()

PUBLISHED_NVIDIA_ROWS = {"v5.0": 75, "v5.1": 34, "v6.0": 61}
PUBLISHED_DATACENTER_ROWS = {"v5.0": 905, "v5.1": 586, "v6.0": 465}


@pytest.mark.parametrize(("rnd", "rows"), sorted(PUBLISHED_NVIDIA_ROWS.items()))
def test_nvidia_datacenter_rows_per_round(rnd: str, rows: int) -> None:
    """The per-round counts in the article's table, none of them with power.

    Parameters
    ----------
    rnd : str
        MLPerf Inference round.
    rows : int
        NVIDIA datacenter result rows published for that round.
    """
    assert RESULT["rounds"][rnd]["nvidia_datacenter_rows"] == rows
    assert RESULT["rounds"][rnd]["nvidia_datacenter_rows_with_power"] == 0


def test_the_headline_scoreboard_is_170_to_0() -> None:
    """The article's headline: 170 NVIDIA results, none with measured power."""
    assert RESULT["nvidia_datacenter_rows_total"] == 170
    assert RESULT["nvidia_datacenter_rows_with_power_total"] == 0


def test_the_edge_rows_are_out_of_scope_and_also_without_power() -> None:
    """The article's caveat covers NVIDIA's few edge rows, also without power."""
    outside = {r: v["nvidia_rows_outside_datacenter"] for r, v in RESULT["rounds"].items()}
    assert outside == {"v5.0": 0, "v5.1": 1, "v6.0": 2}
    assert all(
        v["nvidia_rows_outside_datacenter_with_power"] == 0 for v in RESULT["rounds"].values()
    )


@pytest.mark.parametrize(("rnd", "rows"), sorted(PUBLISHED_DATACENTER_ROWS.items()))
def test_datacenter_suite_size_per_round(rnd: str, rows: int) -> None:
    """The denominator behind 'nobody measured power in v6.0': 0 of 465.

    Parameters
    ----------
    rnd : str
        MLPerf Inference round.
    rows : int
        Total datacenter result rows in that round.
    """
    assert RESULT["rounds"][rnd]["datacenter_rows"] == rows


def test_nobody_measured_power_in_v6_0() -> None:
    """In v6.0 no submitter at all measured power in the datacenter suite."""
    assert RESULT["rounds"]["v6.0"]["datacenter_rows_with_power"] == 0
    assert RESULT["rounds"]["v6.0"]["power_submitters"] == []


def test_lenovo_is_the_audited_counterpart_on_blackwell() -> None:
    """Lenovo submitted 12 power-measured results on B200 in v5.1."""
    assert RESULT["lenovo_v51_power_rows"] == 12
    assert RESULT["rounds"]["v5.1"]["power_submitters"] == ["Lenovo"]
    assert all("B200" in acc for acc in RESULT["lenovo_v51_power_accelerators"])


def test_nvidia_measured_power_in_the_previous_generation_and_stopped() -> None:
    """``_MaxQ`` systems exist for H100 in v4.0 and H200 in v4.1, and nowhere after."""
    maxq = RESULT["nvidia_maxq_systems"]
    assert maxq["v4.0"] == ["DGX-H100_H100-SXM-80GBx8_TRT_MaxQ"]
    assert maxq["v4.1"] == ["H200-SXM-141GBx8_TRT_MaxQ"]
    assert maxq["v5.0"] == maxq["v5.1"] == maxq["v6.0"] == []
