# Automated review and revision

Read [reviewer.md](reviewer.md) and the relevant [perspectives](perspectives.md).
Use the validated configuration and [model routing](models.md).
Review the requested artifacts or code, with local corrections enabled by default.
An explicit user request for findings only overrides automatic revision.

## Establish the review

1. Identify the requested outcome, artifact paths, relevant repositories, and verification commands.
   Read the selected feature, relevant maintained docs, and any supporting design or implementation plan.
   Design and planning may be inline in the feature; separate files are unnecessary.
2. For code, resolve the diff against the requested base or the PR's actual base, including relevant staged, unstaged, and untracked task files.
   Snapshot Git status and existing changes so the agent can distinguish its edits from unrelated work.
   If there is no PR, review the local diff normally; creating a PR is not a prerequisite.
   A dirty tree is not itself a blocker when the task's changes can be separated.
3. Run applicable deterministic lint or repository checks.
   Record pre-existing failures separately and use evidence when deciding whether a change caused them.
4. Choose two perspectives from the work's actual concerns, or three if needed.
   Each reviewer reads the relevant project instructions, feature, maintained docs, and code directly.
   Optional project persona files supplement the bundled perspectives; their absence never blocks review.
5. Create one temporary run directory in a permitted project scratch location and a small state file inside it.
   For example, use `mktemp -d "<project-root>/.development-workflow-run.XXXXXX"` and exclude that exact directory from staging.
   Do not assume a global temporary directory is within the host's deletion permissions.
   Record canonical repository roots, artifact paths and hashes or diff basis, authorization scope, configured models, round limit, and current round.
   Keep pending findings and their dispositions there to survive context compaction.
   Store no credentials, source payloads, or copied project documentation in this state.

Temporary state is progress tracking for this run.
It does not create binding decisions, suppress new findings, or replace current project documents.
Resume the same run with its remaining budget; context compaction or a new finding does not reset the counter.
If its artifact basis changed externally, reconcile the actual changes before continuing and invalidate affected earlier checks.

## Revision rounds

Run up to `max_rounds` rounds, three by default.
Do not return to the user between ordinary rounds.

1. Increment and persist the round counter before launching reviewers.
2. Launch the selected reviewers in parallel as fresh agents on the same artifact version.
   Give them the [reviewer prompt](reviewer.md), perspective, scope, relevant paths, and verification evidence.
   Give neither the author's defense nor other reviewers' findings.
   Let them form an initial assessment before supplying prior findings for a targeted completeness check if needed.
3. Evaluate the findings against the code and intended outcome.
   Deduplicate overlapping findings without discarding distinct failure modes.
   For each, record `accept`, `reject`, or `unresolved`, with concise evidence.
   Rejection needs a factual reason; an earlier approval or decision is not a reason.
   A reviewer disagreement is something the orchestrator should investigate, not an automatic request for human arbitration.
4. Apply accepted local fixes, addressing the cause and affected callers within scope.
   Update rationale in the owning doc or code comment when needed.
   Revise coupled feature, design, or plan sections when authorized so the artifacts remain consistent.
   Do not weaken the requested outcome, rewrite governing user constraints, or grow the task to resolve a finding.
5. Verify the edits and run the relevant checks.
   A failed check or a fix that creates a new defect remains pending for the next round.
   Re-check the behavior affected by each accepted fix, not just the edited sentence or line.
6. Persist the round result and pending findings.
   Continue when substantive defects remain or accepted edits need independent review.
   End the revision phase early after a round with no material findings or edits.

Reviewers may find a defect in unchanged text; they need not explain why an earlier reviewer missed it.
Prior acceptance provides no immunity, and findings on new edits receive no automatic severity discount.
A supported rejected finding can be closed; lack of evidence leaves a material concern unresolved.
Optional style preferences do not drive additional rounds.

## Fresh final audit

After the revision phase, launch one fresh reviewer over the complete final artifact and its affected context.
Supply the intended outcome, relevant project docs, code/diff, and actual verification results.
Do not supply prior verdicts, disposition history, or the orchestrator's defense.
The audit uses the configured reviewer model and sits outside the revision-round budget: at most three revision rounds plus one audit by default.

The final auditor reports independently and does not edit.
The orchestrator may verify or reject an audit finding with evidence, but makes no further edits within this run.
Any accepted or unresolved material audit finding leaves the run incomplete and is presented to the user.
Do not hide an extra revision round in final-audit remediation.
A material missing decision or external permission ends the dependent work; finish useful independent work and report what is needed.

## Result and human handoff

- `ready for user review`: the final audit ran, required verification passed, and every material finding is resolved or rejected with evidence.
- `needs input`: a material product/scope/authorization decision is required.
- `review incomplete`: the budget ended with material findings, the final audit found an unresolved defect, required checks could not be completed, or independent reviewers were unavailable.

Report the artifact or diff, consequential revisions, important rejected findings and their evidence, remaining questions, verification, round count, and configured/requested/observed models.
Include measured time and usage when the host exposes them; label unavailable cost or token figures as unavailable.
Human approval concerns this mature result, not every intermediate suggestion.
On handoff, remove only the exact run-state file, then use `rmdir` on the exact empty run directory; never recursively delete the directory.
The session transcript carries the review report.
Keep it only if the user requests a paused run to be resumed, and identify its exact path.
Do not automatically commit, push, update a PR, post a verdict, merge, or advance from reviewed design into implementation.
If the user's existing request already authorizes the next action, continue under that authorization.
