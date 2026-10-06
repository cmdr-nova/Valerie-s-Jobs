#!/usr/bin/env python3
"""Export STBL additions without importing game modules. Names are key contracts."""

import importlib.util
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entries():
    spec = importlib.util.spec_from_file_location("catalog", ROOT / "src/valeries_jobs/catalog.py")
    catalog = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(catalog)
    strings = json.loads((ROOT / "localization/strings.json").read_text())
    for career_id, profile in catalog.CAREERS.items():
        strings["career." + str(career_id)] = profile["name"]
    for skill in catalog.SKILLS:
        strings["skill." + skill] = skill.replace("_", " ").title()
    strings["skill.research_debate"] = "Research & Debate"
    return [
        {"name": name, "key": zlib.crc32(("valeries_jobs." + name).encode("utf-8")) & 0xffffffff, "value": value}
        for name, value in sorted(strings.items())
    ]


if __name__ == "__main__":
    print(json.dumps(entries(), ensure_ascii=False))
