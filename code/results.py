"""Assembly of the five conjuntos into a single results payload.

``run_all.py`` writes what :func:`build` returns to ``output/results.json``. The
tests read that same structure, so code and published numbers cannot drift apart
without the suite going red.
"""

from __future__ import annotations

from typing import Any

import deng
import eia
import microsoft
import mlperf
import pjm

CONJUNTOS = {
    "deng_languages": deng,
    "pjm_auctions": pjm,
    "eia_prices": eia,
    "microsoft_locations": microsoft,
    "mlperf_power": mlperf,
}


def build() -> dict[str, Any]:
    """Compute every conjunto and return them under one mapping.

    Returns
    -------
    dict
        Conjunto name to the numbers derived by its module.
    """
    return {name: module.compute() for name, module in CONJUNTOS.items()}
