# Execute a reviewed plan

Read the plan, its linked or explicitly selected spec, project guidance, and current code.
Select the requested chunk from the plan table/section or an optional detailed chunk document.
If only one actionable chunk matches, use it; ask when the choice changes scope.
Check actual prerequisites in the code and available review evidence, not a mandatory approval marker or nonexistent brief.
If the current plan has not been reviewed, run the design review loop before implementation.
The request to execute authorizes implementing the selected chunk after that review is ready.
Do not continue into implementation from an incomplete design review.

Inspect staged, unstaged, and untracked files first.
Use the current checkout when its changes are separable from the task.
An isolated worktree is optional when it helps concurrent work or protects overlapping user changes.
Do not automatically copy credentials, provision services, start unrelated containers, or create a branch from an assumed `origin/main`.

Implement the smallest coherent change that meets the chunk's acceptance criteria.
Use existing abstractions and update affected callers within scope.
Plans guide the work and may be refined as facts become clear; keep them consistent with the implementation and requested outcome.
Do not turn an ordinary implementation adjustment into a request to amend a frozen contract.

Verify in proportion to the change and run the repository's required checks.
Use test-first development when a failing behavioral test usefully specifies the work.
Do not add tests merely to mirror implementation details or satisfy a blanket TDD rule.
Record baseline failures, unavailable services, and any unverified acceptance criteria honestly.
A required check that remains unverified prevents a complete result.

Run the [review loop](review.md) over the task's complete local diff, including its uncommitted files.
The loop applies accepted fixes and repeats automatically; the orchestrator re-runs checks affected by revisions.
No PR is required to review code.
If a PR already exists, inspect it read-only and include the current local changes in the review basis.
Do not edit the PR body or publish review comments without authorization.

Handoff the reviewed diff, acceptance evidence, important changes, and remaining questions.
A complete chunk does not mean the whole feature is complete.
Proceed to [publishing](ship.md) only when the user has authorized it, including authorization already given for this task.
