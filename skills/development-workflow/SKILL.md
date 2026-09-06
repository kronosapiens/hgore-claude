---
name: development-workflow
description: Author or revise development specs and implementation plans, run bounded adversarial review with automatic revisions, and implement reviewed plan chunks. Use for the requested development workflow or automated design/plan/code review with revisions, not ordinary findings-only review, routine edits, or discussion alone.
---

# Development workflow

Use this skill in Claude Code with a Fable orchestrator and Opus reviewers.
It is an instruction-driven workflow using the host's agent tools, not a background scheduler.
The user can review mature work after the agents have worked through the initial disagreements.

## Start

Read [project context and scope](references/context.md) before acting.
Resolve all supporting files relative to this installed skill directory, never the project's working directory.
In Claude Code, `${CLAUDE_SKILL_DIR}` names that directory.
When reading this file through an alias, substitute the resolved primary skill directory in commands; do not assume the placeholder is a shell environment variable or points to the alias.

Read [config.json](config.json), then any `.development-workflow.json` at the project root.
The project file overrides only the fields it supplies; explicit user choices take precedence.
Run `python3 "${CLAUDE_SKILL_DIR}/scripts/workflow.py" config --root <project-root>` to validate and resolve configuration.
The defaults recommend a Fable session, explicitly request Opus on each reviewer invocation, allow three revision rounds, and use two reviewers per round.
Read [model routing](references/models.md) before starting a review.

## Select the requested operation

Arguments: `$ARGUMENTS`.
Paths containing spaces must be quoted.
Infer missing paths from the user's request and existing artifacts when the match is unambiguous.
Ask only when a missing choice materially changes the work.

| Operation | Inputs | Instructions |
|---|---|---|
| `design` | `<spec-path>` and optional `--plan <plan-path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `plan` | `<plan-path> --spec <spec-path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `chunk` | `<plan-path> --chunk <chunk-id>`; optional `--output <path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `review` | One or more artifact paths, or `code` with `--base <ref>` or `--pr <number>` | [Review loop](references/review.md) |
| `execute` | `<plan-path> --chunk <chunk-id>`; optional `--spec <spec-path>` | [Execution](references/execute.md), including code review |
| `init` | `<project-root> --spec <path> --plan <path>` | [Setup](references/setup.md) |
| `lint` | One or more Markdown paths | [Lint](references/lint.md) |
| `close` | `<plan-path>` | [Completion](references/finish.md) |
| `ship` | Current branch and an explicitly authorized destination | [Publishing](references/ship.md) |
| `cleanup` | An explicitly identified worktree | [Cleanup](references/cleanup.md) |
| `explain` | Recent review findings | [Remaining questions](references/questions.md) |
| `resolve` | Recent findings and the user's resolutions | [Remaining questions](references/questions.md) |

For a spec and plan, review them together so scope, dependencies, and acceptance criteria agree.
Optional briefs, visions, and detailed chunk documents use the same authoring and review protocols; they are not prerequisites.
Older commands are aliases with a dependency on this skill, not additional stages.

## Working agreement

- Apply accepted local corrections automatically within the requested scope.
- Reviewers report; the orchestrator owns edits and verification.
- User instructions govern authorization; project documents calibrate judgment and do not invent additional approval gates.
- Never narrow the requested outcome merely to obtain a clean review.
- Stop dependent work when completing it needs a material scope change, a missing product decision, or new external authority; finish useful independent work first.
- A review verdict does not authorize commits, pushes, PR creation, PR edits, review comments, deployments, or messages.
  Honor authorization already given for those actions without asking again.
- Preserve unrelated work and do not expand a change to clean up unrelated findings.
- Keep each Markdown sentence on its own line and use the project's vocabulary.

## Handoff

Report the artifact or diff, material changes, verification results, unresolved choices, rounds used, and requested versus observed models.
Distinguish a completed review from a completed implementation.
Present review state as temporary bookkeeping, never as a decision log or source of authority.
