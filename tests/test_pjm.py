"""Conjunto 2 - the five PJM capacity auctions."""

from __future__ import annotations

import pjm

RESULT = pjm.compute()

PUBLISHED_SERIES = [28.92, 269.92, 329.17, 333.44, 325.00]


def test_the_series_has_five_auctions_in_delivery_year_order() -> None:
    """The article promises the series of the five auctions."""
    assert RESULT["delivery_years"] == [
        "2024/2025",
        "2025/2026",
        "2026/2027",
        "2027/2028",
        "2028/2029",
    ]
    assert RESULT["prices_usd_mw_day"] == PUBLISHED_SERIES


def test_the_first_step_is_the_833_percent_jump() -> None:
    """From 28,92 to 269,92 dollars per MW-day is a 833,3 percent increase."""
    assert round(RESULT["pct_increase_2024_25_to_2025_26"], 1) == 833.3


def test_three_consecutive_auctions_cleared_at_the_cap() -> None:
    """2026/27, 2027/28 and 2028/29 all cleared at the regulatory cap."""
    assert RESULT["auctions_cleared_at_cap"] == 3


def test_the_last_auction_is_below_the_record() -> None:
    """The 2028/2029 price fell against the 2027/2028 record, cap and all."""
    assert RESULT["prices_usd_mw_day"][-1] < RESULT["prices_usd_mw_day"][-2]
