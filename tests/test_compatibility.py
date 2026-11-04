import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from compatibility import compare_snapshots, resolve_game_file  # noqa: E402


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


class GameFileResolutionTests(unittest.TestCase):
    def _touch(self, root, relative):
        path = Path(root) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")
        return path

    def test_windows_layout_uses_canonical_path(self):
        with tempfile.TemporaryDirectory() as root:
            expected = self._touch(root, "Game/Bin/Python/generated.zip")
            self.assertEqual(resolve_game_file(root, "Game/Bin/Python/generated.zip"), expected)

    def test_mac_layout_falls_back_to_alternate(self):
        with tempfile.TemporaryDirectory() as root:
            expected = self._touch(root, "Python/generated.zip")
            self.assertEqual(resolve_game_file(root, "Game/Bin/Python/generated.zip"), expected)

    def test_missing_file_lists_every_location(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(RuntimeError) as raised:
                resolve_game_file(root, "Game/Bin/Python/generated.zip")
            self.assertIn("Python/generated.zip", str(raised.exception))


if __name__ == "__main__":
    unittest.main()

