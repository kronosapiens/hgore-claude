---
name: plan-lint
description: Check Markdown links and explicit dependency graphs with development-workflow structural lint.
---

# plan-lint

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `lint` operation with these inputs: `$ARGUMENTS`.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Use the bundled offline helper; no model reviewers are needed for lint.

Use explicit artifact paths and the primary skill's argument conventions.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent claude-code`.
Do not fetch instructions or install dependencies implicitly.
