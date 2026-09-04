"""Conjunto 5 - measured power in the MLPerf Inference: Datacenter ledger.

Article claims covered
----------------------
- NVIDIA submitted 75, 34 and 61 datacenter results in rounds v5.0, v5.1 and
  v6.0 - 170 in total - and none of them carries measured power.
- Lenovo did measure power on Blackwell: 12 results with B200 accelerators in
  v5.1.
- In v6.0 no submitter at all measured power in the datacenter suite (0 of 465).
- NVIDIA did measure in the previous generation: the ``_MaxQ`` systems exist for
  v4.0 (H100) and v4.1 (H200) and for no round after that.

The counting rule is exactly the one used for the article: a row belongs to
NVIDIA when ``submitter == "NVIDIA"`` and to the datacenter suite when
``suite == "datacenter"``. Both filters matter - NVIDIA also submits a handful
of edge rows, which are outside the claim and are reported separately here.

Row-level evidence is frozen in ``data/mlperf_submissions.json``, derived from
the ``summary_results.json`` ledger of each MLCommons results repository
(Apache-2.0). The frozen file keeps only the rows any claim needs, under one
explicit filter re-applied at fetch time: a row is kept when its suite mentions
``datacenter`` **or** its submitter is NVIDIA. Edge rows from other submitters
are dropped - they are outside every claim here, and v5.0 alone carries 16,537
of them. The ``_MaxQ`` evidence predates that ledger and is frozen in
``data/mlperf_nvidia_systems.json`` as a directory listing.
"""

from __future__ import annotations

from typing import Any

from loaders import load

SUBMISSIONS_FILE = "mlperf_submissions.json"
SYSTEMS_FILE = "mlperf_nvidia_systems.json"
ROUNDS = ("v5.0", "v5.1", "v6.0")
VENDOR = "NVIDIA"
DATACENTER = "datacenter"
MAXQ = "_MaxQ"


def _rows() -> list[dict[str, Any]]:
    """Load every frozen submission row.

    Returns
    -------
    list of dict
        One entry per result line across the three rounds.
    """
    return load(SUBMISSIONS_FILE)


def compute() -> dict[str, Any]:
    """Derive the power scoreboard the article publishes.

    Returns
    -------
    dict
        Per-round and total counts for NVIDIA and for the datacenter suite as a
        whole, the Lenovo counter-example, and the ``_MaxQ`` presence per round.
    """
    rows = _rows()
    per_round: dict[str, dict[str, Any]] = {}

    for rnd in ROUNDS:
        in_round = [r for r in rows if r["round"] == rnd]
        datacenter = [r for r in in_round if r["suite"] == DATACENTER]
        vendor_dc = [r for r in datacenter if r["submitter"] == VENDOR]
        vendor_other = [
            r for r in in_round if r["submitter"] == VENDOR and r["suite"] != DATACENTER
        ]
        with_power = [r for r in datacenter if r["has_power"]]
        per_round[rnd] = {
            "datacenter_rows": len(datacenter),
            "datacenter_rows_with_power": len(with_power),
            "power_submitters": sorted({r["submitter"] for r in with_power}),
            "nvidia_datacenter_rows": len(vendor_dc),
            "nvidia_datacenter_rows_with_power": sum(1 for r in vendor_dc if r["has_power"]),
            "nvidia_rows_outside_datacenter": len(vendor_other),
            "nvidia_rows_outside_datacenter_with_power": sum(
                1 for r in vendor_other if r["has_power"]
            ),
        }

    lenovo_power = [
        r
        for r in rows
        if r["round"] == "v5.1"
        and r["suite"] == DATACENTER
        and r["has_power"]
        and r["submitter"] == "Lenovo"
    ]

    systems = load(SYSTEMS_FILE)["systems"]
    return {
        "rounds": per_round,
        "nvidia_datacenter_rows_total": sum(
            v["nvidia_datacenter_rows"] for v in per_round.values()
        ),
        "nvidia_datacenter_rows_with_power_total": sum(
            v["nvidia_datacenter_rows_with_power"] for v in per_round.values()
        ),
        "lenovo_v51_power_rows": len(lenovo_power),
        "lenovo_v51_power_accelerators": sorted({r["accelerator"] for r in lenovo_power}),
        "nvidia_maxq_systems": {
            rnd: [name for name in names if MAXQ in name] for rnd, names in systems.items()
        },
    }
