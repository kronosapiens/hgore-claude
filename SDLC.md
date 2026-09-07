# Workflow contract

The [README](README.md) covers installation and commands.
The executable instructions live in [development-workflow](skills/development-workflow/SKILL.md).
Describe intent in natural language after `/development-workflow`; operation names and flags are optional shorthand.
The orchestrator infers the selected feature, requested stage, and artifacts from the conversation and project context, asking only when missing information materially changes the work.
This routing preserves the user's scope and authorization limits.

## Artifacts and judgment

Organize work around a feature: a bounded delivery effort with an observable outcome and completion point.
Start with one feature document containing scope, acceptance criteria, design, implementation chunks, and verification evidence.
Read existing project guidance and code before drafting it.
Use a descriptive feature name and select relevant documents by purpose and scope.
New features do not require sequential spec versions, and existing specs and plans can supply context or describe the selected effort without migration.

Separate designs, implementation plans, briefs, visions, and chunk documents are optional aids for larger work.
Link supporting documents from the feature and a separate plan back to the feature, keeping each detail in one owning document.
Small changes do not need the whole document hierarchy.
Chunk boundaries follow behavior, dependencies, and reviewability, not fixed file counts, banned words, or a universal one-chunk/one-PR rule.
Sequential chunks may touch the same files.
Parallel work requires genuinely independent changes or explicit coordination.

Keep feature rationale beside its design while work is underway.
At completion, update maintained project docs with delivered behavior and enduring rationale, using inline comments where appropriate.
Completed feature documents and Git history explain how the work evolved; maintained docs describe the current system.
Neither a decision log nor a previous approval can override current evidence or user instructions.
Project priorities calibrate review severity; an alpha project should not accumulate compatibility layers merely to coordinate deployment.
Record real operational coordination concerns in PR descriptions instead.

Follow project status conventions, or use `draft`, `active`, and `complete` for the feature lifecycle.
Review readiness does not imply implementation or feature completion.
Close a feature only when its acceptance criteria are verified, including the combined outcome across chunks, and relevant maintained docs are updated.
Keep unverified scope incomplete; only the user can authorize deferring a required outcome.
Later enhancements normally begin a new bounded feature based on maintained docs and current code.

## Automated adversarial review

The orchestrator owns the artifact, edits, and verification.
Fresh reviewers independently try to falsify it against the requested outcome, project guidance, and repository evidence.
They do not edit, inherit the author's defense, see each other's initial findings, or launch additional agents.
Bundled perspectives work without mandatory project persona files.

Each run has a bounded revision phase and a separate final audit:

1. Establish scope, authorization, artifact version, verification commands, and the round budget.
2. Launch two fresh reviewers in parallel, optionally three for a distinct additional perspective.
3. Investigate each finding and accept, reject, or leave it unresolved with evidence.
4. Apply accepted corrections locally and verify the affected behavior.
5. Repeat while material concerns or edits need independent review, up to three rounds by default.
6. Have one new reviewer audit the complete final artifact without previous verdicts or the orchestrator's defense.

The final audit is outside the revision budget and does not permit another edit cycle.
An accepted or unresolved material audit finding produces an incomplete handoff, not an unbounded retry.
Optional stylistic preferences do not prolong the loop.
Rejected findings need factual rebuttals; agreement, prior acceptance, and absence of evidence are not rebuttals.

Ordinary disagreements stay inside the automated loop.
The orchestrator does not ask the user to choose between initial reviewer opinions.
It stops dependent work only when a material product choice, scope expansion, or new authority is genuinely necessary.
An explicit findings-only request disables local revisions.

Temporary run state preserves the round count, artifact basis, pending findings, and authorization through compaction.
It is not committed or treated as durable authority and is removed at handoff unless the user requests a paused run.
Compaction and newly discovered findings do not reset the budget.

## Verification and handoff

Structural lint checks common local links and explicit dependency graphs, not prose heuristics.
Repository-required checks still apply, with pre-existing failures distinguished from regressions.
Verification must cover the behavior affected by corrections, not merely the edited lines.

The possible handoffs are:

- `ready for user review`: the final audit ran, required checks passed, and every material finding is resolved or rejected with evidence.
- `needs input`: a material product, scope, or authorization decision remains.
- `review incomplete`: material findings remain, required checks could not finish, or independent reviewers were unavailable.

Report consequential changes, important rejected findings, remaining questions, verification, rounds used, and requested versus observed models.
Include measured time and usage when available, without inventing cost or model observations.
A ready design is not an implemented feature, and a ready local implementation is not a shipped PR.

## Execution and publishing

An implementation request authorizes the selected feature scope and its automatic local code-review loops.
Honor whether the user requested one chunk, the next ready chunk, or the whole feature.
For a whole-feature request, continue through ready chunks and verify the overall outcome before closure.
Review the actual local diff, including relevant staged, unstaged, and untracked changes; an existing PR is not required.
Preserve unrelated work, and use a worktree only when isolation helps.
No special completion marker or duplicate chunk document is required when the feature or supporting plan already supplies sufficient detail.

A review or implementation request alone does not authorize Git commits, pushes, PR publishing, merges, or deployments.
Honor explicit existing authority without repeatedly asking for it.
An authorized PR includes the outcome, review and verification evidence, limitations, and any operational coordination notes.
Completion updates describe the delivered feature and carry current knowledge into maintained docs.
