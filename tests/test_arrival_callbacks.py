import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from valeries_jobs.arrival_callbacks import (  # noqa: E402
    discard_arrival_callback,
    notify_interview_arrival,
    register_arrival_callback,
)


class ArrivalCallbackTests(unittest.TestCase):
    def test_callback_fires_only_once(self):
        arrivals = []
        register_arrival_callback(101, lambda: arrivals.append(101))

        self.assertTrue(notify_interview_arrival(101))
        self.assertFalse(notify_interview_arrival(101))
        self.assertEqual(arrivals, [101])

    def test_discard_prevents_stale_callback(self):
        register_arrival_callback(202, lambda: self.fail("stale callback fired"))
        discard_arrival_callback(202)

        self.assertFalse(notify_interview_arrival(202))


if __name__ == "__main__":
    unittest.main()
