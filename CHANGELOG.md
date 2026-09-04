# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-04

Pre-DOI. No GitHub release exists yet: the first release will be the release
candidate that mints the DOI.

### Added

- Five conjuntos, one module each under `code/`: the 122-language energy divide
  (Deng et al.), the five PJM capacity auctions, the US residential electricity
  price variation (EIA), Microsoft datacenter electricity by location against
  its regional total, and measured power in MLPerf Inference: Datacenter.
- `tests/test_article_numbers.py`: every self-calculated number the article
  publishes, as a table of claim to assertion - 31 rows.
- `run_all.py`: results, tests and provenance in one offline entry point.
- `make_provenance.py`: SHA-256 chain over code, tests, frozen evidence and
  derived results, with `--verify`.
- `fetch_sources.py`: Track 2 - downloads every primary source, reports digest
  drift and re-derives the frozen evidence from the published documents.
- `data/SOURCES.json`: registry of the eleven primary sources with URL, licence,
  digest at retrieval and what is or is not redistributed.

### Notes

- The companion dataset of Deng et al. (CC BY-NC-SA 4.0) is not redistributed;
  only the rows the article cites, plus ranks derived from the full table.
- Two URLs recorded during the reporting had to be corrected against the
  publisher: the PJM 2025/2026 and 2028/2029 auction reports do not follow the
  `-bra-report.pdf` pattern of the other two.
