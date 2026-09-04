# Hash chain

`chain_hash` = `a17644ff6ab4645f91fac952cfd606ce28574cbbf44bc311994c34949c3bdf25`

Recompute with `python make_provenance.py --verify`.

| # | File | SHA-256 | Chain after |
|---|---|---|---|
| 1 | `code/deng.py` | `b76f7b27576c59c1...` | `a8ec1ce0890cafd5...` |
| 2 | `code/eia.py` | `6e7f295a888053bc...` | `dd7cb9ef6f2aea2f...` |
| 3 | `code/loaders.py` | `21431e5caadbf259...` | `835b704ca2a91c64...` |
| 4 | `code/microsoft.py` | `2998259a4552ea51...` | `714b024bf24ba205...` |
| 5 | `code/mlperf.py` | `de8832491dbf2b93...` | `22daf03306e3e226...` |
| 6 | `code/parsers.py` | `7b5ac230b39533f8...` | `ed73e9c963394d3b...` |
| 7 | `code/pjm.py` | `3d7b3d526cf71dfc...` | `79fb4678b0cfb377...` |
| 8 | `code/results.py` | `0a107539dbc4c7a1...` | `59a7f331c72894a1...` |
| 9 | `data/SOURCES.json` | `43340f54a17f8255...` | `3572be5dad3d5712...` |
| 10 | `data/deng_languages.json` | `b38a43090a3a7333...` | `4d1bd37048c154f1...` |
| 11 | `data/eia_retail_price_residential_us.json` | `c7be56ab0f526b00...` | `61917aa89df6b30c...` |
| 12 | `data/microsoft_fy25.json` | `f17640f6f4991bd1...` | `b1c1cc12b6e2645a...` |
| 13 | `data/mlperf_nvidia_systems.json` | `3ee3d89a198d3435...` | `74afea53b5793c71...` |
| 14 | `data/mlperf_submissions.json` | `775dfb75328d894f...` | `9d85baf929277cb8...` |
| 15 | `data/pjm_auctions.json` | `293d348914b648b5...` | `bc6762aee57ca584...` |
| 16 | `fetch_sources.py` | `a1d4c3b89d0375b4...` | `29fef7cf3cda619f...` |
| 17 | `make_provenance.py` | `9a73665e4af6e71c...` | `47b2104fed632056...` |
| 18 | `output/results.json` | `81e91fa47f8126e1...` | `7ef3d1c3a59d04fc...` |
| 19 | `run_all.py` | `e6f86e086d40d7d2...` | `64f42449384f5124...` |
| 20 | `tests/test_article_numbers.py` | `79c8b4f36b308bdf...` | `6251e3354d4d4feb...` |
| 21 | `tests/test_deng.py` | `e498014078e4cd95...` | `3cdf3687d9d40fc5...` |
| 22 | `tests/test_determinism.py` | `979b103a57c17358...` | `e31716e2f5e9d06c...` |
| 23 | `tests/test_eia.py` | `449110682ddb3b27...` | `4a3cb0bb9b1a1219...` |
| 24 | `tests/test_microsoft.py` | `6780cb6cf9b87670...` | `37ff0f651e65a389...` |
| 25 | `tests/test_mlperf.py` | `77710fd3796e6fc7...` | `2aee6894688bec8a...` |
| 26 | `tests/test_pjm.py` | `010294bd3fb2713d...` | `a17644ff6ab4645f...` |

## Informational (NOT hashed)

- requirements.lock
- python version and platform
- everything under .github/, docs/ and the Markdown at the root

The Python version and the operating system are deliberately absent from
this file as well as from the chain: the seal must survive a change of
machine, and so must this document. The environment that produced the
committed seal is recorded verbatim in `requirements.lock`.
