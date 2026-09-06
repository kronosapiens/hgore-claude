# Development workflow for Claude Code

A fork of [hgorelick/hgore-claude](https://github.com/hgorelick/hgore-claude), adapted for spec-driven development with automated adversarial review and revision.
Fable orchestrates; independent Opus agents do most of the review.
The human reviews the revised result, not each initial disagreement.

## Install

From the target project, install the self-contained primary skill:

```bash
npx skills add kronosapiens/hgore-claude --skill development-workflow --agent claude-code -y
```

Add `--global` if you want it available across projects.
For a local checkout, replace `kronosapiens/hgore-claude` with its absolute directory path.
Installation includes the skill's references, templates, configuration, and Python helper.
It does not install hooks, a statusline, or project settings.
Python 3.10+ is required for the offline helper.

Start Claude Code with `claude --model fable` and verify `/development-workflow` is available.
Your Claude Code version and account must support the requested session and reviewer models.
See [model routing](skills/development-workflow/references/models.md) for configuration and fallback behavior.

## Use

Use the project's existing document locations; no `features/` layout is required.
Supply the desired outcome in the same request when authoring a new spec or plan.

```text
/development-workflow design docs/spec.md --plan docs/implementation.md
/development-workflow review docs/spec.md docs/implementation.md
/development-workflow execute docs/implementation.md --chunk extraction
/development-workflow review code --base main
```

Authoring and execution include review and revision automatically.
A separate review command is useful for existing artifacts or subsequent changes, not a mandatory duplicate stage.
Use `init . --spec docs/spec.md --plan docs/implementation.md` to scaffold missing documents without overwriting existing files.
Other operations include `plan`, `chunk`, `lint`, `close`, `ship`, `cleanup`, `explain`, and `resolve`.
The [primary skill](skills/development-workflow/SKILL.md) documents their inputs.

The default process is:

1. Read project instructions, relevant specs, and actual code to calibrate scope and priorities.
2. Author or revise a spec and implementation plan; add other documents only when useful.
3. Run up to three review/revision rounds, with two fresh independent reviewers per round, then one fresh final audit.
4. Hand the mature result to the user, or continue only if the existing request already authorizes the next action.

Reviewers report evidence; the orchestrator adjudicates, applies accepted local corrections, and verifies them.
Unresolved material findings, missing decisions, or unavailable required checks are reported honestly.
Ordinary review disagreement does not require human arbitration.

## Configuration and authority

[config.json](skills/development-workflow/config.json) supplies the defaults.
An optional `.development-workflow.json` at the project root overrides individual fields:

```json
{
  "orchestrator_model": "fable",
  "reviewer_model": "opus",
  "max_rounds": 3,
  "reviewer_count": 2
}
```

Use two reviewers, or three for a distinct additional perspective.
The session-model setting records intent; it does not switch the running host model.
An Astra orchestrator is an alternative only in a host with an explicitly configured way to invoke the chosen reviewers; this pack does not provide cross-provider orchestration.
Requested and observed models are reported separately.

Current specs and relevant inline comments hold durable rationale; Git history holds historical context.
There is no decision log, permanent approval ledger, or rule that a previously accepted choice cannot be questioned.
Temporary review state exists only to resume the current bounded run.

Local corrections are automatic within the requested workflow scope.
Commits, pushes, PR creation or updates, comments, merges, and deployments require user authorization; a clean verdict grants none.
A request to open a PR includes the necessary commit and push, without authorizing a merge or deployment.
Deployment coordination belongs in PR notes and must not drive implementation complexity for an alpha product.

## Existing commands and upgrades

All 21 original skill names remain as optional aliases to the primary skill.
For example:

```bash
npx skills add kronosapiens/hgore-claude --skill development-workflow execute-plan review-pr-v2 --agent claude-code -y
```

Install `development-workflow` alongside every alias.
Names are retained, but old positional feature names and legacy flags are not an API compatibility promise: aliases use the explicit paths and operations documented in their `SKILL.md` files.
The old shared protocol directories and decision-log templates have been retired.
Existing project documents are not deleted or migrated by installation.

The original hook and statusline scripts remain optional legacy utilities in this repository.
The new workflow does not need them, and [settings.example.json](settings.example.json) no longer wires them up.
An existing `block-self-scheduling` hook may interrupt automatic chaining; inspect your settings and remove that specific hook registration if unwanted, preserving unrelated settings.
Never replace an existing settings file wholesale.

## Development and validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/development-workflow/scripts/workflow.py config --root .
python3 skills/development-workflow/scripts/workflow.py lint README.md SDLC.md
```

The helper validates configuration, safely scaffolds two documents, and checks common local Markdown links and explicitly declared dependency tables.
It does not judge prose quality, enforce a document schema, or replace project tests and independent review.
See [SDLC.md](SDLC.md) for the full review contract and [tests/README.md](tests/README.md) for installation and behavioral checks.

This change adapts the pack only.
The Premise/Theo repository split is a separate implementation exercise, driven from its own Claude Code session.

## License

MIT.
Attribution appreciated but not required.
