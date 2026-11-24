import ast
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from valeries_jobs.interview_skips import InterviewSkips


def load_function(filename, name, namespace):
    tree = ast.parse((ROOT / "src" / "valeries_jobs" / filename).read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    function.decorator_list = []
    module = ast.Module(body=[function], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), filename, "exec"), namespace)
    return namespace[name]


class InterviewSkipTests(unittest.TestCase):
    def setUp(self):
        self.skips = InterviewSkips()
        self.careers = {}
        self.tracker = SimpleNamespace(
            _sim_info=SimpleNamespace(id=10, is_selectable=True),
            get_career_by_uid=self.careers.get,
        )
        self.career = SimpleNamespace(guid64=27932)
        self.started = Mock()
        self.original = Mock(side_effect=self.join)
        self.pending = {}
        self.hook = load_function("interviews.py", "_intercepted_add_career", {
            "INTERVIEW_SKIPS": self.skips,
            "_PENDING": self.pending,
            "_ORIGINAL_ADD_CAREER": self.original,
            "should_bypass": lambda career: False,
            "_start_interview": self.started,
        })

    def join(self, tracker, career, *args, **kwargs):
        self.careers[career.guid64] = career
        return "joined"

    def test_success_joins_immediately_and_only_once(self):
        self.skips.arm(10)
        self.assertEqual(self.hook(self.tracker, self.career, show_confirmation_dialog=True), "joined")
        self.started.assert_not_called()
        self.assertFalse(self.skips.should_skip(10, self.career.guid64, True))
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.started.assert_called_once()

    def test_unarmed_application_still_interviews(self):
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.started.assert_called_once()
        self.original.assert_not_called()

    def test_other_sim_not_affected(self):
        self.skips.arm(11)
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.started.assert_called_once()
        self.assertTrue(self.skips.should_skip(11, self.career.guid64, True))

    def test_canceled_confirmation_retains_skip_and_arguments(self):
        self.skips.arm(10)
        self.original.side_effect = None
        self.original.return_value = None  # EA displayed a dialog, no career yet.
        options = {"show_confirmation_dialog": True, "schedule_shift_override": "evening", "career_track": "agency"}
        self.hook(self.tracker, self.career, **options)
        self.original.assert_called_once_with(self.tracker, self.career, **options)
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, False))

    def test_deferred_confirmation_callback_consumes_only_after_join(self):
        self.skips.arm(10)
        self.original.side_effect = None
        self.original.return_value = None
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.original.side_effect = self.join
        self.hook(self.tracker, self.career, show_confirmation_dialog=False, schedule_shift_override="evening")
        self.assertFalse(self.skips.should_skip(10, self.career.guid64, True))
        self.started.assert_not_called()

    def test_failed_join_and_exception_retain_skip(self):
        self.skips.arm(10)
        self.original.side_effect = None
        self.original.return_value = False
        self.assertFalse(self.hook(self.tracker, self.career, show_confirmation_dialog=True))
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))
        self.original.side_effect = RuntimeError("game rejected join")
        with self.assertRaises(RuntimeError):
            self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))

    def test_preexisting_career_does_not_consume_skip(self):
        self.careers[self.career.guid64] = self.career
        self.skips.arm(10)
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))

    def test_unrelated_background_join_does_not_consume_skip(self):
        self.skips.arm(10)
        self.hook(self.tracker, self.career, show_confirmation_dialog=False)
        self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))

    def test_pending_interview_not_interrupted(self):
        self.pending[10] = object()
        self.skips.arm(10)
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.started.assert_called_once()  # Existing pending-interview guard handles it.
        self.original.assert_not_called()

    def test_bypassed_or_nonselectable_career_does_not_consume(self):
        self.skips.arm(10)
        for bypass, selectable in ((True, True), (False, False)):
            self.hook.__globals__["should_bypass"] = lambda career: bypass
            self.tracker._sim_info.is_selectable = selectable
            self.hook(self.tracker, self.career, show_confirmation_dialog=True)
            self.assertTrue(self.skips.should_skip(10, self.career.guid64, True))
        self.started.assert_not_called()

    def test_rearming_does_not_stack_and_cancel_is_per_sim(self):
        self.skips.arm(10)
        self.skips.arm(10)
        self.skips.arm(11)
        self.hook(self.tracker, self.career, show_confirmation_dialog=True)
        self.assertFalse(self.skips.should_skip(10, self.career.guid64, True))
        self.assertTrue(self.skips.should_skip(11, self.career.guid64, True))
        self.assertTrue(self.skips.cancel(11))
        self.assertFalse(self.skips.cancel(11))

    def test_state_is_not_shared_by_new_sessions(self):
        self.skips.arm(10)
        self.assertFalse(InterviewSkips().should_skip(10, self.career.guid64, True))

    def test_original_positional_arguments_and_return_are_preserved(self):
        self.skips.arm(10)
        result = self.skips.join(self.tracker, self.career, self.original, True, "track", schedule_shift_override="day")
        self.assertEqual(result, "joined")
        self.original.assert_called_once_with(self.tracker, self.career, True, "track", schedule_shift_override="day")


class SkipCommandTests(unittest.TestCase):
    def setUp(self):
        self.skips = InterviewSkips()
        self.output = Mock()
        self.client = SimpleNamespace(active_sim_info=SimpleNamespace(id=10))
        self.pending = {}
        self.modules = {
            "services": SimpleNamespace(client_manager=lambda: SimpleNamespace(get=lambda connection: self.client)),
            "valeries_jobs.interview_skips": SimpleNamespace(INTERVIEW_SKIPS=self.skips),
            "valeries_jobs.interviews": SimpleNamespace(_PENDING=self.pending),
        }
        self.command = load_function("commands.py", "valeries_jobs_skip_next_interview", {
            "sims4": SimpleNamespace(commands=SimpleNamespace(CheatOutput=lambda connection: self.output)),
        })

    def call(self, *args):
        with patch.dict(sys.modules, self.modules):
            self.command(*args)

    def test_command_arms_selected_sim_and_can_cancel(self):
        self.call()
        self.assertTrue(self.skips.should_skip(10, 27932, True))
        self.call(False)
        self.assertFalse(self.skips.should_skip(10, 27932, True))

    def test_no_selected_sim_does_not_arm(self):
        self.client = None
        self.call()
        self.assertFalse(self.skips.should_skip(10, 27932, True))
        self.assertIn("select a Sim", self.output.call_args[0][0])

    def test_existing_interview_rejects_command(self):
        self.pending[10] = object()
        self.call()
        self.assertFalse(self.skips.should_skip(10, 27932, True))
        self.assertIn("finish or cancel", self.output.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
