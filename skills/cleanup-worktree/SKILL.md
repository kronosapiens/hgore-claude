---
name: cleanup-worktree
description: Remove one requested worktree with local data preservation using development-workflow.
---

# cleanup-worktree

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `cleanup` operation with these inputs: `$ARGUMENTS`.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Resolve the exact target and preserve local work.
Do not perform orphan-directory or container sweeps.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent claude-code`.
Do not fetch instructions or install dependencies implicitly.
