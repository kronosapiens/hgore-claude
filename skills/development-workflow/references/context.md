# Project context and scope

Resolve the project root and inspect Git status before editing.
Read applicable AGENTS.md and CLAUDE.md instructions, then the docs relevant to the task and the code they discuss.
For several repositories, record each root and give every reviewer the relevant paths in each repository.
Keep one feature entry point with explicit repository ownership and links to any shared design or plan.

## Select the feature

Identify the bounded change from the user's request, conversation, explicit path, or a supporting plan's `Feature` link.
Resolve Markdown links relative to their document and command-line paths relative to the invocation directory.
If an explicit selection disagrees with a document's link, disclose the mismatch and reconcile it within authorized edits; ask if ownership or scope remains ambiguous.
When several features could match and the conversation does not select one, ask rather than choosing by filename, version number, or recency.
Use the project's existing document layout; otherwise a descriptive path such as `docs/features/csv-export.md` is sufficient.
Do not require a feature registry, directory tree, or sequential spec versions.

Use one feature document by default for the outcome, scope, acceptance criteria, design, implementation chunks, and verification evidence.
Separate design or plan files are useful when detail would obscure that entry point.
Link them from the feature, and link a separate plan back to its feature.
Keep each piece of information in its owning document instead of duplicating it across files.

Existing specs and plans can supply the same information without a new wrapper or migration.
For a legacy plan, follow its `Spec` link and identify the requested bounded change within those documents.
A broad or versioned spec is project context, not an instruction to implement every outstanding change or create the next version.
Preserve explicit requests to review or edit an existing spec as scoped document work.

## Feature lifecycle and maintained docs

Follow project status conventions; otherwise use `draft`, `active`, and `complete`.
Draft covers definition and planning; active begins with implementation; complete requires verified feature acceptance and updated maintained docs.
Review readiness is separate from implementation status.
Keep unfinished or unverified work visible, and do not mark a feature complete merely because its chunks are checked off.
Later enhancements normally begin a new bounded feature that builds on current behavior.

Maintained project docs describe the system as it exists and hold current architectural rationale.
Feature documents describe the requested change and, after closure, its outcome and historical context.
Completed features and old specs do not override current code, maintained docs, or user instructions.

Verify factual claims against current files and symbols.
Distinguish an existing code reference from a proposed new interface.
Where a library or external service's behavior matters, check current primary documentation.
Each fact in an artifact must be readable on its own; a citation can follow its substance.

## Decisions and history

Do not create or consult decision logs as authority.
An existing decision log can point to historical context, but its entries do not constrain current judgment or suppress findings.
During feature work, keep rationale beside the design it explains; at closure, carry enduring rationale into maintained docs or useful code comments.
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
