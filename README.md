<div align="center">

# AI energy claims, traced to the primary source

**Seven figures decide the public conversation about the energy use of artificial intelligence. Six of the seven arrived with the wrong technical sheet attached — and the seventh, the only one that would decide anything here, does not exist.**

[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSES/Apache-2.0.txt)
[![License: CC BY 4.0](https://img.shields.io/badge/prose-CC--BY--4.0-lightgrey.svg)](LICENSES/CC-BY-4.0.txt)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![tests](https://img.shields.io/badge/tests-74_passing-brightgreen.svg)](tests/)
[![reproducible](https://img.shields.io/badge/reproducible-SHA--256_chain-brightgreen.svg)](output/hash-chain.md)

</div>

> [!IMPORTANT]
> **Finding.** NVIDIA submitted **170 results** to MLPerf Inference: Datacenter across
> rounds v5.0, v5.1 and v6.0, and **none** carries measured power - while its Blackwell
> product page advertises 25x the energy efficiency of the H100. Lenovo did measure the
> same generation: **12 results on B200** in v5.1. NVIDIA measured in the generation
> before, and stopped: the `_MaxQ` systems exist for the H100 in v4.0 and the H200 in
> v4.1, and for no round after that.

## The article

**Portuguese (pt-BR):** *O Brasil virou destino de data center e não mede o que eles gastam*, to
be published at [ulissesflores.com/energia](https://ulissesflores.com/energia).

> [!NOTE]
> That link is not live yet. This repository went up first on purpose: the article's closing
> paragraph points readers here, so the URL had to exist before the text could cite it. The link
> starts resolving when the article is published.

This repository is the companion to that article. Every figure the article
calculates itself lives here as running code with a test locking the published
value; nothing here is a number the article merely quotes from someone else.

## What this contributes

1. **Five recomputations from primary sources**, each one a number the article
   derives rather than repeats: the 122-language energy divide, the series of
   five PJM capacity auctions, the variation of the US residential electricity
   price, the sum of Microsoft's per-location datacenter electricity against its
   regional total, and the count of NVIDIA submissions to the power category of
   MLPerf Inference: Datacenter.
2. **A claim-to-assertion table.** `tests/test_article_numbers.py` holds 31
   rows, one per published sentence or figure label, mapping the wording in the
   article to the value this code derives. If the two ever diverge, the suite
   goes red.
3. **Provenance in two directions.** A SHA-256 chain seals code, frozen evidence
   and derived results; and `fetch_sources.py` walks back out to the publishers,
   re-downloads all eleven primary sources and re-derives the frozen evidence
   from the documents themselves.

## At a glance

| Conjunto | Headline number | Primary source | Redistributed here |
|---|---|---|---|
| Language-energy divide | 179x between English and Southern Pashto; Portuguese 2nd cheapest of 122 | Deng et al., arXiv:2606.21869v1 | cited rows only (dataset is CC BY-NC-SA) |
| PJM capacity auctions | 28.92 -> 269.92 -> 329.17 -> 333.44 -> 325.00 USD/MW-day | PJM Base Residual Auction reports | prices only |
| US residential price | +32% from 2020 to 2025 | EIA API v2, `electricity/retail-sales` | verbatim (public domain) |
| Microsoft by location | 655,194 MWh - 99.04% of Latin America - with no published location | Microsoft 2026 Environmental Data Fact Sheet | figures only |
| MLPerf measured power | 170 NVIDIA results, 0 with measured power | MLCommons `summary_results.json` (v5.0, v5.1, v6.0) | derived subset (Apache-2.0) |

## Quick start

```bash
git clone https://github.com/ulissesflores/ai-energy-claim-provenance
cd ai-energy-claim-provenance
pip install -r requirements.txt
python run_all.py
```

Expected output:

```text
74 passed
provenance written: a17644ff6ab4645f91fac952cfd606ce28574cbbf44bc311994c34949c3bdf25
results written: .../output/results.json (5 conjuntos)
```

To go back to the publishers instead of trusting `data/` - needs network access
and `pdftotext` (Poppler):

```bash
python fetch_sources.py
```

```text
Track 2 complete: every frozen figure re-derived from its primary source.
```

## Results

| # | Published in the article | Derived here |
|---|---|---|
| 1 | 122 languages measured | `n_languages = 122` |
| 2 | 179x between English and Southern Pashto (Table 1) | `table_1_english_pashto_ratio = 179.0` |
| 3 | 187.8x for the same pair (Table 5, what the figure draws) | `table_5_english_pashto_ratio = 187.81` |
| 4 | Portuguese is the 2nd cheapest of the 122, at 1.47x English | `rank = 2`, `ratio = 1.4667` |
| 5 | Shan: 175x the energy, 10.6% accuracy against 94.6% for English | `ratio = 175.41`, `accuracy = 10.6` |
| 6 | The PJM series across five delivery years | `[28.92, 269.92, 329.17, 333.44, 325.00]` |
| 7 | The jump from the first auction to the second | `+833.3%` |
| 8 | The US residential price, 2020 to 2025 | `13.16 -> 17.33 cents/kWh`, `+31.7%` |
| 9 | The same since November 2022 | `15.55 -> 18.34 cents/kWh`, `+17.9%` |
| 10 | 29 Microsoft locations summing to 15,931,489 MWh, 43% of the company | `located_sum = 15931489`, `share = 43.03%` |
| 11 | 661,556 minus 6,362 is 655,194 MWh, 99.04% of Latin America | `unlocated = 655194`, `99.04%` |
| 12 | NVIDIA: 75 + 34 + 61 = 170 datacenter results, 0 with power | `170`, `0` |
| 13 | Lenovo: 12 results with measured power on B200, v5.1 | `12`, `NVIDIA B200-SXM-180GB` |
| 14 | v6.0: nobody measured power, 0 of 465 | `0`, `465` |
| 15 | `_MaxQ` in v4.0 and v4.1 only | `v4.0: 1`, `v4.1: 1`, `v5.0/v5.1/v6.0: 0` |

Section-by-section reasoning, including what each number would take to move, is
in [`docs/findings.md`](docs/findings.md).

## What is and isn't claimed

**Claimed.** That the values above are what the cited documents contain, as
retrieved on the dates recorded in `data/SOURCES.json`, and that the arithmetic
turning them into the article's sentences is the arithmetic in `code/`.

**Not claimed.** Nothing about anyone's intent. The MLPerf ledger records what
was submitted, not why - "no measured power in the submitted rows" is a
statement about the ledger, never about a decision. Nothing about benchmarks
outside MLPerf Inference: Datacenter; Green500, SPECpower and the other MLPerf
suites were not examined. Nothing about the cause of Brazil's absence from the
Microsoft location table, which is consistent with leased capacity or with the
document's own 1 percent threshold. And no absolute energy figure travels from
the 122-language study to production models: only the ratios between languages.

**Frozen.** `data/` is what publishers said on a date, not a live feed. A moved
report or a revised table turns Track 2 red, which is the correct signal. The
Deng companion dataset (CC BY-NC-SA 4.0) and the paper text are deliberately
absent, so the "second cheapest of 122" ordering verifies in Track 2 only - see
[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Integrity

```text
chain_hash = a17644ff6ab4645f91fac952cfd606ce28574cbbf44bc311994c34949c3bdf25
```

One SHA-256 chain over 26 files: the entry points, `code/`, `tests/`, `data/`
and `output/results.json`. Recompute and compare:

```bash
python make_provenance.py --verify
```

The per-file links are in [`output/hash-chain.md`](output/hash-chain.md). The
lockfile, the Python version and the operating system are informational and are
deliberately outside the chain, so the seal survives a change of machine.

## Layout

```text
run_all.py             offline: results -> tests -> provenance seal
make_provenance.py     builds and --verify's the SHA-256 chain
fetch_sources.py       Track 2: re-download the primaries and re-derive data/
code/                  one module per conjunto, plus the raw-source parsers
data/                  frozen evidence + SOURCES.json (URL, licence, digest)
tests/                 published numbers, the claim table, determinism
output/                results.json, provenance.json, hash-chain.md
docs/findings.md       what each number means and what would move it
```

## Author

**Carlos Ulisses Flores**

[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--6034--7765-A6CE39.svg)](https://orcid.org/0000-0002-6034-7765)
[![Website](https://img.shields.io/badge/Website-ulissesflores.com-1f2937.svg)](https://ulissesflores.com)
[![Lattes](https://img.shields.io/badge/Lattes-6905246706890561-005580.svg)](http://lattes.cnpq.br/6905246706890561)

## Citation

No DOI yet: this repository is pre-release at version `0.1.0`, and the first
GitHub release will be the one that mints it. Until then, cite the commit.

```bibtex
@software{flores_ai_energy_claim_provenance_2026,
  author  = {Flores, Carlos Ulisses},
  title   = {ai-energy-claim-provenance: recomputation and provenance for the
             self-calculated figures in "O Brasil virou destino de data center
             e não mede o que eles gastam"},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/ulissesflores/ai-energy-claim-provenance}
}
```

Once the DOI exists, prefer the **concept DOI** to cite the project as a whole -
it always resolves to the latest version - and the **version DOI** to cite the
exact state you ran. Machine-readable metadata lives in
[`CITATION.cff`](CITATION.cff), [`codemeta.json`](codemeta.json) and
[`.zenodo.json`](.zenodo.json).

## License

Code is [Apache-2.0](LICENSES/Apache-2.0.txt); prose and documentation are
[CC BY 4.0](LICENSES/CC-BY-4.0.txt). Third-party terms, and what is and is not
redistributed from each source, are in [`NOTICE`](NOTICE).

## References

- Deng et al., *The Language-Energy Divide*, [arXiv:2606.21869v1](https://arxiv.org/abs/2606.21869) (preprint)
- MLCommons, [MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/)
- Microsoft, [2026 Environmental Data Fact Sheet](https://aka.ms/SustainabilityFactsheet2026)
- PJM Interconnection, [Base Residual Auction reports](https://www.pjm.com/markets-and-operations/rpm)
- U.S. Energy Information Administration, [Open Data API](https://www.eia.gov/opendata/)
- Lawrence Berkeley National Laboratory, *2025 United States Data Center Energy Usage Report*, [DOI 10.71468/P1RP4F](https://doi.org/10.71468/P1RP4F)
