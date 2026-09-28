#!/usr/bin/env python3
"""Create and compare non-redistributable-free EA patch fingerprints."""

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from game_paths import PROJECT_ROOT, load_paths, read_game_version


WHOLE_FILES = {
    "python_base": "Data/Simulation/Gameplay/base.zip",
    "python_core": "Data/Simulation/Gameplay/core.zip",
    "python_simulation": "Data/Simulation/Gameplay/simulation.zip",
    "python_generated": "Game/Bin/Python/generated.zip",
    "simulation_tuning_full": "Data/Simulation/SimulationFullBuild0.package",
    "simulation_tuning_delta": "Data/Simulation/SimulationDeltaBuild0.package",
}

MONITORED_MEMBERS = {
    "Data/Simulation/Gameplay/simulation.zip": (
        "careers/career_base.pyc",
        "careers/career_interactions.pyc",
        "careers/career_service.pyc",
        "careers/career_tracker.pyc",
        "careers/career_tuning.pyc",
        "careers/pick_career_by_agent_interaction.pyc",
        "careers/active_career_gig.pyc",
        "careers/acting/acting_tuning.pyc",
        "careers/noble_career.pyc",
    ),
}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_snapshot():
    paths = load_paths()
    game_dir = paths["game_dir"]
    version = read_game_version(paths["version_file"])

    files = {}
    for label, relative_path in WHOLE_FILES.items():
        path = game_dir / relative_path
        if not path.is_file():
            raise RuntimeError("Missing monitored game file: {}".format(path))
        files[label] = {
            "path": relative_path,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }

    members = {}
    for archive_relative, member_names in MONITORED_MEMBERS.items():
        archive_path = game_dir / archive_relative
        with zipfile.ZipFile(str(archive_path), "r") as archive:
            for member_name in member_names:
                key = "{}::{}".format(archive_relative, member_name)
                try:
                    payload = archive.read(member_name)
                except KeyError:
                    members[key] = {"missing": True}
                else:
                    members[key] = {
                        "size": len(payload),
                        "sha256": sha256_bytes(payload),
                    }

    return {
        "schema": 1,
        "game_version": version,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "zip_members": members,
    }


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compare_snapshots(old, new):
    changes = []
    if old.get("game_version") != new.get("game_version"):
        changes.append(
            "game_version: {} -> {}".format(old.get("game_version"), new.get("game_version"))
        )

    for section in ("files", "zip_members"):
        old_items = old.get(section, {})
        new_items = new.get(section, {})
        for key in sorted(set(old_items) | set(new_items)):
            if old_items.get(key) != new_items.get(key):
                changes.append("{}: {}".format(section, key))
    return changes


def command_snapshot(args):
    snapshot = create_snapshot()
    version = snapshot["game_version"]
    output = Path(args.output) if args.output else (
        PROJECT_ROOT / "compatibility" / "snapshots" / "{}.json".format(version)
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Recorded compatibility snapshot: {}".format(output))


def command_check(_args):
    supported_path = PROJECT_ROOT / "compatibility" / "supported.json"
    supported = load_json(supported_path)
    baseline_path = PROJECT_ROOT / supported["snapshot"]
    if not baseline_path.is_file():
        print("REVIEW REQUIRED: supported snapshot is missing: {}".format(baseline_path))
        return 2

    baseline = load_json(baseline_path)
    current = create_snapshot()
    changes = compare_snapshots(baseline, current)
    declared_supported = supported.get("status") == "supported"

    if changes or not declared_supported:
        print("REVIEW REQUIRED")
        if not declared_supported:
            print("- Baseline status is {!r}, not 'supported'.".format(supported.get("status")))
        for change in changes:
            print("- {}".format(change))
        return 2

    print("SUPPORTED: installed game matches tested snapshot {}.".format(current["game_version"]))
    return 0


def command_diff(args):
    changes = compare_snapshots(load_json(args.old), load_json(args.new))
    if not changes:
        print("No monitored differences.")
        return 0
    print("Monitored differences:")
    for change in changes:
        print("- {}".format(change))
    return 1


def command_mark_supported(args):
    if not args.tested:
        raise RuntimeError("Refusing to mark support without the explicit --tested flag.")

    snapshot_path = PROJECT_ROOT / "compatibility" / "snapshots" / "{}.json".format(args.version)
    if not snapshot_path.is_file():
        raise RuntimeError("Snapshot does not exist: {}".format(snapshot_path))

    supported_path = PROJECT_ROOT / "compatibility" / "supported.json"
    supported = {
        "game_version": args.version,
        "snapshot": str(snapshot_path.relative_to(PROJECT_ROOT)),
        "status": "supported",
        "tested_on": datetime.now(timezone.utc).date().isoformat(),
        "notes": args.notes or "Rebuilt and passed the patch smoke-test checklist.",
    }
    supported_path.write_text(json.dumps(supported, indent=2) + "\n", encoding="utf-8")
    print("Marked game version {} as supported.".format(args.version))


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser("snapshot", help="record the installed game state")
    snapshot_parser.add_argument("--output")
    snapshot_parser.set_defaults(handler=command_snapshot)

    check_parser = subparsers.add_parser("check", help="compare installed game with support baseline")
    check_parser.set_defaults(handler=command_check)

    diff_parser = subparsers.add_parser("diff", help="compare two snapshots")
    diff_parser.add_argument("old")
    diff_parser.add_argument("new")
    diff_parser.set_defaults(handler=command_diff)

    support_parser = subparsers.add_parser("mark-supported", help="promote a tested snapshot")
    support_parser.add_argument("--version", required=True)
    support_parser.add_argument("--tested", action="store_true")
    support_parser.add_argument("--notes")
    support_parser.set_defaults(handler=command_mark_supported)
    return parser


def main():
    args = make_parser().parse_args()
    try:
        result = args.handler(args)
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1
    return int(result or 0)


if __name__ == "__main__":
    sys.exit(main())

