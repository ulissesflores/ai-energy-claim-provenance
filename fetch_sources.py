"""Track 2: re-derive the frozen evidence from the published primary sources.

``run_all.py`` is offline and trusts ``data/``. This script does the opposite:
it downloads every primary source listed in ``data/SOURCES.json``, reports
digest drift, re-parses each document and compares the result against the frozen
evidence. A green run means the frozen files are still what the publishers say.

Needs network access, and ``pdftotext`` (Poppler) for the five PDF sources.
Downloads land in ``sources/``, which is gitignored.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))

import parsers  # noqa: E402

DATA = ROOT / "data"
SOURCES = ROOT / "sources"
REGISTRY = json.loads((DATA / "SOURCES.json").read_text(encoding="utf-8"))["sources"]
TIMEOUT = 120
USER_AGENT = "ai-energy-claim-provenance/0.1.0 (+https://ulissesflores.com/energia)"


def by_id(source_id: str) -> dict[str, Any]:
    """Return one registry entry.

    Parameters
    ----------
    source_id : str
        The ``id`` field of the wanted source.

    Returns
    -------
    dict
        The registry entry.

    Raises
    ------
    KeyError
        If no entry carries that id.
    """
    for entry in REGISTRY:
        if entry["id"] == source_id:
            return entry
    raise KeyError(source_id)


def download(entry: dict[str, Any], suffix: str) -> tuple[Path, str]:
    """Fetch one source into ``sources/`` and digest it.

    Parameters
    ----------
    entry : dict
        Registry entry carrying ``id`` and ``url``.
    suffix : str
        File suffix to store it under, for example ``".pdf"``.

    Returns
    -------
    tuple
        Path of the stored file and its SHA-256 hex digest.
    """
    SOURCES.mkdir(exist_ok=True)
    target = SOURCES / f"{entry['id']}{suffix}"
    request = urllib.request.Request(entry["url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        payload = response.read()
    target.write_bytes(payload)
    return target, hashlib.sha256(payload).hexdigest()


def pdf_text(path: Path) -> str:
    """Convert a PDF to layout-preserving text.

    Parameters
    ----------
    path : pathlib.Path
        PDF to convert.

    Returns
    -------
    str
        The extracted text.

    Raises
    ------
    RuntimeError
        If ``pdftotext`` is not on PATH, or if the file is not a PDF - a
        publisher that moved a report typically answers with an HTML page and
        HTTP 200, which would otherwise surface as an opaque converter crash.
    """
    if shutil.which("pdftotext") is None:
        raise RuntimeError("pdftotext (Poppler) not found on PATH; PDF sources cannot be re-read")
    if not path.read_bytes().lstrip()[:5].startswith(b"%PDF"):
        raise RuntimeError(f"{path.name} is not a PDF; the publisher likely moved the document")
    done = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True
    )
    return done.stdout


def report(name: str, ok: bool, detail: str) -> bool:
    """Print one check line and pass its verdict through.

    Parameters
    ----------
    name : str
        Check name.
    ok : bool
        Whether the check passed.
    detail : str
        Short explanation printed after the verdict.

    Returns
    -------
    bool
        The ``ok`` argument, unchanged.
    """
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def digest_note(entry: dict[str, Any], digest: str) -> str:
    """Describe how a fresh digest compares with the recorded one.

    Parameters
    ----------
    entry : dict
        Registry entry.
    digest : str
        Freshly computed digest.

    Returns
    -------
    str
        Human-readable comparison.
    """
    recorded = entry.get("sha256")
    if recorded is None:
        return "no recorded digest (live endpoint)"
    if recorded == digest:
        return f"digest matches {recorded[:12]}..."
    if entry.get("drift_expected"):
        return f"digest drifted as expected ({recorded[:12]}... -> {digest[:12]}...)"
    return (
        f"digest DRIFTED ({recorded[:12]}... -> {digest[:12]}...); the publisher changed the file"
    )


def check_mlperf() -> bool:
    """Re-derive the MLPerf rows from the three live ledgers.

    Returns
    -------
    bool
        Whether the re-derived rows match the frozen evidence.
    """
    frozen = json.loads((DATA / "mlperf_submissions.json").read_text(encoding="utf-8"))
    rebuilt: list[dict[str, Any]] = []
    for round_name in ("v5.0", "v5.1", "v6.0"):
        entry = by_id(f"mlperf-{round_name}")
        path, digest = download(entry, ".json")
        print(f"       mlperf {round_name}: {digest_note(entry, digest)}")
        rebuilt += parsers.parse_mlperf_ledger(path.read_bytes(), round_name)
    key = lambda row: (row["round"], row["id"])  # noqa: E731
    same = sorted(rebuilt, key=key) == sorted(frozen, key=key)
    return report("mlperf_submissions.json", same, f"{len(rebuilt)} rows re-derived")


def check_mlperf_systems() -> bool:
    """Re-list the NVIDIA system directories and check the ``_MaxQ`` pattern.

    Returns
    -------
    bool
        Whether the listings still match the frozen ones.
    """
    frozen = json.loads((DATA / "mlperf_nvidia_systems.json").read_text(encoding="utf-8"))
    template = frozen["api_url_template"]
    ok = True
    for round_name, names in frozen["systems"].items():
        request = urllib.request.Request(
            template.format(round=round_name), headers={"User-Agent": USER_AGENT}
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            live = sorted(item["name"] for item in json.load(response))
        ok &= report(f"NVIDIA systems {round_name}", live == names, f"{len(live)} directories")
    return ok


def check_deng() -> bool:
    """Re-parse Table 5 of the paper and check the cited rows and ranks.

    Returns
    -------
    bool
        Whether every cited row and rank is reproduced.
    """
    frozen = json.loads((DATA / "deng_languages.json").read_text(encoding="utf-8"))
    entry = by_id("deng-language-energy-divide")
    path, digest = download(entry, ".pdf")
    print(f"       deng: {digest_note(entry, digest)}")
    rows = parsers.parse_deng_table5(pdf_text(path))
    if not report(
        "Deng Table 5 size", len(rows) == frozen["n_languages"], f"{len(rows)} languages"
    ):
        return False
    ranks = {
        row["code"]: i for i, row in enumerate(sorted(rows, key=lambda r: r["total_energy_j"]), 1)
    }
    parsed = {row["code"]: row for row in rows}
    ok = True
    for cited in frozen["table_5_cited_rows"]:
        code = cited["code"]
        live = parsed[code]
        matches = (
            live["total_energy_j"] == cited["total_energy_j"]
            and live["accuracy_pct"] == cited["accuracy_pct"]
            and ranks[code] == cited["rank_by_total_energy"]
        )
        ok &= report(f"Deng {code}", matches, f"rank {ranks[code]} of {len(rows)}")
    return ok


def check_microsoft() -> bool:
    """Re-parse Table 15 of the Fact Sheet and compare it with the frozen rows.

    Returns
    -------
    bool
        Whether the 29 locations and their values are reproduced.
    """
    frozen = json.loads((DATA / "microsoft_fy25.json").read_text(encoding="utf-8"))
    entry = by_id("microsoft-fact-sheet")
    path, digest = download(entry, ".pdf")
    print(f"       microsoft: {digest_note(entry, digest)}")
    rows = parsers.parse_microsoft_table15(pdf_text(path))
    live = {row["location"]: row["electricity_mwh"] for row in rows}
    want = {row["location"]: row["electricity_mwh"] for row in frozen["table_15_locations"]}
    return report("Microsoft Table 15", live == want, f"{len(live)} locations re-derived")


def check_pjm() -> bool:
    """Re-extract the clearing prices from the four BRA reports.

    Returns
    -------
    bool
        Whether all five published prices are reproduced.
    """
    frozen = json.loads((DATA / "pjm_auctions.json").read_text(encoding="utf-8"))["auctions"]
    want = {row["delivery_year"]: row["price_usd_mw_day"] for row in frozen}
    live: dict[str, float] = {}
    for entry in (e for e in REGISTRY if e["id"].startswith("pjm-bra-")):
        path, digest = download(entry, ".pdf")
        print(f"       {entry['id']}: {digest_note(entry, digest)}")
        for year, price in parsers.parse_pjm_prices(pdf_text(path)).items():
            if year in live and live[year] != price:
                return report("PJM prices", False, f"{year} disagrees across reports")
            live[year] = price
    missing = {year: price for year, price in want.items() if live.get(year) != price}
    return report("PJM prices", not missing, f"{len(want)} prices re-derived from 4 reports")


def check_eia() -> bool:
    """Re-fetch the EIA series and check that every frozen month survives.

    Returns
    -------
    bool
        Whether the live series still contains every frozen month, unchanged.
    """
    frozen = json.loads((DATA / "eia_retail_price_residential_us.json").read_text(encoding="utf-8"))
    entry = by_id("eia-residential-price")
    path, digest = download(entry, ".json")
    print(f"       eia: {digest_note(entry, digest)}")
    live = {
        row["period"]: row["price"]
        for row in json.loads(path.read_text(encoding="utf-8"))["response"]["data"]
    }
    was = {row["period"]: row["price"] for row in frozen["response"]["data"]}
    revised = {k: (v, live.get(k)) for k, v in was.items() if live.get(k) != v}
    return report(
        "EIA monthly series",
        not revised,
        f"{len(was)} frozen months still present in {len(live)} live months",
    )


CHECKS = (
    ("MLPerf ledgers", check_mlperf),
    ("MLPerf NVIDIA systems", check_mlperf_systems),
    ("Deng Table 5", check_deng),
    ("Microsoft Table 15", check_microsoft),
    ("PJM auctions", check_pjm),
    ("EIA prices", check_eia),
)


def main() -> int:
    """Run every Track 2 check and report the verdict.

    Returns
    -------
    int
        ``0`` if every check passed, ``1`` otherwise.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keep",
        action="store_true",
        help="leave the downloaded sources in sources/ instead of deleting them",
    )
    args = parser.parse_args()

    failures = []
    try:
        for name, check in CHECKS:
            print(f"--- {name}")
            if not check():
                failures.append(name)
    finally:
        if not args.keep and SOURCES.exists():
            shutil.rmtree(SOURCES)

    if failures:
        print(f"\nTrack 2 FAILED for: {', '.join(failures)}")
        return 1
    print("\nTrack 2 complete: every frozen figure re-derived from its primary source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
