import ast
import importlib.util
import re
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/valeries_jobs"
spec = importlib.util.spec_from_file_location("export_strings", ROOT / "tools/export_strings.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.strings = {entry["name"]: entry for entry in exporter.entries()}
        tree = ast.parse((SOURCE / "interviews.py").read_text())
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in ("_feedback", "_sim_name")]

        def text(name, *tokens):
            value = self.strings[name]["value"]
            indexes = {int(index) for index in re.findall(r"\{(\d+)\.(?:String|Number)\}", value)}
            self.assertEqual(indexes, set(range(len(tokens))), name)
            return (name, tokens)

        namespace = {"text": text}
        exec(compile(ast.Module(body=functions, type_ignores=[]), "interviews.py", "exec"), namespace)
        self.feedback = namespace["_feedback"]
        self.sim_name = namespace["_sim_name"]

    def test_keys_are_unique_and_stable(self):
        original = [0x042dc034, 0xe3ac5520, 0xe1e13b87, 0xa61a9f2f,
                    0xa58982e0, 0xb0a5f214, 0x4925ed61, 0xf4eea8b8, 0x1e923aed]
        keys = original + [entry["key"] for entry in self.strings.values()]
        self.assertEqual(len(keys), len(set(keys)))
        for entry in self.strings.values():
            self.assertEqual(entry["key"], zlib.crc32(("valeries_jobs." + entry["name"]).encode()) & 0xffffffff)

    def test_all_feedback_branches_use_nested_localized_strings(self):
        cases = [
            ("ghosted", 0, 0, "feedback.ghosted", None),
            ("accepted", 2, 0, "feedback.accepted", "feedback.accepted.skill"),
            ("accepted", 0, 0, "feedback.accepted", "feedback.accepted.potential"),
            ("rejected", 0, 0, "feedback.rejected", "feedback.rejected.skill"),
            ("rejected", 2, 0, "feedback.rejected", "feedback.rejected.charisma"),
            ("rejected", 2, 2, "feedback.rejected", "feedback.rejected.competition"),
        ]
        for outcome, primary, charisma, outer, inner in cases:
            with self.subTest(outcome=outcome, primary=primary, charisma=charisma):
                result = self.feedback({"primary": "logic"}, {"primary": primary, "charisma": charisma}, {"outcome": outcome})
                self.assertEqual(result[0], outer)
                if inner:
                    self.assertEqual(result[1][0][0], inner)
                    if inner.endswith("skill"):
                        self.assertEqual(result[1][0][1][0][0], "skill.logic")

    def test_static_text_calls_exist_and_match_token_counts(self):
        for filename in ("interviews.py", "notifications.py"):
            tree = ast.parse((SOURCE / filename).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "text" and isinstance(node.args[0], ast.Constant):
                    entry = self.strings[node.args[0].value]
                    indexes = {int(index) for index in re.findall(r"\{(\d+)\.(?:String|Number)\}", entry["value"])}
                    self.assertEqual(indexes, set(range(len(node.args) - 1)))

    def test_no_raw_english_dialogs_or_python_formatting(self):
        for filename in ("interviews.py", "notifications.py"):
            source = (SOURCE / filename).read_text()
            self.assertNotIn("get_raw_text", source)
            self.assertNotIn(".format(", source)

    def test_duration_messages_are_whole_sentences(self):
        self.assertIn("started.body.one", self.strings)
        self.assertIn("started.body.two", self.strings)

    def test_fallback_sim_name_is_localized(self):
        self.assertEqual(self.sim_name(object())[0], "sim.fallback")
        self.assertEqual(self.sim_name(type("Sim", (), {"first_name": "María"})()), "María")

    def test_native_api_receives_key_and_unmodified_tokens(self):
        tree = ast.parse((SOURCE / "localization.py").read_text())
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        namespace = {"zlib": zlib, "_create_localized_string": lambda key, *tokens: (key, tokens)}
        exec(compile(ast.Module(body=functions, type_ignores=[]), "localization.py", "exec"), namespace)
        nested = object()
        self.assertEqual(namespace["text"]("result.body", nested, 62), (self.strings["result.body"]["key"], (nested, 62)))
