"""Conjunto 2 - the five PJM capacity auctions that frame the US price story.

Article claim covered
---------------------
The series of RTO clearing prices for delivery years 2024/2025 through
2028/2029, and the jump from the first to the second.

Prices are frozen in ``data/pjm_auctions.json`` with the quote anchor and the
report URL for each one; ``fetch_sources.py`` re-extracts them from the official
PJM Base Residual Auction reports.
"""

from __future__ import annotations

from typing import Any

from loaders import load

FILE = "pjm_auctions.json"


def compute() -> dict[str, Any]:
    """Derive the auction price series and the 2024/25 to 2025/26 jump.

    Returns
    -------
    dict
        Ordered delivery years, their clearing prices, the percentage increase
        of the first step and how many auctions cleared at the regulatory cap.
    """
    auctions = load(FILE)["auctions"]
    years = [a["delivery_year"] for a in auctions]
    prices = [a["price_usd_mw_day"] for a in auctions]
    first, second = prices[0], prices[1]
    return {
        "delivery_years": years,
        "prices_usd_mw_day": prices,
        "pct_increase_2024_25_to_2025_26": (second - first) / first * 100.0,
        "auctions_cleared_at_cap": sum(1 for a in auctions if a["cleared_at_cap"]),
    }
