"""Conjunto 1 - the language-energy divide across 122 languages (Deng et al.).

Article claims covered
----------------------
- 179x between English and Southern Pashto (Table 1, the value the authors sign).
- 187.8x for the same pair in Table 5, which is what the figure plots.
- Portuguese is the second cheapest of the 122 languages, at 1.47x English.
- The five accuracy/ratio pairs drawn in the figure.

Only the rows the article cites are frozen in ``data/deng_languages.json``: the
authors' companion CSV is CC BY-NC-SA 4.0 and is deliberately not redistributed.
The rank of Portuguese over all 122 languages is a derived integer frozen with
those rows; ``fetch_sources.py`` re-derives it from the published PDF.
"""

from __future__ import annotations

from typing import Any

from loaders import load

FILE = "deng_languages.json"


def _by_code(rows: list[dict[str, Any]], code: str) -> dict[str, Any]:
    """Return the single row carrying a given FLORES language code.

    Parameters
    ----------
    rows : list of dict
        Rows of Table 5 frozen in the evidence file.
    code : str
        FLORES-200 code, for example ``"eng_Latn"``.

    Returns
    -------
    dict
        The matching row.

    Raises
    ------
    KeyError
        If no row carries that code.
    """
    for row in rows:
        if row["code"] == code:
            return row
    raise KeyError(code)


def compute() -> dict[str, Any]:
    """Derive every Deng figure the article publishes.

    Returns
    -------
    dict
        Ratios against English, ranks, accuracies and the two published values
        for the English-Pashto pair.
    """
    raw = load(FILE)
    rows = raw["table_5_cited_rows"]
    english = _by_code(rows, "eng_Latn")
    baseline = english["total_energy_j"]

    ratios = {row["code"]: row["total_energy_j"] / baseline for row in rows}
    return {
        "n_languages": raw["n_languages"],
        "english_total_energy_j": baseline,
        "energy_ratio_vs_english": ratios,
        "rank_by_total_energy": {row["code"]: row["rank_by_total_energy"] for row in rows},
        "accuracy_pct": {row["code"]: row["accuracy_pct"] for row in rows},
        "table_1_english_pashto_ratio": raw["table_1_english_pashto_ratio"],
        "table_5_english_pashto_ratio": ratios["pbt_Arab"],
    }
