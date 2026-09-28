import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from valeries_jobs.scoring import calculate_interview_chance, resolve_interview  # noqa: E402


class InterviewScoringTests(unittest.TestCase):
    def test_unskilled_baseline(self):
        self.assertEqual(calculate_interview_chance(), 30)

    def test_skill_bonuses(self):
        chance = calculate_interview_chance(
            primary_level=10,
            secondary_levels=(10, 10, 10),
            charisma_level=10,
        )
        self.assertEqual(chance, 80)

    def test_chance_is_clamped(self):
        self.assertEqual(calculate_interview_chance(base_chance=-500), 5)
        self.assertEqual(
            calculate_interview_chance(base_chance=500, degree_bonus=500),
            95,
        )

    def test_ghost_listing_always_ghosts(self):
        result = resolve_interview(100, ghost_listing=True, rng=random.Random(1))
        self.assertEqual(result["outcome"], "ghosted")

    def test_seeded_resolution_is_repeatable(self):
        first = resolve_interview(50, rng=random.Random(8))
        second = resolve_interview(50, rng=random.Random(8))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

