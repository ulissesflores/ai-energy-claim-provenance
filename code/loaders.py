"""Filesystem access to the frozen evidence under ``data/``.

The whole package reads its inputs through this module so that a single path
constant defines where frozen evidence lives.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load(name: str) -> Any:
    """Load one frozen evidence file from ``data/``.

    Parameters
    ----------
    name : str
        File name relative to ``data/``, including the ``.json`` suffix.

    Returns
    -------
    Any
        The decoded JSON payload.

    Raises
    ------
    FileNotFoundError
        If the file is missing from ``data/``.
    """
    path = DATA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"frozen evidence missing: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)
