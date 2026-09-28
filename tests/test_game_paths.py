import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from game_paths import read_game_version  # noqa: E402


class GameVersionTests(unittest.TestCase):
    def test_reads_utf16_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "GameVersion.txt"
            path.write_bytes("1.128.90.1030".encode("utf-16"))
            self.assertEqual(read_game_version(path), "1.128.90.1030")

    def test_reads_nul_padded_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "GameVersion.txt"
            path.write_bytes(b"1\x00.\x001\x002\x008\x00.\x009\x000\x00.\x001\x000\x003\x000\x00")
            self.assertEqual(read_game_version(path), "1.128.90.1030")


if __name__ == "__main__":
    unittest.main()

