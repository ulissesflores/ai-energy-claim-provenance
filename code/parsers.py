"""Parsers that read the primary sources, used only by ``fetch_sources.py``.

Everything in ``code/`` other than this module works offline against the frozen
evidence in ``data/``. These functions exist so that the frozen evidence can be
re-derived from the published documents rather than trusted.

PDF sources are read through ``pdftotext -layout`` (Poppler): the tables here
are column-aligned, and the layout mode is what preserves that alignment.
"""

from __future__ import annotations

import json
import re
from typing import Any

MLPERF_KEEP_SUITE = "datacenter"
MLPERF_KEEP_SUBMITTER = "NVIDIA"

_DENG_ROW = re.compile(
    r"^\s*([A-Za-zÀ-ÿ'’()\. -]+?)\s{2,}([a-z]{3}_[A-Za-z]{4})\s+(High|Medium|Low)\s+"
    r"([\d.]+)\s+([\d,]+)\s+([\d,]+\.?\d*)\s+([\d.]+)\s*$"
)
_MSFT_ROW = re.compile(
    r"^(Asia Pacific|Europe|Americas|Middle East and Africa)?\s{2,}"
    r"([A-Za-zÀ-ÿ.()–' -]+?)\s{2,}([A-Za-zÀ-ÿ.() -]+?)\s{2,}([\d,]+)\s"
)
_PJM_PRICE = re.compile(r"^\s*(?:Capacity|Performance)\s+(\d{4}/\d{2})\**\s+\$([\d,]+\.\d{2})")


def parse_mlperf_ledger(raw: bytes, round_name: str) -> list[dict[str, Any]]:
    """Reduce one MLPerf ``summary_results.json`` to the rows the claims need.

    Parameters
    ----------
    raw : bytes
        The ledger as downloaded.
    round_name : str
        Round label, for example ``"v6.0"``.

    Returns
    -------
    list of dict
        Rows whose suite mentions ``datacenter`` or whose submitter is NVIDIA.
    """
    rows = []
    for entry in json.loads(raw):
        suite = str(entry.get("Suite", ""))
        if MLPERF_KEEP_SUITE not in suite and entry.get("Submitter") != MLPERF_KEEP_SUBMITTER:
            continue
        rows.append(
            {
                "round": round_name,
                "id": entry.get("ID"),
                "submitter": entry.get("Submitter"),
                "suite": entry.get("Suite"),
                "category": entry.get("Category"),
                "accelerator": entry.get("Accelerator"),
                "has_power": bool(entry.get("has_power")),
            }
        )
    return rows


def parse_deng_table5(text: str) -> list[dict[str, Any]]:
    """Extract every language row of Table 5 from the paper text.

    Parameters
    ----------
    text : str
        Output of ``pdftotext -layout`` over the paper PDF.

    Returns
    -------
    list of dict
        One row per language, with energy per token, output tokens, total energy
        and accuracy.
    """
    rows = []
    for line in text.splitlines():
        match = _DENG_ROW.match(line)
        if match:
            rows.append(
                {
                    "language": match.group(1).strip(),
                    "code": match.group(2),
                    "resource": match.group(3),
                    "j_per_token": float(match.group(4)),
                    "output_tokens": int(match.group(5).replace(",", "")),
                    "total_energy_j": float(match.group(6).replace(",", "")),
                    "accuracy_pct": float(match.group(7)),
                }
            )
    return rows


def parse_microsoft_table15(text: str) -> list[dict[str, Any]]:
    """Extract the per-location electricity rows of Table 15 from the Fact Sheet.

    Parameters
    ----------
    text : str
        Output of ``pdftotext -layout`` over the Fact Sheet PDF.

    Returns
    -------
    list of dict
        Region, location, country and electricity consumption in MWh.
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.strip().startswith("Table 15")]
    if not starts:
        return []
    rows: list[dict[str, Any]] = []
    region = None
    for line in lines[starts[-1] :]:
        if line.strip().startswith("Footnotes"):
            break
        match = _MSFT_ROW.match(line)
        if not match:
            continue
        if match.group(1):
            region = match.group(1)
        rows.append(
            {
                "region": region,
                "location": match.group(2).strip(),
                "country": match.group(3).strip(),
                "electricity_mwh": int(match.group(4).replace(",", "")),
            }
        )
    return rows


def parse_pjm_prices(text: str) -> dict[str, float]:
    """Extract RTO clearing prices from one PJM Base Residual Auction report.

    A report states its own delivery year and, in the same summary table, the
    price of the year before, which is why four reports yield five prices.

    Parameters
    ----------
    text : str
        Output of ``pdftotext -layout`` over a BRA report PDF.

    Returns
    -------
    dict
        Delivery year in ``YYYY/YYYY`` form to price in USD per MW-day.
    """
    prices: dict[str, float] = {}
    for line in text.splitlines():
        match = _PJM_PRICE.match(line)
        if not match:
            continue
        short, value = match.group(1), float(match.group(2).replace(",", ""))
        start = short.split("/")[0]
        full = f"{start}/{start[:2]}{short.split('/')[1]}"
        prices.setdefault(full, value)
    return prices
