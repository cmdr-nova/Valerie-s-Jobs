#!/usr/bin/env python3
"""Extract local EA Python archives for private API inspection."""

import shutil
import zipfile
from pathlib import Path

from game_paths import PROJECT_ROOT, load_paths, read_game_version


ARCHIVES = {
    "base": "Data/Simulation/Gameplay/base.zip",
    "core": "Data/Simulation/Gameplay/core.zip",
    "simulation": "Data/Simulation/Gameplay/simulation.zip",
    "generated": "Game/Bin/Python/generated.zip",
}


def main():
    paths = load_paths()
    version = read_game_version(paths["version_file"])
    root = PROJECT_ROOT / ".cache" / "game_api"
    destination = root / version

    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    for name, relative_path in ARCHIVES.items():
        target = destination / name
        target.mkdir()
        with zipfile.ZipFile(str(paths["game_dir"] / relative_path), "r") as archive:
            archive.extractall(str(target))

    current = root / "current"
    if current.is_symlink() or current.exists():
        if current.is_dir() and not current.is_symlink():
            shutil.rmtree(current)
        else:
            current.unlink()
    current.symlink_to(destination.name, target_is_directory=True)
    print("Extracted private game API references to {}".format(destination))


if __name__ == "__main__":
    main()

