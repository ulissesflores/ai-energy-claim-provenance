"""Conjunto 4 - Microsoft datacenter electricity by location and by region."""

from __future__ import annotations

import microsoft
import pytest
from loaders import load

RESULT = microsoft.compute()
LOCATIONS = {
    row["location"]: row["electricity_mwh"] for row in load(microsoft.FILE)["table_15_locations"]
}


def test_twenty_nine_locations_summing_to_the_published_total() -> None:
    """Table 15 lists 29 locations summing to 15.931.489 MWh."""
    assert RESULT["n_locations"] == 29
    assert RESULT["located_sum_mwh"] == 15931489


def test_the_located_sum_is_43_percent_of_the_company() -> None:
    """The article calls the located sum 43 percent of the company's electricity."""
    assert RESULT["company_total_mwh"] == 37026353
    assert round(RESULT["located_share_of_company_pct"]) == 43


@pytest.mark.parametrize(
    ("location", "mwh"),
    [("Boydton (VA)", 3113847), ("Dublin", 1308581), ("Queretaro", 6362)],
)
def test_the_three_locations_drawn_in_the_figure(location: str, mwh: int) -> None:
    """Each bar the article draws matches its row in Table 15.

    Parameters
    ----------
    location : str
        Location as published in Table 15.
    mwh : int
        Electricity consumption in MWh.
    """
    assert LOCATIONS[location] == mwh


def test_only_one_latin_american_location_is_published() -> None:
    """Queretaro is the single Latin American location in Table 15."""
    countries = {
        row["location"]: row["country"] for row in load(microsoft.FILE)["table_15_locations"]
    }
    latin = [loc for loc, country in countries.items() if country in {"Mexico", "Brazil", "Chile"}]
    assert latin == ["Queretaro"]


def test_the_one_line_subtraction_the_article_publishes() -> None:
    """661.556 minus 6.362 is 655.194 MWh, 99,04 percent of the region."""
    assert RESULT["latin_america_total_mwh"] == 661556
    assert RESULT["latin_america_located_mwh"] == 6362
    assert RESULT["latin_america_unlocated_mwh"] == 655194
    assert round(RESULT["latin_america_unlocated_pct"], 2) == 99.04
