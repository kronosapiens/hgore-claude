"""Validate the synthetic inputs and their concrete consequences, not model prose."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MODULE_SPEC = importlib.util.spec_from_file_location(
    "prepare_behavioral", Path(__file__).parent / "behavioral/prepare.py"
)
prepare = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(prepare)


class BehavioralFixtureTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def run_case(self, case, code):
        project = prepare.prepare(case, self.root / case)
        return subprocess.run(
            [sys.executable, "-c", code], cwd=project, text=True,
            capture_output=True, check=False,
        )

    def test_list_input_reaches_the_unchanged_scheduled_consumer(self):
        result = self.run_case("tag-lists", """
from api import save_tags
from jobs import segment_members
from store import load_all
save_tags('person-1', ['news', 'events'])
assert load_all()[0]['tags'] == ['news', 'events']
segment_members('news')
""")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AttributeError", result.stderr)
        self.assertIn("jobs.py", result.stderr)

    def test_removed_guard_exports_another_workspaces_row(self):
        result = self.run_case("workspace-export", """
from export import export_rows
rows = [
    {'workspace': 'one', 'active': True, 'name': 'Own'},
    {'workspace': 'two', 'active': True, 'name': 'Other'},
    {'workspace': 'one', 'active': False, 'name': 'Inactive'},
]
assert export_rows(rows, 'one') == ['Own', 'Other']
""")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ordinary_sorting_defect_is_reproducible(self):
        result = self.run_case("title-order", """
from titles import ordered_titles
assert ordered_titles(['Bravo', 'alpha', 'charlie']) == ['charlie', 'Bravo', 'alpha']
""")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_simplified_sort_preserves_the_required_behavior(self):
        result = self.run_case("direct-sort", """
import unittest
suite = unittest.defaultTestLoader.discover('.')
result = unittest.TextTestRunner().run(suite)
assert result.wasSuccessful() and result.testsRun > 0
""")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_new_reader_fails_on_the_still_supported_writer(self):
        result = self.run_case("rolling-reader", """
from reader import read_amount
from writer import message
assert read_amount({'amount': 12}) == 12
read_amount(message(12))
""")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("KeyError", result.stderr)
        self.assertIn("reader.py", result.stderr)

    def test_prepared_resume_has_a_real_basis_and_no_evaluator_material(self):
        project = prepare.prepare("resume-review", self.root / "resume")
        state = json.loads((project / "checkpoint.json").read_text())
        self.assertEqual(state["project_root"], str(project))
        self.assertEqual(state["artifact_sha256"], hashlib.sha256((project / "app.py").read_bytes()).hexdigest())
        self.assertEqual(state["rounds_started"], 1)
        self.assertEqual(state["max_rounds"], 2)
        self.assertTrue((project / "instructions/review.md").is_file())
        self.assertFalse((project / "README.md").exists())
        self.assertFalse((project / "cases").exists())

    def test_preparation_preserves_an_existing_destination(self):
        project = self.root / "existing"
        project.mkdir()
        marker = project / "user.txt"
        marker.write_text("keep this")
        with self.assertRaises(FileExistsError):
            prepare.prepare("tag-lists", project)
        self.assertEqual(marker.read_text(), "keep this")
        self.assertEqual(list(project.iterdir()), [marker])


if __name__ == "__main__":
    unittest.main()
