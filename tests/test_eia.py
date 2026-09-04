"""Conjunto 3 - the US residential electricity price variation."""

from __future__ import annotations

import eia

RESULT = eia.compute()


def test_the_series_covers_306_months() -> None:
    """The frozen EIA response holds 306 monthly observations."""
    assert RESULT["n_months"] == 306
    assert RESULT["latest_period"] == "2026-06"


def test_the_2020_and_2025_annual_means() -> None:
    """The article's variation runs from 13,16 to 17,33 cents per kWh."""
    assert round(RESULT["mean_2020_cents_kwh"], 2) == 13.16
    assert round(RESULT["mean_2025_cents_kwh"], 2) == 17.33


def test_the_published_32_percent() -> None:
    """The article publishes about 32 percent between 2020 and 2025."""
    assert round(RESULT["pct_change_2020_to_2025"]) == 32


def test_the_published_18_percent_since_chatgpt() -> None:
    """The article publishes about 18 percent since November 2022."""
    assert RESULT["price_2022_11_cents_kwh"] == 15.55
    assert round(RESULT["pct_change_since_chatgpt_launch"]) == 18
