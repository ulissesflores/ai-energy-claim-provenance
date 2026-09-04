"""Conjunto 3 - the US residential electricity price series (EIA).

Article claim covered
---------------------
The average US residential retail price rose about 32 percent between 2020 and
2025, and about 18 percent between the launch of ChatGPT (November 2022) and the
most recent month published.

The raw EIA response is US government work in the public domain and is frozen
verbatim in ``data/eia_retail_price_residential_us.json``. The aggregation rule
is pinned here on purpose: a **simple mean of the monthly values inside each
calendar year**, nominal cents per kWh, not adjusted for inflation and not
weighted by sales volume.
"""

from __future__ import annotations

from typing import Any

from loaders import load

FILE = "eia_retail_price_residential_us.json"


def monthly_series() -> dict[str, float]:
    """Return the monthly price series keyed by ``YYYY-MM``.

    Returns
    -------
    dict
        Period to price in nominal cents per kWh.
    """
    payload = load(FILE)
    return {row["period"]: float(row["price"]) for row in payload["response"]["data"]}


def annual_mean(series: dict[str, float], year: int) -> float:
    """Average the monthly values of one calendar year.

    Parameters
    ----------
    series : dict
        Monthly series as returned by :func:`monthly_series`.
    year : int
        Calendar year to average.

    Returns
    -------
    float
        Simple arithmetic mean of that year's monthly prices.

    Raises
    ------
    ValueError
        If the year has no months in the series.
    """
    values = [v for k, v in series.items() if k.startswith(f"{year}-")]
    if not values:
        raise ValueError(f"no months for {year}")
    return sum(values) / len(values)


def compute() -> dict[str, Any]:
    """Derive the two price variations the article publishes.

    Returns
    -------
    dict
        Annual means, the 2020 to 2025 variation, and the variation since the
        launch month of ChatGPT up to the latest month available.
    """
    series = monthly_series()
    mean_2020 = annual_mean(series, 2020)
    mean_2025 = annual_mean(series, 2025)
    latest_period = max(series)
    chatgpt_launch, latest = series["2022-11"], series[latest_period]
    return {
        "n_months": len(series),
        "latest_period": latest_period,
        "mean_2020_cents_kwh": mean_2020,
        "mean_2025_cents_kwh": mean_2025,
        "pct_change_2020_to_2025": (mean_2025 - mean_2020) / mean_2020 * 100.0,
        "price_2022_11_cents_kwh": chatgpt_launch,
        "price_latest_cents_kwh": latest,
        "pct_change_since_chatgpt_launch": (latest - chatgpt_launch) / chatgpt_launch * 100.0,
    }
