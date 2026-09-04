"""Every self-calculated number the article publishes, in one table.

One row per sentence or figure label. The left column is the wording as it
appears in the article (Portuguese), the middle column is what this repository
derives, the right column is the value that was published. A red row here means
the article and the code disagree - which is the whole point of the repository.

Article: https://ulissesflores.com/artigos/consumo-energia-ia
"""

from __future__ import annotations

from typing import Any

import pytest
from results import build

RESULTS = build()

DENG = RESULTS["deng_languages"]
PJM = RESULTS["pjm_auctions"]
EIA = RESULTS["eia_prices"]
MSFT = RESULTS["microsoft_locations"]
MLPERF = RESULTS["mlperf_power"]

CLAIMS: list[tuple[str, Any, Any]] = [
    # -- Conjunto 1: Deng et al., 122 languages -------------------------------
    ("mediu o consumo em 122 idiomas", DENG["n_languages"], 122),
    (
        "a distancia entre o mais barato e o mais caro e de 179 vezes",
        DENG["table_1_english_pashto_ratio"],
        179.0,
    ),
    (
        "187,8 na Tabela 5, que e a que alimenta a figura",
        round(DENG["table_5_english_pashto_ratio"], 1),
        187.8,
    ),
    (
        "o portugues e a segunda lingua mais barata das 122",
        DENG["rank_by_total_energy"]["por_Latn"],
        2,
    ),
    (
        "com 1,47 vez a energia dele",
        round(DENG["energy_ratio_vs_english"]["por_Latn"], 2),
        1.47,
    ),
    (
        "figura: portugues 90,2% - 1,5x",
        (
            DENG["accuracy_pct"]["por_Latn"],
            round(DENG["energy_ratio_vs_english"]["por_Latn"], 1),
        ),
        (90.2, 1.5),
    ),
    (
        "figura: ingles 94,6% - 1x",
        (
            DENG["accuracy_pct"]["eng_Latn"],
            round(DENG["energy_ratio_vs_english"]["eng_Latn"]),
        ),
        (94.6, 1),
    ),
    (
        "figura: pashto do sul 40,4% - 188x",
        (
            DENG["accuracy_pct"]["pbt_Arab"],
            round(DENG["energy_ratio_vs_english"]["pbt_Arab"]),
        ),
        (40.4, 188),
    ),
    (
        "figura: tibetano 21,9% - 180x",
        (
            DENG["accuracy_pct"]["bod_Tibt"],
            round(DENG["energy_ratio_vs_english"]["bod_Tibt"]),
        ),
        (21.9, 180),
    ),
    (
        "o shan gasta 175 vezes a energia do ingles para acertar 10,6% das vezes",
        (
            round(DENG["energy_ratio_vs_english"]["shn_Mymr"]),
            DENG["accuracy_pct"]["shn_Mymr"],
        ),
        (175, 10.6),
    ),
    # -- Conjunto 2: PJM capacity auctions ------------------------------------
    (
        "a serie dos leiloes do PJM",
        PJM["prices_usd_mw_day"],
        [28.92, 269.92, 329.17, 333.44, 325.00],
    ),
    (
        "o salto do primeiro leilao para o segundo",
        round(PJM["pct_increase_2024_25_to_2025_26"], 1),
        833.3,
    ),
    # -- Conjunto 3: EIA residential price ------------------------------------
    ("a variacao do preco residencial americano", round(EIA["pct_change_2020_to_2025"]), 32),
    (
        "e desde o lancamento do ChatGPT",
        round(EIA["pct_change_since_chatgpt_launch"]),
        18,
    ),
    # -- Conjunto 4: Microsoft ------------------------------------------------
    ("sao 29 enderecos", MSFT["n_locations"], 29),
    ("somando 15.931.489 MWh", MSFT["located_sum_mwh"], 15931489),
    ("43% de toda a eletricidade da empresa", round(MSFT["located_share_of_company_pct"]), 43),
    ("Queretaro, no Mexico, com 6.362 MWh", MSFT["latin_america_located_mwh"], 6362),
    ("661.556 MWh no ano fiscal de 2025", MSFT["latin_america_total_mwh"], 661556),
    ("661.556 menos 6.362 da 655.194 MWh", MSFT["latin_america_unlocated_mwh"], 655194),
    (
        "99,04% do consumo latino-americano sem localidade publicada",
        round(MSFT["latin_america_unlocated_pct"], 2),
        99.04,
    ),
    ("figura: Boydton, EUA, 3.113.847", MSFT["largest_located_mwh"], 3113847),
    # -- Conjunto 5: MLPerf ---------------------------------------------------
    (
        "tabela do artigo: v5.0, 75 resultados",
        MLPERF["rounds"]["v5.0"]["nvidia_datacenter_rows"],
        75,
    ),
    (
        "tabela do artigo: v5.1, 34 resultados",
        MLPERF["rounds"]["v5.1"]["nvidia_datacenter_rows"],
        34,
    ),
    (
        "tabela do artigo: v6.0, 61 resultados",
        MLPERF["rounds"]["v6.0"]["nvidia_datacenter_rows"],
        61,
    ),
    ("total: 170 resultados", MLPERF["nvidia_datacenter_rows_total"], 170),
    ("nenhum com medicao de potencia", MLPERF["nvidia_datacenter_rows_with_power_total"], 0),
    ("a Lenovo submeteu 12 resultados com potencia medida", MLPERF["lenovo_v51_power_rows"], 12),
    (
        "em v6.0 nenhum submissor mediu potencia (0 de 465)",
        (
            MLPERF["rounds"]["v6.0"]["datacenter_rows_with_power"],
            MLPERF["rounds"]["v6.0"]["datacenter_rows"],
        ),
        (0, 465),
    ),
    (
        "os sistemas MaxQ existem para o H100 na v4.0 e para o H200 na v4.1",
        (
            len(MLPERF["nvidia_maxq_systems"]["v4.0"]),
            len(MLPERF["nvidia_maxq_systems"]["v4.1"]),
        ),
        (1, 1),
    ),
    (
        "e para nenhuma rodada depois",
        [len(MLPERF["nvidia_maxq_systems"][r]) for r in ("v5.0", "v5.1", "v6.0")],
        [0, 0, 0],
    ),
]


@pytest.mark.parametrize(("claim", "derived", "published"), CLAIMS, ids=[c[0] for c in CLAIMS])
def test_article_claim(claim: str, derived: Any, published: Any) -> None:
    """Assert that one published sentence still matches what the code derives.

    Parameters
    ----------
    claim : str
        The wording as published in the article.
    derived : Any
        The value this repository derives from the frozen evidence.
    published : Any
        The value printed in the article.
    """
    assert derived == published, claim


def test_every_conjunto_is_covered() -> None:
    """All five conjuntos the article promises appear in the claim table."""
    assert set(RESULTS) == {
        "deng_languages",
        "pjm_auctions",
        "eia_prices",
        "microsoft_locations",
        "mlperf_power",
    }
