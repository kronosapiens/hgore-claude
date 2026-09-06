# Publish authorized changes

Confirm the user's existing authorization covers the intended commit, push, and PR actions.
A request to open a PR authorizes the necessary branch, commit, push, and PR creation for that change.
A successful review or a request to close a plan does not provide that authorization by itself.
Do not re-ask for authority already given.

Inspect Git status, the task diff, repository remotes, and any existing PR.
Select the requested destination explicitly, especially when `origin` is a fork and `upstream` is the source repository.
Resolve the target repository's actual default branch or the user's requested base; do not assume `main`.
Preserve unrelated staged and unstaged changes.
Do not publish code that has unresolved material review findings or required checks that have not passed without the user explicitly accepting that limitation.

1. Create or use the task's feature branch.
2. Stage only the task's files and review the staged diff.
3. Commit in coherent units using conventional prefixes.
   Put useful historical rationale in the commit body.
4. Push to the authorized remote without force-pushing by default.
5. Create the PR in the explicit repository, or update an existing PR only when that is authorized.
   Use a structured API body or an exact temporary body file with `gh pr create --body-file`.
   Do not reconstruct a multiline body through unsafe shell interpolation.

Lead the PR description with the concrete change and resulting behavior.
Include verification and any operational coordination notes that matter.
Do not add implementation complexity to accommodate deployment sequencing.
Do not merge unless the user asks.
Return the PR URL and material verification limits.
