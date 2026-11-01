#!/usr/bin/env python3
"""Convenience wrapper: python scripts/selfplay.py --hands 1000 --sims 200

Runs selfplay from the installed package so it works whether or not you
installed with `pip install -e .` (requires the src/ tree on sys.path)."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bluffbot.__main__ import selfplay  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hands", type=int, default=100)
    ap.add_argument("--sims", type=int, default=120)
    a = ap.parse_args()
    selfplay(a.hands, a.sims)
