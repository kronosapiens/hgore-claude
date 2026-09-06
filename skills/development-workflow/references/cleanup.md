# Clean up a requested worktree

Resolve the exact registered worktree and its main checkout with `git worktree list`.
If the user states it is merged, use that statement without repeatedly checking GitHub.
Before removal, inspect local changes and whether any commits would become unreachable.
Keep a branch containing unmerged or otherwise unretained commits rather than force-deleting it.

Run removal from outside the target worktree using its validated absolute path.
Use `git worktree remove` without force.
A dirty tree requires preserving or explicitly resolving its work before deletion.
Delete the associated local branch with `git branch -d` only when safe; a squash-merged branch that Git refuses to delete can remain for separate handling.

Do not sweep unrelated worktrees, directories, containers, or volumes.
Only remove a dedicated stack when the user requested its cleanup and its exact ownership is verified.
Never infer disposable data from a naming pattern alone.
Report what was removed and what remains, including recovery via retained branches when relevant.
