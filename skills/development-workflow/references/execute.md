# Implement a feature

Resolve the feature and any supporting documents through [project context](context.md), then read project guidance and current code.
Use the implementation checklist in the feature, a linked plan, or an optional detailed chunk document.
Honor whether the user requested one chunk, the next ready chunk, or the whole feature.
For the next ready chunk, use the documented order and actual dependencies; ask only when the choice materially changes scope.
For a whole-feature request, continue through ready chunks and their review loops within the existing authorization.
Check actual prerequisites in the code and available review evidence, not a mandatory approval marker or nonexistent brief.
If the selected work's current design and plan have not been reviewed, run the design review loop before implementation.
These can be sections in the feature document; separate files are unnecessary.
The request to execute authorizes implementing the selected work after that review is ready.
Do not continue into implementation from an incomplete design review.

Inspect staged, unstaged, and untracked files first.
Use the current checkout when its changes are separable from the task.
An isolated worktree is optional when it helps concurrent work or protects overlapping user changes.
Do not automatically copy credentials, provision services, start unrelated containers, or create a branch from an assumed `origin/main`.

Implement the smallest coherent change that meets the chunk's acceptance criteria.
When an implementer agent builds the chunk, the orchestrator writes it a brief: the outcome, the behaviors the chunk delivers, the files and the seams that must survive, the project rules that bite, the verification to run, and what to report back.
A brief names behaviors, never an enumerated list of tests; one test per observable behavior follows from the list, and a scenario the edge-case standard puts below its floor earns neither.
The same implementer carries the revision rounds and the deletion round, resumed with each round's accepted findings rather than re-spawned.
Use existing abstractions and update affected callers within scope.
Use an existing library before writing an adapter, client, parser, or protocol implementation by hand.
Mark the feature active when implementation begins, following the project's status conventions.
Plans guide the work and may be refined as facts become clear; keep them consistent with the feature's acceptance criteria and requested outcome.
Do not turn an ordinary implementation adjustment into a request to amend a frozen contract.

Verify in proportion to the change and run the repository's required checks.
Run long checks leg by leg rather than as one call, in the implementer's brief as in the orchestrator's own hands, so a stalled call never loses a run.
Use test-first development when a failing behavioral test usefully specifies the work.
Do not add tests merely to mirror implementation details or satisfy a blanket TDD rule.
Write one test per observable behavior, not per sentence of the design; an edge case earns a test only when it earned code under the [edge-case standard](edge-cases.md).
Record baseline failures, unavailable services, and any unverified acceptance criteria honestly.
A required check that remains unverified prevents a complete result.

Run the [review loop](review.md) over the task's complete local diff, including its uncommitted files.
The loop applies accepted fixes and repeats automatically; the orchestrator re-runs checks affected by revisions.
No PR is required to review code.
If a PR already exists, inspect it read-only and include the current local changes in the review basis.
Do not edit the PR body or publish review comments without authorization.

Update chunk progress and verification evidence in the feature or owning plan.
A complete chunk does not mean the whole feature is complete.
For a whole-feature request, advance only after the current chunk's required checks and code review are complete.
When the authorized feature scope is finished, follow [completion](finish.md) to verify the overall outcome and update maintained docs.
Handoff the reviewed diff, acceptance evidence, important changes, and remaining questions when the requested scope is finished or cannot proceed.
Proceed to [publishing](ship.md) only when the user has authorized it, including authorization already given for this task.
