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
            workflow.configuration(self.root),
            {
                "orchestrator_model": "fable",
                "reviewer_model": "opus",
                "implementer_model": "opus",
                "max_rounds": 2,
                "reviewer_count": 2,
            },
        )

    def test_partial_override_preserves_other_defaults(self):
        self.write(
            ".development-workflow.json",
            json.dumps({"orchestrator_model": "astra", "max_rounds": 1}),
        )
        config = workflow.configuration(self.root)
        self.assertEqual(config["orchestrator_model"], "astra")
        self.assertEqual(config["max_rounds"], 1)
        self.assertEqual(config["reviewer_model"], "opus")
        self.assertEqual(config["reviewer_count"], 2)
        self.assertEqual(workflow.configuration(self.directory)["max_rounds"], 2)

    def test_supported_numeric_boundaries(self):
        for rounds in (1, 10):
            for reviewers in (1, 3):
                with self.subTest(rounds=rounds, reviewers=reviewers):
                    self.write(
                        ".development-workflow.json",
                        json.dumps({"max_rounds": rounds, "reviewer_count": reviewers}),
                    )
                    config = workflow.configuration(self.root)
                    self.assertEqual(config["max_rounds"], rounds)
                    self.assertEqual(config["reviewer_count"], reviewers)

    def test_invalid_overrides_return_usage_error(self):
        overrides = [
            [],
            None,
            {"unexpected": "value"},
            {"orchestrator_model": " "},
            {"reviewer_model": 7},
            *({"max_rounds": value} for value in (0, 11, True, 2.5, "3")),
            *({"reviewer_count": value} for value in (0, 4, True, 2.0, "2")),
        ]
        for override in overrides:
            with self.subTest(override=override):
                self.write(".development-workflow.json", json.dumps(override))
                status, stdout, stderr = self.invoke("config", "--root", self.root)
                self.assertEqual(status, 2)
                self.assertEqual(stdout, "")
                self.assertIn("error:", stderr)

    def test_malformed_json_returns_usage_error(self):
        self.write(".development-workflow.json", "{")
        status, _, stderr = self.invoke("config", "--root", self.root)
        self.assertEqual(status, 2)
        self.assertIn("error:", stderr)

    def test_missing_configuration_root_is_rejected(self):
        status, _, _ = self.invoke("config", "--root", self.root / "missing")
        self.assertEqual(status, 2)

    def test_script_resolves_bundle_from_an_unrelated_working_directory(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "config"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["reviewer_model"], "opus")


class ScaffoldTests(ProjectTestCase):
    def test_cli_creates_only_the_feature_by_default(self):
        status, stdout, stderr = self.invoke(
            "init", self.root, "--feature", "docs/features/csv-export.md"
        )
        feature = self.root / "docs/features/csv-export.md"
        self.assertEqual(status, 0, stderr)
        self.assertEqual(stdout.strip(), str(feature))
        self.assertEqual(list(self.root.rglob("*.md")), [feature])
        self.assertEqual(workflow.lint(feature), [])

    def test_optional_plan_links_both_ways_across_paths_with_spaces(self):
        status, stdout, stderr = self.invoke(
            "init", self.root,
            "--feature", "feature notes/csv export.md",
            "--plan", "plans/build plan.md",
        )
        feature = self.root / "feature notes/csv export.md"
        plan = self.root / "plans/build plan.md"
        self.assertEqual(status, 0, stderr)
        self.assertEqual(stdout.splitlines(), [str(feature), str(plan)])
        self.assertIn("../feature%20notes/csv%20export.md", plan.read_text())
        self.assertIn("../plans/build%20plan.md", feature.read_text())
        self.assertEqual(workflow.lint(feature), [])
        self.assertEqual(workflow.lint(plan), [])

    def test_standalone_feature_is_not_overwritten(self):
        feature = self.write("feature.md", "Existing user work.\n")
        status, stdout, _ = self.invoke(
            "init", self.root, "--feature", "feature.md"
        )
        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(feature.read_text(), "Existing user work.\n")

    def test_absolute_paths_inside_root_are_supported(self):
        destinations = workflow.scaffold(
            self.root, self.root / "feature.md", self.root / "plan.md"
        )
        self.assertEqual(destinations, [self.root / "feature.md", self.root / "plan.md"])

    def test_existing_second_destination_prevents_all_writes(self):
        plan = self.write("plan.md", "Existing user work.\n")
        with self.assertRaises(ValueError):
            workflow.scaffold(self.root, Path("new/feature.md"), Path("plan.md"))
        self.assertEqual(plan.read_text(), "Existing user work.\n")
        self.assertFalse((self.root / "new").exists())

    def test_identical_normalized_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            workflow.scaffold(self.root, Path("feature.md"), Path("folder/../feature.md"))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_traversal_absolute_and_symlink_escapes_are_rejected(self):
        outside = self.directory / "outside"
        outside.mkdir()
        (self.root / "shortcut").symlink_to(outside, target_is_directory=True)
        for escaped in (
            Path("../outside/feature.md"),
            outside / "feature.md",
            Path("shortcut/feature.md"),
        ):
            for plan in (None, Path("plan.md")):
                with self.subTest(path=escaped, plan=plan), self.assertRaises(ValueError):
                    workflow.scaffold(self.root, escaped, plan)
            with self.subTest(plan=escaped), self.assertRaises(ValueError):
                workflow.scaffold(self.root, Path("feature.md"), escaped)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.root / "feature.md").exists())
        self.assertFalse((self.root / "plan.md").exists())

    def test_invalid_extension_is_rejected_before_writing(self):
        for feature, plan in (
            (Path("feature.txt"), None),
            (Path("feature.md"), Path("plan.txt")),
        ):
            with self.subTest(feature=feature, plan=plan), self.assertRaises(ValueError):
                workflow.scaffold(self.root, feature, plan)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_file_parent_is_rejected_before_creating_feature(self):
        blocker = self.write("blocked", "User data.")
        with self.assertRaises(ValueError):
            workflow.scaffold(self.root, Path("feature.md"), Path("blocked/plan.md"))
        self.assertEqual(blocker.read_text(), "User data.")
        self.assertFalse((self.root / "feature.md").exists())

    def test_destination_ancestor_collision_is_rejected_before_writing(self):
        for feature, plan in (
            ("feature.md", "feature.md/plan.md"),
            ("plan.md/feature.md", "plan.md"),
        ):
            with self.subTest(feature=feature, plan=plan):
                status, _, _ = self.invoke(
                    "init", self.root, "--feature", feature, "--plan", plan
                )
                self.assertEqual(status, 2)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_nonexistent_root_is_not_created(self):
        missing = self.root / "missing"
        status, _, _ = self.invoke(
            "init", missing, "--feature", "feature.md"
        )
        self.assertEqual(status, 2)
        self.assertFalse(missing.exists())


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
