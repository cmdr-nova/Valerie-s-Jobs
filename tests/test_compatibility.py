import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from compatibility import compare_snapshots  # noqa: E402


class CompatibilityComparisonTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {
            "game_version": "1.2.3.4",
            "files": {"simulation": {"sha256": "abc", "size": 10}},
            "zip_members": {"career_tracker.pyc": {"sha256": "def", "size": 5}},
        }

    def test_identical_snapshot_has_no_changes(self):
        self.assertEqual(compare_snapshots(self.baseline, copy.deepcopy(self.baseline)), [])

    def test_version_change_requires_review(self):
        current = copy.deepcopy(self.baseline)
        current["game_version"] = "1.2.3.5"
        self.assertIn("game_version: 1.2.3.4 -> 1.2.3.5", compare_snapshots(self.baseline, current))

    def test_monitored_module_change_is_named(self):
        current = copy.deepcopy(self.baseline)
        current["zip_members"]["career_tracker.pyc"]["sha256"] = "changed"
        self.assertIn(
            "zip_members: career_tracker.pyc",
            compare_snapshots(self.baseline, current),
        )


if __name__ == "__main__":
    unittest.main()

