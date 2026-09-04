"""Put ``code/`` on the import path for the test suite.

The modules under ``code/`` are flat, not a package, so that the directory name
never shadows anything in the standard library.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
