"""Conjunto 4 - Microsoft datacenter electricity, by location and by region.

Article claims covered
----------------------
- 29 locations in Table 15 summing to 15,931,489 MWh, 43 percent of the
  company's electricity.
- Queretaro is the only Latin American location published, at 6,362 MWh.
- Table 13 reports 661,556 MWh for Latin America, so 655,194 MWh - 99.04 percent
  of the region - carries no published location.

Only the figures themselves are frozen in ``data/microsoft_fy25.json``; the Fact
Sheet PDF is not redistributed.
"""

from __future__ import annotations

from typing import Any

from loaders import load

FILE = "microsoft_fy25.json"
LATAM_PUBLISHED_LOCATION = "Queretaro"


def compute() -> dict[str, Any]:
    """Derive the location sum, the company share and the unlocated remainder.

    Returns
    -------
    dict
        Counts, sums, the subtraction the article publishes and the shares
        derived from it.
    """
    raw = load(FILE)
    locations = raw["table_15_locations"]
    regional = raw["table_13"]

    located_sum = sum(row["electricity_mwh"] for row in locations)
    company_total = regional["total_electricity_mwh_fy25"]
    latam_total = regional["latin_america_mwh_fy25"]
    latam_located = sum(
        row["electricity_mwh"] for row in locations if row["location"] == LATAM_PUBLISHED_LOCATION
    )
    unlocated = latam_total - latam_located

    return {
        "n_locations": len(locations),
        "located_sum_mwh": located_sum,
        "company_total_mwh": company_total,
        "located_share_of_company_pct": located_sum / company_total * 100.0,
        "latin_america_total_mwh": latam_total,
        "latin_america_located_mwh": latam_located,
        "latin_america_unlocated_mwh": unlocated,
        "latin_america_unlocated_pct": unlocated / latam_total * 100.0,
        "latin_america_yoy_pct": (
            (latam_total - regional["latin_america_mwh_fy24"])
            / regional["latin_america_mwh_fy24"]
            * 100.0
        ),
        "largest_located_mwh": max(row["electricity_mwh"] for row in locations),
    }
