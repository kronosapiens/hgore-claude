---
name: plan-author
description: Author optional chunk details in a feature or implementation plan using development-workflow.
---

# plan-author

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `chunk` operation for the user's request.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Select the named chunk; write a section unless the user requested a separate file.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command for the current host:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent <host-agent>`.
Replace `<host-agent>` with the installer identifier, such as `codex` or `claude-code`.
Do not fetch instructions or install dependencies implicitly.
