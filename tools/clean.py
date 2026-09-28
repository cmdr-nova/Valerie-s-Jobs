#!/usr/bin/env python3
"""Remove generated repository build outputs only."""

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    for name in ("build", "dist"):
        target = ROOT / name
        if target.parent != ROOT:
            raise RuntimeError("Refusing unexpected clean target: {}".format(target))
        if target.exists():
            shutil.rmtree(str(target))
            print("Removed {}".format(target))


if __name__ == "__main__":
    main()

