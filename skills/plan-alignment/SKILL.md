---
name: plan-alignment
description: Evaluate architecture directions within development-workflow design review.
---

# plan-alignment

Compatibility alias for the installed development-workflow skill.
Read [development-workflow](../development-workflow/SKILL.md) and follow its `design` operation with these inputs: `$ARGUMENTS`.
Load its referenced instructions relative to that skill's directory, not this alias.
Do not invoke a second skill or agent merely to forward the request; continue in the current orchestrator session.

Work from the feature's design and implementation plan, whether inline or in supporting documents.
Resolve ordinary technical choices through the automated loop; escalate only material scope or unresolved product decisions.

Interpret natural-language intent using the primary skill; explicit paths and arguments are optional shorthand.
These aliases preserve command names, not the old mandatory artifact chain, flags, or cache formats.
If the dependency is absent, report it and give the installation command:
`npx skills add kronosapiens/hgore-claude --skill development-workflow --agent claude-code`.
Do not fetch instructions or install dependencies implicitly.
