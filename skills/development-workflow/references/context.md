# Project context and scope

Resolve the project root and inspect Git status before editing.
Read applicable AGENTS.md and CLAUDE.md instructions, then the docs relevant to the task and the code they discuss.
For several repositories, record each root and give every reviewer the relevant paths in each repository.
Keep one feature issue in the owning repository with explicit repository ownership of each change; other repositories reference it as `owner/repo#N`.

## Select and edit the feature

A feature is a GitHub issue in the repository that owns it, labeled `feature` or with the project's established label for feature specs.
Its body is the feature document: outcome, scope, acceptance criteria, design, the implementation plan as a task list or chunk table, and verification evidence.
Identify the feature from the user's request, conversation, an issue number or URL, or by searching open issues with the label, such as `gh issue list --label feature`.
When several features could match and the conversation does not select one, ask rather than choosing by title, number, or recency.
Resolve Markdown links relative to their document and command-line paths relative to the invocation directory.

A supporting document that warrants its own unit, such as an optional brief, vision, or detailed chunk document, is its own issue, linked from the feature issue.
Keep each piece of information in its owning document rather than duplicating it.
Existing in-repo specs and plans remain readable project context, but new feature work goes in an issue.
A broad or versioned spec is project context, not an instruction to implement every outstanding change or create the next version.
Preserve explicit requests to review or edit an existing spec as scoped document work.

To edit an issue body, fetch it to a working copy with `gh issue view <N> --json body -q .body > <copy>`, edit the copy, and push it back with `gh issue edit <N> --body-file <copy>` after corrections so the issue never lags the reviewed version.
Keep the working copy in the run directory that [the review procedure](review.md#establish-the-review) describes, creating that directory when authoring starts if no review has started.
Reviewers and lint read the working copy; the review state records the issue number and the copy's hash as the artifact basis.
GitHub caps an issue body at 65,536 characters; when the body would exceed it, the plan moves to the issue's first comment, edited by its id with `gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<copy>`.

## Feature lifecycle and maintained docs

An open feature issue is in progress; a closed one is complete and kept as the historical record.
Closing requires verified feature acceptance and updated maintained docs.
Review readiness is separate from whether the issue is open or closed.
Keep unfinished or unverified work visible, and do not close a feature merely because its task list is checked off.
Later enhancements normally begin a new bounded feature that builds on current behavior.

Determine each document's purpose and status from project guidance and its contents: current behavior, intended direction, an active change, or historical context.
Do not infer authority from a filename, directory, or the word maintained.
Preserve forward-looking design documents and distinguish delivered behavior from remaining intent when updating them.
Use code and verification to establish what runs today, and the user's request and applicable design guidance to establish what should change.
Completed features normally supply historical context; a project may keep an older document active explicitly.

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

Read the project's maturity, compatibility promises, deployment model, and recovery requirements before choosing mechanisms.
Keep simple implementation as the default where no stronger requirement applies.
Record ordinary deployment coordination in PR notes; add compatibility behavior when a concrete project requirement, such as overlapping application versions or supported external clients, needs it.
Name that requirement and the affected consumer rather than assuming either atomic deployment or mandatory compatibility layers.
