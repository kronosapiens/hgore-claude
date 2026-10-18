---
name: development-workflow
description: Define, plan, implement, and close bounded features with a single spec/plan audit and iterative code review. Use for the requested development workflow or automated feature/design/plan/code review with corrections, not ordinary findings-only review, routine edits, or discussion alone.
---

# Development workflow

The current agent orchestrates, selecting capable implementation and review agents through the host's native tools.
It is an instruction-driven workflow using the host's agent tools, not a background scheduler.
Specs and plans receive one independent audit for major issues; code receives iterative review and correction.

## Start

Read [project context and scope](references/context.md) before acting.
Resolve all supporting files relative to this installed skill directory, never the project's working directory.
Substitute the absolute primary skill directory for `<skill-directory>` in commands below.
Find it from this `SKILL.md` file's location, including when the user points to the file directly or invokes an alias.
The placeholder is not a shell environment variable and does not refer to the alias directory.

Read the bundled defaults in [config.json](config.json).
Apply model and budget choices from the request or existing agent instructions; explicit choices in the current request take precedence.
Do not read or create a project-specific configuration file for this skill.
Run `python3 "<skill-directory>/scripts/workflow.py" config` to validate and display the bundled defaults, then apply any instruction overrides yourself.
Keep `max_rounds` between 1 and 10 and `reviewer_count` between 1 and 3.
The [review procedure](references/review.md) owns the schedule and stopping conditions.
Read [model routing](references/models.md) before invoking implementation or review agents.
Resolve `current` and `auto` through those instructions; they are directives for the orchestrator, not tool model IDs or Python model discovery.

## Interpret the user's intent

Use the user's request and conversation as natural language, not a CLI grammar.
Infer the operation, scope, and relevant artifacts from the request, conversation, and project context.
A feature is a bounded delivery effort with an observable outcome and a completion point.
Each feature is one GitHub issue whose body holds its design and implementation plan.
Add supporting documents when complexity warrants them or the user requests them.
Do not require operation names, flags, issue numbers, or file paths when the intent is clear.
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
| `design` | `<feature-issue>` (number or URL) | [Authoring](references/author.md), then [spec and plan audit](references/review.md#single-spec-and-plan-audit) |
| `plan` | `<feature-issue>` | [Authoring](references/author.md), then [spec and plan audit](references/review.md#single-spec-and-plan-audit) |
| `chunk` | `<feature-issue> --chunk <chunk-id>` | [Authoring](references/author.md), then [spec and plan audit](references/review.md#single-spec-and-plan-audit) |
| `review` | One or more feature issues or artifact paths, or `code` with `--base <ref>` or `--pr <number>` | [Review procedure](references/review.md) |
| `execute` | `<feature-issue>`; optional `--chunk <chunk-id>` | [Execution](references/execute.md), including code review |
| `init` | `<owner/repo>` and a feature name | [Setup](references/setup.md) |
| `lint` | One or more Markdown paths, such as a feature issue's working copy | [Lint](references/lint.md) |
| `close` | `<feature-issue>` | [Completion](references/finish.md) |
| `ship` | Current branch and an explicitly authorized destination | [Publishing](references/ship.md) |
| `cleanup` | An explicitly identified worktree | [Cleanup](references/cleanup.md) |
| `explain` | Recent review findings | [Remaining questions](references/questions.md) |
| `resolve` | Recent findings and the user's resolutions | [Remaining questions](references/questions.md) |

Review a feature together with its supporting documents when relevant so scope, dependencies, and acceptance criteria agree.
Changes to stored shapes, parsing, or data-selection guards also use [data-flow review](references/data-flow.md), from authoring through implementation and review.
Existing in-repo specs and plans need no migration; resolve their roles through [project context](references/context.md).
Optional briefs, visions, and detailed chunk documents use the same authoring and review protocols; they are not prerequisites.
Deeper document review uses the full revision loop only when explicitly requested.
Older commands are aliases with a dependency on this skill, not additional stages.

## Working agreement

- Apply accepted local corrections automatically within the requested scope.
- Reviewers report; the orchestrator owns edits and verification.
- User instructions govern authorization; project documents calibrate judgment and do not invent additional approval gates.
- Never narrow the requested outcome merely to obtain a clean review.
- Stop dependent work when completing it needs a material scope change, a missing product decision, or new external authority; finish useful independent work first.
- A request to design, plan, review with corrections, execute, or close a feature authorizes creating and editing that feature's issue and its supporting issues; it authorizes no other issue edits or comments.
- A review verdict does not authorize commits, pushes, PR creation, PR edits, review comments, deployments, or messages.
  Honor authorization already given for those actions without asking again.
- A feature ships as a single PR per repository unless the user explicitly directs otherwise; each chunk is one commit on the feature branch, and the PR opens once the feature is complete.
  A request to execute a feature authorizes those local chunk commits; pushing and opening the PR still require authorization.
- Preserve unrelated work and do not expand a change to clean up unrelated findings.
- Verify required behavior and screen additional defensive work using [expected, evidenced, or speculative triggers](references/edge-cases.md).
- Keep each sentence of repository Markdown on its own line; write issue and PR text in ordinary paragraphs, since GitHub renders their single newlines as hard line breaks; use the project's vocabulary in both.

## Handoff

Follow the [review handoff and checkpoint lifecycle](references/review.md#result-and-human-handoff), reporting the artifact, verification, and unfinished work.
Distinguish a completed review from a completed implementation.
Present review state as temporary bookkeeping, never as a decision log or source of authority.
