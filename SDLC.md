# Workflow contract

The [README](README.md) covers installation and commands.
The executable instructions live in [development-workflow](skills/development-workflow/SKILL.md).
Describe intent in natural language after `/development-workflow`; operation names and flags are optional shorthand.
The orchestrator infers the requested stage and artifacts from the conversation and project context, asking only when missing information materially changes the work.
This routing preserves the user's scope and authorization limits.

## Artifacts and judgment

Start with a durable spec describing the outcome, constraints, boundaries, and acceptance criteria, plus an implementation plan describing the work and verification.
Read existing project guidance and code before drafting either.
Select the relevant documents by purpose and scope, not by assuming the highest-numbered spec governs everything.

Briefs, visions, and separate chunk plans are optional aids for genuinely larger work.
Small changes do not need the whole document hierarchy.
Chunk boundaries follow behavior, dependencies, and reviewability, not fixed file counts, banned words, or a universal one-chunk/one-PR rule.
Sequential chunks may touch the same files.
Parallel work requires genuinely independent changes or explicit coordination.

Keep important current rationale in the owning spec or a useful inline comment.
Use Git history for how the work evolved.
Neither a decision log nor a previous approval can override current evidence or user instructions.
Project priorities calibrate review severity; an alpha project should not accumulate compatibility layers merely to coordinate deployment.
Record real operational coordination concerns in PR descriptions instead.

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

An implementation request authorizes the selected plan chunk and its automatic local code-review loop.
Review the actual local diff, including relevant staged, unstaged, and untracked changes; an existing PR is not required.
Preserve unrelated work, and use a worktree only when isolation helps.
No special completion marker or duplicate chunk document is required when the plan already supplies sufficient detail.

A review or implementation request alone does not authorize Git commits, pushes, PR publishing, merges, or deployments.
Honor explicit existing authority without repeatedly asking for it.
An authorized PR includes the outcome, review and verification evidence, limitations, and any operational coordination notes.
Completion updates describe what actually happened rather than sealing a plan permanently against future evidence.
