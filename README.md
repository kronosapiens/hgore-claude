# Development workflow for coding agents

A fork of [hgorelick/hgore-claude](https://github.com/hgorelick/hgore-claude), organized around bounded features with automated adversarial review and revision.
The current agent orchestrates, choosing capable implementation and independent review agents through the host's native tools.
Automatic implementation selection prefers a cheaper capable model; explicit choices in the request make runs more repeatable.
The human reviews the revised result, not each initial disagreement.

## Install

Install the self-contained primary skill once for use across projects:

```bash
npx skills add kronosapiens/hgore-claude --skill development-workflow --agent codex --global -y
```

For Claude Code, replace `--agent codex` with `--agent claude-code`.
Omit `--global` for a project-only installation.
For a local checkout, replace `kronosapiens/hgore-claude` with its absolute directory path.
Use that local-checkout form to try an unmerged branch; the repository-name command installs from the default branch.
Installation includes the skill's references, templates, configuration, and Python helper.
It does not install hooks, a statusline, or project settings.
Python 3.10+ is required for the offline helper.

Verify the skill is available in your host, then invoke it using that host's skill interface.
You can also ask the agent to read `/absolute/path/to/hgore-claude/skills/development-workflow/SKILL.md` and follow it for your request.
Your host and account must support native subagents and the selected models.
See [model routing](skills/development-workflow/references/models.md) for configuration and fallback behavior.

## Use

Describe your intent naturally when invoking the skill.
No operation names, flags, or file paths are required when the request and conversation make the task clear.
From any project directory, start Codex with the skill and your task:

```bash
codex '$development-workflow Implement the next ready chunk of CSV export.'
```

To select the implementer explicitly, add `Use gpt-5.6-sol for implementation.` to the same quoted prompt.
Single quotes preserve the literal `$development-workflow` mention for [Codex skill invocation](https://learn.chatgpt.com/docs/build-skills).
The agent works in the current directory; no project configuration file is needed.
In an existing Claude Code session:

```text
/development-workflow Begin designing a feature that lets users export their data.
/development-workflow Review the CSV export feature and fix substantive issues.
/development-workflow Implement the next ready chunk of CSV export, but don't commit or publish anything.
/development-workflow Close the CSV export feature and update the project docs.
```

The agent infers the feature, workflow stage, and relevant artifacts from your request, the conversation, and project docs.
It uses existing document locations or project naming conventions; no `features/` layout is required.
If you say only "begin designing a new feature" without identifying one elsewhere, it asks what you want to build.
Specify limits naturally, such as "findings only" or "design only"; choosing a workflow stage does not authorize additional actions.

Authoring and execution include review and revision automatically.
A separate review request is useful for existing artifacts or subsequent changes, not a mandatory duplicate stage.
You can also ask it to scaffold a feature, check links and dependencies, explain findings, or publish an explicitly authorized PR.

A feature is a bounded delivery effort with an outcome, scope, acceptance criteria, and completion point.
Start with one document containing its design, implementation checklist, and verification evidence.
Add separate design or plan files when the work needs them.
Use descriptive names such as `docs/features/csv-export.md`; new work does not advance a sequence of spec versions.

Follow project status conventions, or use `draft`, `active`, and `complete`.
Completion requires verified feature acceptance and updated maintained project docs, including behavior across implementation chunks.
Interpret project docs by their purpose and status, preserving the distinction between delivered behavior and future intent.
A later enhancement, such as scheduled exports, starts a new feature using the current system as its baseline.

Explicit operations and paths remain optional shorthand:

```text
/development-workflow design docs/features/csv-export.md
/development-workflow plan docs/features/csv-export.md
/development-workflow execute docs/features/csv-export.md --chunk download
/development-workflow review code --base main
```

The [primary skill](skills/development-workflow/SKILL.md) documents all operations and their routing.

The default process is:

1. Read project instructions, the selected feature, maintained docs, and actual code to calibrate scope and priorities.
2. Define or revise the feature's design and implementation plan, inline by default.
3. Follow the [bounded review procedure](skills/development-workflow/references/review.md), with revision, removal where applicable, and an independent final audit.
4. Hand the mature result to the user, or continue only if the existing request already authorizes the next action.

Reviewers report evidence; the orchestrator adjudicates, applies accepted local corrections, and verifies them.
Unresolved material findings, missing decisions, or unavailable required checks are reported honestly.
Ordinary review disagreement does not require human arbitration.

## Configuration and authority

[config.json](skills/development-workflow/config.json) ships with the skill and supplies its defaults: the current session orchestrates, implementation and review models are selected automatically, and the revision budget is two rounds with two reviewers.
Small changes use one reviewer under the review procedure.

The [review procedure](skills/development-workflow/references/review.md#review-schedule) explains how these settings determine the schedule.
Supply overrides in the request, such as "Use gpt-5.6-sol for implementation and reviews, with one revision round."
Standing preferences can live in existing agent instructions such as `AGENTS.md` or `CLAUDE.md`; explicit choices in the current request take precedence.
For repeatable runs, name models tested on representative project tasks, using identifiers supported by your host.
The skill does not read or create a project-specific configuration file.
Existing `.development-workflow.json` files are no longer read; move any wanted preferences into the invocation or existing agent instructions.

Automatic selection checks actual host access, task capability, and available cost evidence before choosing; it does not guarantee equal quality or savings.
Compare tests, independent review, and total usage including retries when evaluating a cheaper model.
The orchestrator announces concrete choices before invocation and does not silently replace explicit pins.
`current` and `auto` are workflow directives, not tool model IDs; the Python helper does not discover models.
The session-model setting records intent and does not switch the running host model, including for legacy concrete values such as `fable`.
This pack does not provide cross-provider orchestration.
Configured, requested, and observed models are reported separately; missing telemetry is reported as unavailable.

Maintained project docs and relevant inline comments hold durable rationale; completed features and Git history hold historical context.
There is no decision log, permanent approval ledger, or rule that a previously accepted choice cannot be questioned.
An unfinished run retains a small checkpoint so interruption or handoff does not lose its findings, verification, or remaining budget.

Local corrections are automatic within the requested workflow scope.
Commits, pushes, PR creation or updates, comments, merges, and deployments require user authorization; a clean verdict grants none.
A request to open a PR includes the necessary commit and push, without authorizing a merge or deployment.
Deployment coordination belongs in PR notes; compatibility mechanisms follow the project's actual requirements.

## Existing commands and upgrades

All 21 original skill names remain as optional aliases to the primary skill.
For example:

```bash
npx skills add kronosapiens/hgore-claude --skill development-workflow execute-plan review-pr-v2 --agent claude-code -y
```

Install `development-workflow` alongside every alias.
Aliases accept natural-language requests for their respective operations, with explicit paths and arguments available as shorthand.
Names are retained, but old positional feature names and legacy flags are not an API compatibility promise.
The old shared protocol directories and decision-log templates have been retired.
Existing project documents are not deleted or migrated by installation.
Existing spec/plan pairs remain usable for a requested bounded change, including plans with a legacy `Spec` link.
A broad versioned spec supplies context without making all of its outstanding work part of the selected feature.
The scaffold helper now uses `--feature <path>` with optional `--plan <path>`; it no longer requires or accepts `--spec`.

The original hook and statusline scripts remain optional legacy utilities in this repository.
The new workflow does not need them, and [settings.example.json](settings.example.json) no longer wires them up.
An existing `block-self-scheduling` hook may interrupt automatic chaining; inspect your settings and remove that specific hook registration if unwanted, preserving unrelated settings.
Never replace an existing settings file wholesale.

## Development and validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/development-workflow/scripts/workflow.py config
python3 skills/development-workflow/scripts/workflow.py lint README.md SDLC.md
```

The helper validates bundled defaults, safely scaffolds a feature and optional linked plan, and checks common local Markdown links and explicitly declared dependency tables.
It does not judge prose quality, enforce a document schema, or replace project tests and independent review.
See [SDLC.md](SDLC.md) for the instruction map and [tests/README.md](tests/README.md) for installation and behavioral checks, including synthetic review and resumption fixtures.

This change adapts the pack only.
The Premise/Theo repository split is a separate implementation exercise, driven from its own agent session.

## License

MIT.
Attribution appreciated but not required.
