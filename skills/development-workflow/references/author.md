# Authoring

Start from the user's intent and the relevant project documents and code.
Use the requested paths; for a new feature, prefer the project's existing spec/plan convention.
The spec can be an existing versioned document or a focused design note.
Do not require a vision, decomposition table, or feature brief before authoring a plan.

## Design

State the intended outcome, ownership and interfaces, meaningful exclusions, and how success will be observed.
Keep present-tense rationale with the design it explains.
Choose ordinary technical details from evidence and project guidance.
Explore significant alternatives when that improves the design, then let the automated review challenge the choice.
Only a genuine unresolved product choice or material scope change needs human input.

When explicitly requested, an optional brief focuses on purpose and scope, and an optional vision focuses on product direction.
They use the same review loop without creating additional mandatory layers.

## Implementation plan

Link the spec, identify reviewable chunks and their dependencies, and give each chunk observable acceptance criteria.
For multiple repositories, name which repository owns each change and contract.
Keep later chunks coarse until earlier work establishes the code they depend on.
Sequential chunks can edit the same file; isolate only concurrent edits that would conflict.
Use a small dependency table when it makes ordering clearer.
The bundled [plan template](../templates/plan.md) is an example, not a required section schema.

A chunk can be defined directly in the plan.
Write a separate chunk document only when substantial implementation detail deserves its own readable unit.
The execution skill can select either representation.
Optional chunk authoring is a section edit unless the user names a separate output path.

## Validate and review

Ground claims about existing files, APIs, and data in the current repository.
Describe proposed interfaces as new work, not as existing anchors.
Run [structural lint](lint.md), then the [automated review loop](review.md).
The author's normal self-check is sufficient before that loop; do not run a second mandatory author-side tribunal.
Review a spec and plan together when both are in scope.
Keep required outcomes fixed through revisions unless the user changes them.
Return the reviewed artifacts and consequential choices before starting implementation unless the user already authorized implementation.
