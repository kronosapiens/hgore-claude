# Authoring

Start from the user's intent and the relevant project documents and code.
Select the bounded feature and artifacts using [project context](context.md).
For new work, create the feature issue through [setup](setup.md) and write its design and implementation plan in the body, using the [editing procedure](context.md#select-and-edit-the-feature).
The bundled [feature template](../templates/feature.md) is a starting point, not a required section schema.
Use an existing feature issue when it already describes the requested change.

## Design

State the intended outcome, current versus proposed behavior, meaningful exclusions, and observable acceptance criteria for the whole feature.
Describe ownership, interfaces, and the mechanism at the level the work needs.
For stored shapes, parsing, or data-selection changes, discover the producers and consumers using [data-flow review](data-flow.md) and include the inventory with the design.
Keep present-tense rationale with the design it explains.
Choose ordinary technical details from evidence and project guidance.
Prefer an existing library over a hand-rolled adapter, client, parser, or protocol implementation; a design that hand-rolls one names the library it considered and why it does not serve.
Explore significant alternatives when that improves the design, then let the automated review challenge the choice.
Name the cases that earn code and the costs the design declines by the [edge-case standard](edge-cases.md); do not enumerate every conceivable case, since each named case tends to become a code path, a test, and a finding.
Only a genuine unresolved product choice or material scope change needs human input.

When explicitly requested, an optional brief focuses on purpose and scope, and an optional vision focuses on product direction.
They use the same review loop without creating additional mandatory layers.

## Implementation plan

Plan in the feature issue's implementation section, or its first comment when the body is too long, using a short task list for simple work.
Identify coherent, reviewable chunks and their dependencies, and connect each chunk's acceptance evidence to the feature's criteria.
Identify foundations the feature needs: shared contracts, representations, storage access, parsing, or components that later work depends on.
Establish and verify those foundations in the earliest coherent chunk before building their dependent feature behavior.
Name the concrete later consumers that justify each foundation, and reuse existing foundations when they already serve.
If no foundational change is needed, start directly with feature work; a small feature can establish its foundation and first use in one coherent chunk.
Explain what a removed or relaxed guard had been protecting.
Include verification of the combined outcome when several chunks contribute to it.
Record progress alongside the work it describes.
For multiple repositories, name which repository owns each change and contract.
Keep later chunks coarse until earlier work establishes the code they depend on.
Sequential chunks can edit the same file; isolate only concurrent edits that would conflict.
Use a small dependency table when it makes ordering clearer.

A chunk is defined directly in the feature issue.
Write a separate chunk document, as its own issue, only when substantial implementation detail deserves its own readable unit.
The execution skill can select either representation.
Optional chunk authoring is a section edit unless the user requests a separate chunk document.

## Validate and review

Ground claims about existing files, APIs, and data in the current repository.
Describe proposed interfaces as new work, not as existing anchors.
Run [structural lint](lint.md), then the [automated review loop](review.md).
The author's normal self-check is sufficient before that loop; do not run a second mandatory author-side tribunal.
Review the feature and relevant supporting documents together when they are in scope.
Keep required outcomes fixed through revisions unless the user changes them.
Return the reviewed artifacts and consequential choices before starting implementation unless the user already authorized implementation.
