# Validation

Run the offline helper suite with Python 3.10+:

```bash
python3 -m unittest discover -s tests -v
```

Coverage includes configuration overrides, unsafe scaffold paths, overwrite protection, local Markdown links, dependency-table errors, and CLI exit codes.
Fixtures use temporary directories and do not modify existing project documents.
These tests do not prove model routing or review behavior.

## Installation smoke test

From an empty disposable project directory, install from an absolute checkout path:

```bash
npx skills add /absolute/path/to/hgore-claude --skill development-workflow execute-plan plan-lint --agent claude-code -y
python3 .claude/skills/development-workflow/scripts/workflow.py config --root .
python3 .claude/skills/development-workflow/scripts/workflow.py init . --spec docs/spec.md --plan docs/plan.md
python3 .claude/skills/plan-lint/lint.py docs/spec.md docs/plan.md
```

Confirm the primary skill contains its references and templates and aliases can read the installed primary skill.
Do not install globally or modify personal Claude settings for this check.

## Behavioral smoke test

Check natural-language routing in a fresh disposable project with `/development-workflow Begin designing a new feature`.
Without a feature described in the conversation or project, the agent should ask for the intended outcome, not invent one or demand flags and paths.
With an existing plan and a request such as "implement the next ready chunk, but don't commit", check that it infers the target while preserving the publishing restriction.

In a disposable project, give the installed skill a spec and implementation plan with concrete, independently assessable defects.
Request review and local corrections, explicitly withholding permission to commit, push, or publish.
Run under Fable with Opus reviewers and a small explicit spend limit when supported by the host.

Check that reviewers independently inspect project context, the orchestrator adjudicates and corrects findings without intermediate human approval, corrected work receives independent review, and a fresh final audit runs.
Confirm the round limit, authorization boundaries, temporary-state cleanup, and requested versus observed model reporting.
Inspect the resulting files yourself; a model's success report is not sufficient evidence.
Report authentication or model-availability failures as untested behavior rather than a passing smoke test.
When scripting Claude Code, retain the `project` settings source so installed project skills are discoverable; disabling all settings sources also hides those skills.
