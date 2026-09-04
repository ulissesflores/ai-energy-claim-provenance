"""Single entry point: derive the numbers, run the tests, seal the result.

Runs offline against the frozen evidence in ``data/``. Order matters and is the
contract: results are written first, the test suite then checks them against the
values published in the article, and only a green suite gets sealed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))

from results import build  # noqa: E402

RESULTS = ROOT / "output" / "results.json"


def write_results() -> dict:
    """Compute every conjunto and write ``output/results.json``.

    Returns
    -------
    dict
        The payload that was written.
    """
    payload = build()
    RESULTS.parent.mkdir(exist_ok=True)
    RESULTS.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def run_tests() -> int:
    """Run the pytest suite.

    Returns
    -------
    int
        The pytest exit code.
    """
    return subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)


def main() -> int:
    """Run results, tests and provenance in order.

    Returns
    -------
    int
        Process exit code; non-zero if any stage fails.
    """
    payload = write_results()
    print(f"results written: {RESULTS} ({len(payload)} conjuntos)")

    code = run_tests()
    if code != 0:
        print("FAIL: test suite red; provenance not rebuilt.")
        return code

    return subprocess.call([sys.executable, "make_provenance.py"], cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
