"""Behavioral coverage for the dependency-free development workflow helper."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/development-workflow/scripts/workflow.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location("workflow", SCRIPT)
workflow = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(workflow)


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.root = self.directory / "project"
        self.root.mkdir()

    def write(self, name, content="", root=None):
        path = (root or self.root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def invoke(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = workflow.main(list(map(str, args)))
        return status, stdout.getvalue(), stderr.getvalue()


class ConfigurationTests(ProjectTestCase):
    def test_defaults(self):
        self.assertEqual(
            workflow.configuration(),
            {
                "orchestrator_model": "current",
                "reviewer_model": "auto",
                "implementer_model": "auto",
                "max_rounds": 2,
                "reviewer_count": 2,
            },
        )

    def test_cli_uses_bundle_from_unrelated_directory_without_project_configuration(self):
        for legacy_file in (False, True):
            with self.subTest(legacy_file=legacy_file):
                if legacy_file:
                    self.write(".development-workflow.json", "{")
                before = {path.name: path.read_text() for path in self.root.iterdir()}
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "config"],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), workflow.configuration())
                self.assertEqual(
                    {path.name: path.read_text() for path in self.root.iterdir()}, before
                )


class LintTests(ProjectTestCase):
    def lint(self, content):
        return workflow.lint(self.write("docs/plan.md", content))

    def test_ordinary_prose_and_proposed_inline_paths_do_not_require_a_schema(self):
        self.assertEqual(self.lint("# Small plan\n\nAdd `src/future.py` and verify behavior.\n"), [])

    def test_local_links_resolve_from_document_and_ignore_remote_urls_and_anchors(self):
        self.write("specs/design notes.md", "# Design\n")
        self.assertEqual(
            self.lint(
                '[Spec](../specs/design%20notes.md#design "Design title")\n'
                "[Spec](<../specs/design notes.md>)\n"
                "[Web](https://example.invalid/absent) [Mail](mailto:a@example.invalid)\n"
                "[CDN](//example.invalid/spec.md) [Here](#heading)\n"
            ),
            [],
        )

    def test_missing_link_reports_original_source_line(self):
        findings = self.lint("# Plan\n\n[Missing](missing.md)\n")
        self.assertEqual(len(findings), 1)
        self.assertIn("plan.md:3:", findings[0])
        self.assertIn("missing.md", findings[0])

    def test_missing_image_is_a_missing_local_target(self):
        findings = self.lint("![Diagram](missing.png)\n")
        self.assertEqual(len(findings), 1)
        self.assertIn("missing.png", findings[0])

    def test_examples_in_fences_inline_code_and_comments_are_ignored(self):
        self.assertEqual(
            self.lint(
                "```markdown\n[Missing](one.md)\n```\n"
                "~~~~markdown\n~~~\n[Missing](two.md)\n~~~~\n"
                "`[Missing](three.md)` and ``[Missing](four.md)``\n"
                "<!-- [Missing](five.md)\n[Missing](six.md) -->\n"
                "~~~markdown\n| Chunk | Depends on |\n|---|---|\n| a | a |\n~~~\n"
            ),
            [],
        )

    def test_visible_links_after_comments_and_fences_keep_correct_line_numbers(self):
        findings = self.lint(
            "<!-- hidden --> [Missing](one.md)\n"
            "```md\n[Ignored](ignored.md)\n```\n[Missing](two.md)\n"
        )
        self.assertEqual(len(findings), 2)
        self.assertIn("plan.md:1:", findings[0])
        self.assertIn("plan.md:5:", findings[1])

    def test_balanced_parentheses_in_link_destination(self):
        self.write("docs/design(v2).md")
        self.assertEqual(self.lint("[Spec](design(v2).md)\n"), [])

    def test_escaped_link_markup_is_literal_prose(self):
        self.assertEqual(self.lint(r"\[Example](not-a-link.md)" + "\n"), [])

    def test_reference_style_links_check_the_local_destination(self):
        findings = self.lint("Read [the spec][design].\n\n[design]: missing.md\n")
        self.assertTrue(any("missing.md" in finding for finding in findings))

    def test_valid_dependency_graph_and_slug_alias(self):
        for heading in ("Chunk", "Slug"):
            with self.subTest(heading=heading):
                self.assertEqual(
                    self.lint(
                        f"| {heading} | Depends on | Acceptance |\n"
                        "|:---|---:|---|\n"
                        "| `base` | — | Builds |\n"
                        "| reader | base | Reads |\n"
                        "| writer | `base`, `reader` | Writes |\n"
                    ),
                    [],
                )

    def test_dependency_table_without_outer_pipes(self):
        self.assertEqual(
            self.lint("Chunk | Depends on\n--- | ---\na | —\nb | a\n"), []
        )

    def test_dependency_errors(self):
        cases = {
            "duplicate": "| a | — |\n| a | — |\n",
            "undefined": "| a | missing |\n",
            "itself": "| a | a |\n",
            "cycle": "| a | b |\n| b | a |\n",
            "empty chunk": "| | — |\n",
            "malformed": "| a | — | extra |\n",
        }
        for expected, rows in cases.items():
            with self.subTest(expected=expected):
                findings = self.lint("| Chunk | Depends on |\n|---|---|\n" + rows)
                self.assertTrue(any(expected in finding for finding in findings), findings)

    def test_unrelated_tables_are_not_dependency_graphs(self):
        self.assertEqual(self.lint("| Name | Owner |\n|---|---|\n| a | b |\n"), [])

    def test_escaped_pipe_in_freeform_table_column(self):
        self.assertEqual(
            self.lint(
                "| Chunk | Depends on | Acceptance |\n|---|---|---|\n"
                r"| a | — | Supports a \| b |" + "\n"
            ),
            [],
        )

    def test_long_dependency_chain_does_not_hit_recursion_limit(self):
        rows = ["| step0 | — |"] + [
            f"| step{number} | step{number - 1} |" for number in range(1, 1200)
        ]
        self.assertEqual(
            self.lint("| Chunk | Depends on |\n|---|---|\n" + "\n".join(rows)), []
        )

    def test_cli_distinguishes_clean_findings_and_file_errors(self):
        clean = self.write("clean.md", "# Design\n")
        broken = self.write("broken.md", "[Missing](missing.md)\n")
        self.assertEqual(self.invoke("lint", clean)[0], 0)
        self.assertEqual(self.invoke("lint", clean, broken)[0], 1)
        status, _, stderr = self.invoke("lint", self.root / "absent.md")
        self.assertEqual(status, 2)
        self.assertIn("error:", stderr)


if __name__ == "__main__":
    unittest.main()
