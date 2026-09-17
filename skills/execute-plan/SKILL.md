---
name: execute-plan
description: Implement reviewed feature work and run automated code review using development-workflow.
---

# execute-plan

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `execute` operation for the user's request.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Accept implementation chunks in the feature, a supporting plan, or a separate chunk document.
Preserve whether the request covers one chunk or the whole feature.
Do not require a PR before reviewing the implementation.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command for the current host:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent <host-agent>`.
Replace `<host-agent>` with the installer identifier, such as `codex` or `claude-code`.
Do not fetch instructions or install dependencies implicitly.
