# Validation

Run the offline helper suite with Python 3.10+:

```bash
python3 -m unittest discover -s tests -v
```

Coverage includes configuration overrides, single-document feature scaffolding, optional plans with reciprocal links, unsafe paths, overwrite protection, local Markdown links, dependency-table errors, and CLI exit codes.
Fixtures use temporary directories and do not modify existing project documents.
These tests do not prove model routing or review behavior.

## Installation smoke test

From an empty disposable project directory, install from an absolute checkout path:

```bash
npx skills add /absolute/path/to/hgore-claude --skill development-workflow execute-plan plan-lint --agent claude-code -y
python3 .claude/skills/development-workflow/scripts/workflow.py config --root .
python3 .claude/skills/development-workflow/scripts/workflow.py init . --feature docs/features/csv-export.md
python3 .claude/skills/plan-lint/lint.py docs/features/csv-export.md
python3 .claude/skills/development-workflow/scripts/workflow.py init . --feature docs/features/scheduled-exports.md --plan docs/plans/scheduled-exports.md
python3 .claude/skills/plan-lint/lint.py docs/features/scheduled-exports.md docs/plans/scheduled-exports.md
```

Confirm the primary skill contains its references and templates and aliases can read the installed primary skill.
Do not install globally or modify personal Claude settings for this check.

## Behavioral smoke test

Check natural-language routing in a fresh disposable project with `/development-workflow Begin designing a new feature`.
Without a feature described in the conversation or project, the agent should ask for the intended outcome, not invent one or demand flags and paths.
With the outcome supplied, check that design and planning can remain in one named feature document.
With an existing feature and a request such as "implement the next ready chunk, but don't commit", check that it infers the target while preserving scope and the publishing restriction.
For a whole-feature request, check that it continues through ready chunks and verifies their combined outcome.

In a disposable project, give the installed skill a feature with inline design and planning containing concrete, independently assessable defects.
Request review and local corrections, explicitly withholding permission to commit, push, or publish.
Run under Fable with Opus reviewers and a small explicit spend limit when supported by the host.

Check that reviewers independently inspect project context, the orchestrator adjudicates and corrects findings without intermediate human approval, corrected work receives independent review, and a fresh final audit runs.
Confirm the round limit, authorization boundaries, checkpoint retention for unfinished work, cleanup after completion, and requested versus observed model reporting.
For closure, supply a feature whose chunks are marked done but whose combined acceptance check is unverified; it should remain incomplete until verified.
After verified completion, check that doc updates preserve their intended role while recording the delivered outcome, and that later enhancements start a new feature.
Repeat feature selection with a legacy plan's `Spec` link into a broad versioned spec; the request should select only its bounded change without forcing migration or advancing the spec version.
Inspect the resulting files yourself; a model's success report is not sufficient evidence.
Report authentication or model-availability failures as untested behavior rather than a passing smoke test.
When scripting Claude Code, retain the `project` settings source so installed project skills are discoverable; disabling all settings sources also hides those skills.

Use the [synthetic behavioral fixtures](behavioral/README.md) to exercise review, simplification, project policy, and interrupted-run behavior without private project data.
Prepare one isolated case at a time and keep its evaluation criteria out of the reviewing agent's context.
Model checks are explicit, bounded development evaluations, not merge requirements; the offline suite validates the fixtures' concrete behavior, not the quality of a model's review.

For an optional historical data-flow review, use an authorized disposable pre-fix snapshot of a past shape or selection change, with its original brief and tests.
Supply the reviewer instructions and raw repository, withholding the post-mortem, known defect, and expected correction.
Inspect whether the reviewer independently discovers consumers missing from the brief and traces an accepted value to a concrete consequence.
Include a guard-removal example to check that fewer lines are not treated as evidence of preserved behavior.
Record the actual paths inspected and findings; this exercise supplies behavioral evidence, not exhaustive proof or a required merge check.
