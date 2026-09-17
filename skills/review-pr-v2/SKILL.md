---
name: review-pr-v2
description: Review and automatically revise a PR or local code diff using development-workflow.
---

# review-pr-v2

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `review code` operation for the user's request.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Use the named PR, or the current branch's PR when one exists; otherwise review the local task diff.
An existing PR can be read without permission to change its body or post a comment.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command for the current host:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent <host-agent>`.
Replace `<host-agent>` with the installer identifier, such as `codex` or `claude-code`.
Do not fetch instructions or install dependencies implicitly.
