import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TUNING = ROOT / "tuning"


class InterviewTuningTests(unittest.TestCase):
    def test_all_tuning_is_well_formed_xml(self):
        files = tuple(TUNING.glob("*.xml"))
        self.assertEqual(len(files), 8)
        for path in files:
            with self.subTest(path=path.name):
                ET.parse(path)

    def test_outcome_buffs_are_visible_temporary_moodlets(self):
        expected = {
            "ValeriesJobs_Buff_InterviewAccepted.xml": ("14634", "240"),
            "ValeriesJobs_Buff_InterviewRejected.xml": ("14643", "120"),
            "ValeriesJobs_Buff_GhostListing.xml": ("251719", "180"),
        }
        builder = (ROOT / "tools" / "build_package.js").read_text()
        for filename, (mood_type, duration) in expected.items():
            with self.subTest(path=filename):
                root = ET.parse(TUNING / filename).getroot()
                self.assertEqual(root.attrib["c"], "Buff")
                self.assertEqual(root.attrib["m"], "buffs.buff")
                self.assertEqual(root.find("./T[@n='mood_type']").text, mood_type)
                self.assertEqual(root.find("./T[@n='mood_weight']").text, "1")
                self.assertEqual(root.find("./T[@n='visible']").text, "True")
                self.assertEqual(
                    root.find(".//T[@n='max_duration']").text,
                    duration,
                )
                self.assertIn(filename, builder)
        ghost = ET.parse(TUNING / "ValeriesJobs_Buff_GhostListing.xml").getroot()
        category = ghost.find(".//L[@n='categories']/E")
        self.assertIsNotNone(category)
        self.assertEqual(category.text, "Scared_Buffs")

    def test_interviews_use_buffered_conditions_for_progress_display(self):
        expected_display_minutes = {
            "ValeriesJobs_JobInterview_OneHour.xml": "61",
            "ValeriesJobs_JobInterview_TwoHours.xml": "121",
        }
        for path in TUNING.glob("ValeriesJobs_JobInterview_*.xml"):
            root = ET.parse(path).getroot()
            self.assertEqual(root.attrib["c"], "JobInterviewInteraction")
            self.assertEqual(root.attrib["m"], "valeries_jobs.interview_interaction")
            condition = root.find(".//V[@t='time_based']/U[@n='time_based']")
            self.assertIsNotNone(condition)
            self.assertEqual(
                condition.find("./T[@n='min_time']").text,
                expected_display_minutes[path.name],
            )
            self.assertEqual(
                condition.find("./T[@n='max_time']").text,
                expected_display_minutes[path.name],
            )
            literal = root.find(".//U[@n='literal']")
            self.assertEqual(
                literal.find("./E[@n='interaction_action']").text,
                "EXIT_NATURALLY",
            )
            self.assertEqual(
                literal.find("./E[@n='progress_bar_action']").text,
                "FORCE_USE_CONDITION",
            )
            self.assertIsNone(root.find("./L[@n='basic_liabilities']"))

    def test_interviews_hold_the_native_offscreen_posture(self):
        for path in TUNING.glob("ValeriesJobs_JobInterview_*.xml"):
            root = ET.parse(path).getroot()
            posture = root.find(".//V[@t='posture']//T[@n='enabled']")
            animation = root.find(".//U[@n='animation_ref']/T[@n='factory']")
            self.assertIsNotNone(posture)
            self.assertEqual(posture.text, "23832")
            self.assertIsNotNone(animation)
            self.assertEqual(animation.text, "23834")

    def test_interviews_route_to_lot_exit_before_hiding(self):
        for path in TUNING.glob("ValeriesJobs_JobInterview_*.xml"):
            root = ET.parse(path).getroot()
            spawn_tag = root.find(".//L[@n='Spawn_Point_Tags']/E")
            self.assertIsNotNone(spawn_tag)
            self.assertEqual(spawn_tag.text, "Spawn_Arrival")

    def test_rabbit_holes_have_an_away_action(self):
        for path in TUNING.glob("*RabbitHole*.xml"):
            root = ET.parse(path).getroot()
            self.assertIsNotNone(root.find("./T[@n='away_action']"))

    def test_rabbit_hole_clock_starts_from_scripted_arrival(self):
        for path in TUNING.glob("*RabbitHole*.xml"):
            root = ET.parse(path).getroot()
            policy = root.find("./E[@n='time_tracking_policy']")
            self.assertIsNotNone(policy)
            self.assertEqual(policy.text, "NO_TIME_LIMIT")


if __name__ == "__main__":
    unittest.main()
