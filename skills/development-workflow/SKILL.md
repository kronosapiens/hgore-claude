---
name: development-workflow
description: Define, plan, implement, and close bounded features with automated adversarial review and revisions. Use for the requested development workflow or automated feature/design/plan/code review with revisions, not ordinary findings-only review, routine edits, or discussion alone.
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
Configuration supplies model roles and revision limits; the [review procedure](references/review.md) owns the schedule and stopping conditions.
Read [model routing](references/models.md) before starting a review.

## Interpret the user's intent

Request: `$ARGUMENTS`.
Treat the request as natural language, not a CLI grammar.
Infer the operation, scope, and relevant artifacts from the request, conversation, and project context.
A feature is a bounded delivery effort with an observable outcome and a completion point.
Use one feature document by default, keeping its design and implementation plan inline.
Add supporting documents when complexity warrants them or the user requests them.
Do not require operation names, flags, or file paths when the intent is clear.
Use existing document locations or the project's naming conventions for new artifacts.
Ask only for missing information that materially changes the work, such as an unspecified feature outcome or an ambiguous chunk selection.
If the user says only "begin designing a new feature" and the conversation does not identify one, ask what they want to build rather than inventing a feature or demanding command syntax.
Preserve limits such as "findings only", "design only", or "don't commit" when routing; intent inference does not grant additional authority.

Examples:

```text
/development-workflow Begin designing a feature that lets users export their data.
/development-workflow Review the CSV export feature and fix substantive issues.
/development-workflow Implement the next ready chunk of CSV export, but don't commit or publish anything.
/development-workflow Close the CSV export feature and update the project docs.
```

## Route internally

Use the table to select the relevant instructions, not as a form the user must fill out.
Operation names and flags remain optional shorthand for precise requests.
Quote paths containing spaces when using that shorthand or invoking shell helpers.

| Operation | Inputs | Instructions |
|---|---|---|
| `design` | `<feature-path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `plan` | `<feature-path>`; optional `--output <plan-path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `chunk` | `<feature-or-plan-path> --chunk <chunk-id>`; optional `--output <path>` | [Authoring](references/author.md), then [review loop](references/review.md) |
| `review` | One or more artifact paths, or `code` with `--base <ref>` or `--pr <number>` | [Review loop](references/review.md) |
| `execute` | `<feature-or-plan-path>`; optional `--chunk <chunk-id>` | [Execution](references/execute.md), including code review |
| `init` | `<project-root> --feature <path>`; optional `--plan <path>` | [Setup](references/setup.md) |
| `lint` | One or more Markdown paths | [Lint](references/lint.md) |
| `close` | `<feature-or-plan-path>` | [Completion](references/finish.md) |
| `ship` | Current branch and an explicitly authorized destination | [Publishing](references/ship.md) |
| `cleanup` | An explicitly identified worktree | [Cleanup](references/cleanup.md) |
| `explain` | Recent review findings | [Remaining questions](references/questions.md) |
| `resolve` | Recent findings and the user's resolutions | [Remaining questions](references/questions.md) |

Review a feature together with its supporting design and plan when relevant so scope, dependencies, and acceptance criteria agree.
Changes to stored shapes, parsing, or data-selection guards also use [data-flow review](references/data-flow.md), from authoring through implementation and review.
Existing specs and plans remain usable without migration; resolve their roles through [project context](references/context.md).
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
- Verify required behavior and screen additional defensive work using [expected, evidenced, or speculative triggers](references/edge-cases.md).
- Keep each Markdown sentence on its own line and use the project's vocabulary.

## Handoff

Follow the [review handoff and checkpoint lifecycle](references/review.md#result-and-human-handoff), reporting the artifact, verification, and unfinished work.
Distinguish a completed review from a completed implementation.
Present review state as temporary bookkeeping, never as a decision log or source of authority.
