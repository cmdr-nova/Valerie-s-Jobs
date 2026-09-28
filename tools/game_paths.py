"""Shared local-path and game-version helpers."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_CONFIG = PROJECT_ROOT / "config" / "local_paths.json"


def load_paths():
    if not LOCAL_CONFIG.is_file():
        raise RuntimeError(
            "Missing config/local_paths.json; copy config/local_paths.example.json first."
        )

    data = json.loads(LOCAL_CONFIG.read_text(encoding="utf-8"))
    game_dir = Path(data["game_dir"]).expanduser().resolve()
    user_dir = Path(data["user_dir"]).expanduser().resolve()

    required = {
        "game_dir": game_dir,
        "user_dir": user_dir,
        "mods_dir": user_dir / "Mods",
        "version_file": user_dir / "GameVersion.txt",
    }
    missing = ["{}={}".format(name, path) for name, path in required.items() if not path.exists()]
    if missing:
        raise RuntimeError("Configured Sims 4 paths are missing: {}".format(", ".join(missing)))
    return required


def read_game_version(version_file):
    raw = Path(version_file).read_bytes()
    for encoding in ("utf-16", "utf-16-le", "utf-8-sig", "utf-8"):
        try:
            value = raw.decode(encoding).replace("\x00", "").strip()
        except UnicodeError:
            continue
        if value and all(character.isdigit() or character == "." for character in value):
            return value
    raise RuntimeError("Could not parse game version from {}".format(version_file))

