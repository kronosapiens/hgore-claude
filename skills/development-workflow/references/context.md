# Project context and scope

Resolve the project root and inspect Git status before editing.
Read applicable AGENTS.md and CLAUDE.md instructions, then the docs relevant to the task and the code they discuss.
For several repositories, record each root and give every reviewer the relevant paths in each repository.
Keep one migration spec and plan with explicit repository ownership rather than duplicating the shared contract.

Accept an explicit Markdown spec path wherever it lives, including `spec/v5.md`.
Resolve a plan's Markdown `Spec` link relative to the plan file; resolve command-line paths relative to the invocation directory.
An explicit `--spec` selects the design under consideration; disclose a disagreement with an existing plan link and reconcile that link as part of the authorized plan edit.
Without an explicit path, use a plan's spec link or the uniquely identified spec relevant to the request.
Do not universally choose the highest version: some projects have overlapping specs and others designate one active version.
Follow the project's actual document roles and status conventions.

The default artifacts are a design spec and an implementation plan.
The spec carries intended behavior, boundaries, guidelines, and the rationale that still matters.
The plan carries build order, reviewable chunks, dependencies, and observable acceptance criteria.
Use existing docs when they already do these jobs.
Create an optional brief or chunk document only when it removes real ambiguity.

Verify factual claims against current files and symbols.
Distinguish an existing code reference from a proposed new interface.
Where a library or external service's behavior matters, check current primary documentation.
Each fact in an artifact must be readable on its own; a citation can follow its substance.

## Decisions and history

Do not create or consult decision logs as authority.
An existing decision log can point to historical context, but its entries do not constrain current judgment or suppress findings.
Current rationale belongs beside the mechanism in the owning spec or code comment.
Consult relevant Git history or PR discussion when a historical question affects the task; do not ingest the whole history by default.
Do not migrate or delete a project's pre-existing logs as an unrelated cleanup.

## Proportional implementation

Use the project's package manager and actual verification commands; default to pnpm only when the repo has no preference.
Prefer small changes with a coherent purpose and abstractions that remove demonstrated duplication.
Several sequential chunks may change the same file.
File ownership matters for concurrent edits, not as a permanent exclusion between chunks.
Judge concerns by behavior, not word choice, document length, or file count.

Describe deployment coordination concerns in a PR's operational notes when relevant.
Do not derive implementation choices, compatibility layers, feature flags, or additional stages from deployment sequencing.
Actual requirements such as a single consumer owning a listener remain behavioral requirements.
Do not invent whole-feature deployment assumptions either.
