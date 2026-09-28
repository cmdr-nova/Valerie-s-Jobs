import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "valeries_jobs"


def _function_calls(path, function_name):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return {
                "{}.{}".format(call.func.value.id, call.func.attr)
                for call in ast.walk(node)
                if isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
            } | {
                call.func.id
                for call in ast.walk(node)
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            }
    raise AssertionError("Function not found: {}".format(function_name))


class InterviewLifecycleTests(unittest.TestCase):
    def test_interaction_uses_critical_priority_guard(self):
        path = SOURCE / "interview_interaction.py"
        calls = _function_calls(path, "__init__")
        self.assertIn("CriticalPriorityLiability", calls)
        self.assertIn("self.add_liability", calls)
        tree = ast.parse(path.read_text())
        constructor = next(
            call
            for call in ast.walk(tree)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "CriticalPriorityLiability"
        )
        self.assertGreaterEqual(len(constructor.args), 1)
        self.assertIsInstance(constructor.args[0], ast.Name)
        self.assertEqual(constructor.args[0].id, "self")
        priority_keywords = {
            keyword.arg: keyword.value
            for keyword in constructor.keywords
        }
        run_priority = priority_keywords["priority_on_run"]
        self.assertIsInstance(run_priority, ast.Attribute)
        self.assertEqual(run_priority.attr, "Critical")

    def test_arrival_starts_duration_alarm(self):
        calls = _function_calls(SOURCE / "interviews.py", "_on_rabbit_hole_enter")
        self.assertIn("alarms.add_alarm", calls)

    def test_exit_cancels_duration_alarm(self):
        calls = _function_calls(SOURCE / "interviews.py", "_on_rabbit_hole_exit")
        self.assertIn("_cancel_duration_alarm", calls)

    def test_duration_alarm_closes_managed_rabbit_hole(self):
        calls = _function_calls(SOURCE / "interviews.py", "_on_duration_elapsed")
        self.assertIn("finish_interview_rabbit_hole", calls)

    def test_completion_applies_the_outcome_moodlet(self):
        calls = _function_calls(SOURCE / "interviews.py", "_complete_interview")
        self.assertIn("apply_outcome_moodlet", calls)

    def test_interview_rejects_autonomous_displacement(self):
        path = SOURCE / "interview_interaction.py"
        tree = ast.parse(path.read_text())
        displace = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "displace"
        )
        returns = [node for node in ast.walk(displace) if isinstance(node, ast.Return)]
        self.assertEqual(len(returns), 1)
        self.assertIsInstance(returns[0].value, ast.Constant)
        self.assertIs(returns[0].value.value, False)

    def test_interview_blocks_queue_replacement_exit_reasons(self):
        source = (SOURCE / "interview_interaction.py").read_text()
        for name in (
            "AUTO_EXIT",
            "DISPLACED",
            "INTERACTION_INCOMPATIBILITY",
            "INTERACTION_QUEUE",
            "PRIORITY",
            "SOCIALS",
        ):
            with self.subTest(name=name):
                self.assertIn("FinishingType.{}".format(name), source)
        self.assertIn("def _cancel_eventually", source)
        self.assertIn("super()._cancel_eventually", source)


if __name__ == "__main__":
    unittest.main()
