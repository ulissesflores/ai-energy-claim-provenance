# Reproducibility

Two tracks. Track 1 is offline and takes seconds; Track 2 goes back to the
publishers and takes a few minutes. Both must be green before the article's
numbers can be called reproduced.

## Two seals

This repository holds two different kinds of thing, and conflating them would be
dishonest:

| Kind | What it means | Where it lives |
|---|---|---|
| **Derivation** | Arithmetic over frozen evidence. Fully reproducible, forever, offline. | `code/`, `output/results.json` |
| **Frozen evidence** | What a publisher said on a given date. Re-derivable from the source while the source is served, and never again after that. | `data/` |

A publisher can move a report, revise a table or take a page down. When that
happens the derivation stays valid and Track 2 goes red - which is the correct
signal, not a bug. Every entry in `data/SOURCES.json` records the SHA-256 of the
file as retrieved, so drift is visible rather than silent.

## Track 1 - offline replication

```bash
git clone https://github.com/ulissesflores/ai-energy-claim-provenance
cd ai-energy-claim-provenance
pip install -r requirements.txt
python run_all.py
```

`run_all.py` derives every number into `output/results.json`, runs the test
suite against the values published in the article, and only then rebuilds the
provenance seal. Expected tail:

```text
74 passed
provenance written: <chain_hash>
```

Verify the committed seal without rebuilding it:

```bash
python make_provenance.py --verify
```

## Track 2 - re-derivation from the primary sources

```bash
python fetch_sources.py          # add --keep to inspect the downloads
```

Needs network access and `pdftotext` (Poppler) for the five PDF sources. It
downloads every entry of `data/SOURCES.json`, reports digest drift, re-parses
each document with the parsers in `code/parsers.py` and compares the result
against the frozen evidence. Downloads land in `sources/`, which is gitignored
and deleted at the end unless `--keep` is passed.

Two sources drift by design and are marked `drift_expected` in the registry:

- **EIA** appends a month at a time, so its digest changes; the check requires
  every already-frozen month to still be present with the same value.
- **The GitHub API listing** of NVIDIA result directories has no stable digest;
  the check requires `_MaxQ` to keep appearing only in v4.0 and v4.1.

## What cannot be re-run

- **The measurements themselves.** Nothing here re-measures energy. Deng et al.
  ran open models on an academic L40S GPU with a hardware counter; MLCommons
  submitters ran their own systems; Microsoft metered its own datacenters. This
  repository recomputes what those parties published, and nothing more.
- **The state of a source before it changed.** If PJM replaces a report, the
  recorded digest proves what was read on 2026-09-02; it cannot restore the file.
- **The full 122-language table.** The companion dataset of Deng et al. is
  licensed CC BY-NC-SA 4.0 and is not redistributed here, nor is the paper text.
  Only the rows the article cites are frozen, plus the ranks derived over all
  122. The claim that Portuguese is the second cheapest of the 122 therefore
  verifies in **Track 2 only**, where the paper is fetched and the whole table
  re-parsed; Track 1 asserts the frozen rank, not the ordering that produced it.

## Determinism

No random number generator, no clock and no network call takes part in the
derivation, so there is no seed to fix. `tests/test_determinism.py` asserts that
two consecutive builds agree and that `output/results.json` still matches a
fresh run.
