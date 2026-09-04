"""Conjunto 1 - the 122-language energy divide, as published."""

from __future__ import annotations

import deng
import pytest

RESULT = deng.compute()


def test_the_paper_covers_122_languages() -> None:
    """The article says the measurement spans 122 languages."""
    assert RESULT["n_languages"] == 122


def test_english_is_the_cheapest_and_portuguese_the_second() -> None:
    """The article says Portuguese is the second cheapest of the 122."""
    assert RESULT["rank_by_total_energy"]["eng_Latn"] == 1
    assert RESULT["rank_by_total_energy"]["por_Latn"] == 2


def test_portuguese_costs_1_47_times_english() -> None:
    """Body text says 1,47 vez; the figure label rounds the same value to 1,5x."""
    ratio = RESULT["energy_ratio_vs_english"]["por_Latn"]
    assert round(ratio, 2) == 1.47
    assert round(ratio, 1) == 1.5


def test_the_two_published_english_pashto_ratios_stay_distinct() -> None:
    """The article prints 179x from Table 1 and 187,8x from Table 5, never an average."""
    assert RESULT["table_1_english_pashto_ratio"] == 179.0
    assert round(RESULT["table_5_english_pashto_ratio"], 1) == 187.8
    assert RESULT["table_1_english_pashto_ratio"] != round(
        RESULT["table_5_english_pashto_ratio"], 1
    )


@pytest.mark.parametrize(
    ("code", "figure_ratio"),
    [("eng_Latn", 1), ("pbt_Arab", 188), ("bod_Tibt", 180), ("shn_Mymr", 175)],
)
def test_figure_energy_ratios(code: str, figure_ratio: int) -> None:
    """Each whole-number ratio in the article's figure rounds from the frozen value.

    Portuguese is left out on purpose: its label carries one decimal (1,5x) and
    is asserted by :func:`test_portuguese_costs_1_47_times_english`.

    Parameters
    ----------
    code : str
        FLORES-200 language code.
    figure_ratio : int
        Ratio against English as printed in the figure label.
    """
    assert round(RESULT["energy_ratio_vs_english"][code]) == figure_ratio


@pytest.mark.parametrize(
    ("code", "accuracy"),
    [
        ("eng_Latn", 94.6),
        ("por_Latn", 90.2),
        ("pbt_Arab", 40.4),
        ("bod_Tibt", 21.9),
        ("shn_Mymr", 10.6),
    ],
)
def test_figure_accuracies(code: str, accuracy: float) -> None:
    """Each accuracy drawn in the article's figure matches the frozen row.

    Parameters
    ----------
    code : str
        FLORES-200 language code.
    accuracy : float
        Accuracy in percent as printed in the figure label.
    """
    assert RESULT["accuracy_pct"][code] == accuracy


def test_the_expensive_languages_also_answer_worse() -> None:
    """The article's point: the languages that cost more also get answered worse."""
    accuracy = RESULT["accuracy_pct"]
    ratios = RESULT["energy_ratio_vs_english"]
    assert ratios["shn_Mymr"] > 100 and accuracy["shn_Mymr"] < accuracy["eng_Latn"] / 5
