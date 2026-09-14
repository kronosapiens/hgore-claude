# Data flow and boundary changes

Use this guidance when changing a stored or wire shape, its parsing, or a guard controlling which data is accepted, selected, or sent.
Discovering the affected flow is ordinary impact analysis, before scoring possible defects against the [edge-case standard](edge-cases.md).

## Discover the consumers

Search for the underlying store, fields, and accessors as well as changed symbols.
Follow producers through parsing and persistence to readers and outbound destinations, including background jobs, projections, and relevant services in other repositories.
For a selection change, identify the newly included records and where they go.
Keep a concise inventory in the existing feature, plan, or implementer brief: the relevant paths, what each consumes or produces, and whether it changes or why it remains compatible.
This is evidence for the current change, not a permanent dependency registry.

The author discovers the flow, the implementer verifies and extends it, and the reviewer independently searches the code before comparing with the supplied inventory.
A brief's file list is a starting point, never evidence that no other consumer exists.
Report inaccessible consumers as verification gaps; do not silently assume compatibility or expand implementation authority into another repository.

## Trace behavior

Follow a representative value accepted by the proposed input through storage to its consequential consumers.
Include distinct changed shapes or selection paths where they affect the outcome; one convenient value need not exercise the whole change.
Inspect unchanged consumers to discover defects, without requiring a finding in advance.
Check what a value means at each boundary: absent, empty, and clear may differ, and a display label may not be a stored code.
Parsing establishes shape; provenance, authorization, and permission to disclose remain separate concerns.

Name what an existing guard prevents and what becomes possible when it is removed or relaxed.
Establish the parsing and shared interpretation that new consumers need before exposing them to the change.
Separate a reshape from a change in accepted or shared data when each can be implemented and reviewed coherently on its own.
Do not impose one PR per behavior when the changes need to land together.

## Verify the flow

Use behavioral checks across the affected components where isolated tests would miss a consequential consumer.
Choose assertions from the user-visible or stored result, including what crosses a boundary, under the edge-case standard.
Keep known architectural seams mechanically checkable when a small existing lint rule or check can enforce them.
A symbol search or passing schema test does not establish that every consumer handles the value correctly.
Report which paths were traced and which outcomes were verified or remain unverified.
