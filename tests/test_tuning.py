import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TUNING = ROOT / "tuning"


class InterviewTuningTests(unittest.TestCase):
    def test_all_tuning_is_well_formed_xml(self):
        files = tuple(TUNING.glob("*.xml"))
        self.assertEqual(len(files), 5)
        for path in files:
            with self.subTest(path=path.name):
                ET.parse(path)

    def test_interview_durations_are_exact(self):
        expectations = {
            "ValeriesJobs_JobInterview_OneHour.xml": "60",
            "ValeriesJobs_JobInterview_TwoHours.xml": "120",
        }
        for filename, minutes in expectations.items():
            root = ET.parse(TUNING / filename).getroot()
            minimum = root.find(".//T[@n='min_time']")
            maximum = root.find(".//T[@n='max_time']")
            self.assertEqual(minimum.text, minutes)
            self.assertEqual(maximum.text, minutes)

    def test_interviews_use_safe_time_based_content(self):
        for path in TUNING.glob("ValeriesJobs_JobInterview_*.xml"):
            root = ET.parse(path).getroot()
            self.assertIsNotNone(root.find(".//V[@t='time_based']"))
            self.assertIsNone(root.find(".//U[@n='animation_ref']"))
            self.assertIsNone(root.find(".//V[@t='posture']"))

    def test_rabbit_holes_have_an_away_action(self):
        for path in TUNING.glob("*RabbitHole*.xml"):
            root = ET.parse(path).getroot()
            self.assertIsNotNone(root.find("./T[@n='away_action']"))


if __name__ == "__main__":
    unittest.main()
