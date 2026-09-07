---
name: spec-author
description: Define and review a bounded feature or revise an existing design using development-workflow.
---

# spec-author

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `design` operation with these inputs: `$ARGUMENTS`.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Use the requested Markdown path and project conventions; no fixed root filename or decomposition schema.
For new work, define a bounded feature with inline design and planning.
Honor explicit requests to revise an existing spec without advancing its version or expanding its scope.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent claude-code`.
Do not fetch instructions or install dependencies implicitly.
