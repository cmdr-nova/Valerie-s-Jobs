import importlib.util
import unittest
from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "upload_curseforge", Path(__file__).resolve().parents[1] / "tools/upload_curseforge.py"
)
uploader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uploader)


class CurseForgeUploadTests(unittest.TestCase):
    def test_missing_base_game_uses_only_exact_tested_patch(self):
        versions = [{"id": 17078, "name": "1.128.90"}, {"id": 18000, "name": "1.129.1"}]
        self.assertEqual(uploader.game_version_ids(versions, "", "1.128.90.1030"), [17078])
        with self.assertRaises(ValueError):
            uploader.game_version_ids(versions, "", "1.127.0.1030")
        with self.assertRaises(ValueError):
            uploader.game_version_ids(versions + [{"id": 17079, "name": "1.128.90"}], "", "1.128.90.1030")

    def test_resolves_base_game_without_selecting_packs(self):
        versions = [{"id": 10, "name": "Base Game"}, {"id": 20, "name": "Get Famous"}]
        self.assertEqual(uploader.game_version_ids(versions, ""), [10])

    def test_missing_or_ambiguous_base_game_requires_configuration(self):
        for versions in ([], [{"id": 10, "name": "Base Game"}, {"id": 11, "name": "Base Game"}]):
            with self.assertRaises(ValueError):
                uploader.game_version_ids(versions, "")

    def test_explicit_ids_must_exist_and_are_deduplicated(self):
        versions = [{"id": 10}, {"id": 20}]
        self.assertEqual(uploader.game_version_ids(versions, "10,20,10"), [10, 20])
        with self.assertRaises(ValueError):
            uploader.game_version_ids(versions, "99")

    def test_multipart_preserves_zip_bytes_and_delimiters(self):
        data = b"PK\x03\x04\x00\xff"
        body = uploader.multipart({"releaseType": "beta"}, "mod.zip", data, "boundary")
        self.assertIn(b'name="metadata"', body)
        self.assertIn(b'name="file"; filename="mod.zip"', body)
        self.assertIn(b'{"releaseType": "beta"}', body)
        self.assertTrue(body.endswith(data + b"\r\n--boundary--\r\n"))

    def test_redirects_cannot_forward_credentials(self):
        self.assertIsNone(uploader.NoRedirects().redirect_request(None, None, 302, "", {}, "https://example.com"))
