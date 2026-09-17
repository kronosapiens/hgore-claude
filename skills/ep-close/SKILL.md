---
name: ep-close
description: Verify feature completion and update the feature, supporting plan, and maintained docs using development-workflow.
---

# ep-close

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `close` operation for the user's request.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Completion does not authorize a commit or create a permanent closure ledger.
When given a plan, resolve its owning feature and check the whole requested outcome before closing it.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command for the current host:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent <host-agent>`.
Replace `<host-agent>` with the installer identifier, such as `codex` or `claude-code`.
Do not fetch instructions or install dependencies implicitly.
