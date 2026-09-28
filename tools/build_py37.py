#!/usr/bin/env python3
"""Compile deterministic Python 3.7 bytecode and build a ts4script archive."""

import py_compile
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
BUILD = ROOT / "build" / "scripts"
DIST = ROOT / "dist"
OUTPUT = DIST / "ValeriesJobs.ts4script"


def main():
    if BUILD.exists():
        shutil.rmtree(str(BUILD))
    BUILD.mkdir(parents=True)
    DIST.mkdir(parents=True, exist_ok=True)

    compiled = []
    for source in sorted(SOURCE.rglob("*.py")):
        relative = source.relative_to(SOURCE)
        target = (BUILD / relative).with_suffix(".pyc")
        target.parent.mkdir(parents=True, exist_ok=True)
        py_compile.compile(
            str(source),
            cfile=str(target),
            dfile=str(relative),
            doraise=True,
            optimize=0,
            invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH,
        )
        compiled.append(target)

    temporary_output = OUTPUT.with_suffix(".tmp")
    with zipfile.ZipFile(str(temporary_output), "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in compiled:
            relative = path.relative_to(BUILD).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    temporary_output.replace(OUTPUT)
    print("Built {} with {} modules".format(OUTPUT, len(compiled)))


if __name__ == "__main__":
    main()

