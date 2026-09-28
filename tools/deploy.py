#!/usr/bin/env python3
"""Deploy only Valerie's Jobs artifacts to the configured live Mods folder."""

import shutil

from game_paths import PROJECT_ROOT, load_paths


ARTIFACTS = ("ValeriesJobs.ts4script", "ValeriesJobs.package")


def main():
    paths = load_paths()
    mods_dir = paths["mods_dir"]
    destination = mods_dir / "ValeriesJobs"

    if destination.parent != mods_dir:
        raise RuntimeError("Refusing unexpected deployment target: {}".format(destination))
    destination.mkdir(parents=True, exist_ok=True)

    copied = 0
    for artifact_name in ARTIFACTS:
        source = PROJECT_ROOT / "dist" / artifact_name
        if not source.is_file():
            continue
        shutil.copy2(str(source), str(destination / artifact_name))
        print("Deployed {}".format(destination / artifact_name))
        copied += 1

    if not copied:
        raise RuntimeError("No Valerie's Jobs artifacts exist under dist/; run make build first.")


if __name__ == "__main__":
    main()

