import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from valeries_jobs.catalog import get_profile, should_bypass  # noqa: E402


def career_type(career_id, name="Career"):
    return type(name, (), {"guid64": career_id})


class CareerCatalogTests(unittest.TestCase):
    def test_actor_is_supported(self):
        actor = career_type(189135, "ActorCareer")
        self.assertEqual(get_profile(actor)["primary"], "acting")
        self.assertFalse(should_bypass(actor))

    def test_part_time_job_uses_easier_profile(self):
        barista = career_type(35220, "TeenBarista")
        self.assertTrue(get_profile(barista)["part_time"])

    def test_noble_and_unknown_careers_fail_open(self):
        self.assertTrue(should_bypass(career_type(999, "NobleCareer")))
        self.assertTrue(should_bypass(career_type(123456789, "CustomCareer")))


if __name__ == "__main__":
    unittest.main()
