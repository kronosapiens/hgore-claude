# Authoring

Start from the user's intent and the relevant project documents and code.
Select the bounded feature and artifacts using [project context](context.md).
For new work, use one feature document with inline design and implementation planning.
The bundled [feature template](../templates/feature.md) is a starting point, not a required section schema.
Use an existing spec or plan when it already describes the requested change.

## Design

State the intended outcome, current versus proposed behavior, meaningful exclusions, and observable acceptance criteria for the whole feature.
Describe ownership, interfaces, and the mechanism at the level the work needs.
Keep present-tense rationale with the design it explains.
Choose ordinary technical details from evidence and project guidance.
Explore significant alternatives when that improves the design, then let the automated review challenge the choice.
Only a genuine unresolved product choice or material scope change needs human input.

When explicitly requested, an optional brief focuses on purpose and scope, and an optional vision focuses on product direction.
They use the same review loop without creating additional mandatory layers.

## Implementation plan

Plan in the feature's implementation section by default, using a short checklist for simple work.
Identify coherent, reviewable chunks and their dependencies, and connect each chunk's acceptance evidence to the feature's criteria.
Include verification of the combined outcome when several chunks contribute to it.
Record progress alongside the work it describes.
For multiple repositories, name which repository owns each change and contract.
Keep later chunks coarse until earlier work establishes the code they depend on.
Sequential chunks can edit the same file; isolate only concurrent edits that would conflict.
Use a small dependency table when it makes ordering clearer.
Use a separate plan when substantial detail warrants it or the user requests an output path.
Link it from the feature and back to the feature, moving implementation detail instead of maintaining two plans.
The bundled [plan template](../templates/plan.md) is an example, not a required section schema.

A chunk can be defined directly in the feature or a separate plan.
Write a separate chunk document only when substantial implementation detail deserves its own readable unit.
The execution skill can select either representation.
Optional chunk authoring is a section edit unless the user names a separate output path.

## Validate and review

Ground claims about existing files, APIs, and data in the current repository.
Describe proposed interfaces as new work, not as existing anchors.
Run [structural lint](lint.md), then the [automated review loop](review.md).
The author's normal self-check is sufficient before that loop; do not run a second mandatory author-side tribunal.
Review the feature and relevant supporting documents together when they are in scope.
Keep required outcomes fixed through revisions unless the user changes them.
Return the reviewed artifacts and consequential choices before starting implementation unless the user already authorized implementation.
