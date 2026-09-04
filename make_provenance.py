"""Cryptographic provenance for this repository.

Builds one SHA-256 ``chain_hash`` sealing the code, the tests, the frozen
evidence and the derived results, and writes ``output/provenance.json`` plus a
human-readable ``output/hash-chain.md``. ``--verify`` recomputes the chain and
compares it against the committed seal.

Files whose content varies by machine - the lockfile, caches, the platform
itself - are listed as informational and are deliberately left out of the chain,
so that the seal survives moving between machines.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
PROVENANCE = OUTPUT / "provenance.json"
CHAIN_MARKDOWN = OUTPUT / "hash-chain.md"

HASHED_GLOBS = (
    "run_all.py",
    "make_provenance.py",
    "fetch_sources.py",
    "code/*.py",
    "tests/*.py",
    "data/*.json",
    "output/results.json",
)
INFORMATIONAL = (
    "requirements.lock",
    "python version and platform",
    "everything under .github/, docs/ and the Markdown at the root",
)


def hashed_files() -> list[Path]:
    """List, in a stable order, every file that enters the chain.

    Returns
    -------
    list of pathlib.Path
        Existing files matching :data:`HASHED_GLOBS`, sorted by relative path.
    """
    found: set[Path] = set()
    for pattern in HASHED_GLOBS:
        found.update(p for p in ROOT.glob(pattern) if p.is_file())
    return sorted(found, key=lambda p: p.relative_to(ROOT).as_posix())


def file_digest(path: Path) -> str:
    """Return the SHA-256 digest of one file.

    Parameters
    ----------
    path : pathlib.Path
        File to digest.

    Returns
    -------
    str
        Hex digest.
    """
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_chain() -> tuple[str, list[dict[str, str]]]:
    """Fold every hashed file into a single chain hash.

    Returns
    -------
    tuple
        The final chain hash and the per-file links that produced it.
    """
    running = hashlib.sha256(b"ai-energy-claim-provenance").hexdigest()
    links: list[dict[str, str]] = []
    for path in hashed_files():
        relative = path.relative_to(ROOT).as_posix()
        digest = file_digest(path)
        running = hashlib.sha256(f"{running}{relative}{digest}".encode()).hexdigest()
        links.append({"file": relative, "sha256": digest, "chain": running})
    return running, links


def write() -> str:
    """Recompute the chain and write both provenance artefacts.

    Returns
    -------
    str
        The chain hash that was written.
    """
    chain, links = build_chain()
    OUTPUT.mkdir(exist_ok=True)
    PROVENANCE.write_text(
        json.dumps(
            {
                "chain_hash": chain,
                "algorithm": "sha256",
                "n_files": len(links),
                "links": links,
                "informational_not_hashed": list(INFORMATIONAL),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Hash chain",
        "",
        f"`chain_hash` = `{chain}`",
        "",
        "Recompute with `python make_provenance.py --verify`.",
        "",
        "| # | File | SHA-256 | Chain after |",
        "|---|---|---|---|",
    ]
    lines += [
        f"| {i} | `{link['file']}` | `{link['sha256'][:16]}...` | `{link['chain'][:16]}...` |"
        for i, link in enumerate(links, 1)
    ]
    lines += [
        "",
        "## Informational (NOT hashed)",
        "",
        *(f"- {item}" for item in INFORMATIONAL),
        "",
        "The Python version and the operating system are deliberately absent from",
        "this file as well as from the chain: the seal must survive a change of",
        "machine, and so must this document. The environment that produced the",
        "committed seal is recorded verbatim in `requirements.lock`.",
        "",
    ]
    CHAIN_MARKDOWN.write_text("\n".join(lines), encoding="utf-8")
    return chain


def verify() -> int:
    """Compare the recomputed chain against the committed seal.

    Returns
    -------
    int
        ``0`` when the seal matches, ``1`` otherwise.
    """
    if not PROVENANCE.is_file():
        print(f"FAIL: {PROVENANCE} is missing; run `python make_provenance.py` first.")
        return 1
    committed = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    chain, links = build_chain()
    if committed.get("chain_hash") != chain:
        print("FAIL: chain_hash mismatch")
        print(f"  committed:  {committed.get('chain_hash')}")
        print(f"  recomputed: {chain}")
        old = {link["file"]: link["sha256"] for link in committed.get("links", [])}
        new = {link["file"]: link["sha256"] for link in links}
        for name in sorted(set(old) | set(new)):
            if old.get(name) != new.get(name):
                print(f"  differs: {name}")
        return 1
    print(f"provenance verified: {chain} ({len(links)} files)")
    return 0


def main() -> int:
    """Run the command line entry point.

    Returns
    -------
    int
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify",
        action="store_true",
        help="recompute the chain and compare it against output/provenance.json",
    )
    args = parser.parse_args()
    if args.verify:
        return verify()
    chain = write()
    print(f"provenance written: {chain}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
