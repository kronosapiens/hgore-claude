# Review perspectives

Select perspectives after reading the project, not by a keyword table.
The [review procedure](review.md) owns reviewer counts, rounds, and stopping conditions.
One reviewer can cover related concerns.
Every perspective verifies required behavior and applies the [defensive-work standard](edge-cases.md) to additional handling.
Project persona files are optional supplements and should point to current guidance rather than reproduce it.

## Architecture and boundaries

Inspect ownership, interfaces, dependencies, state and write paths, and separation of mechanism from judgment where the project uses that distinction.
Check whether a new abstraction removes real duplication and whether each chunk has a coherent purpose.
Check that required foundations precede dependent feature work and that each foundational change serves concrete consumers in the selected feature.
Check that no hand-rolled adapter, client, parser, or protocol implementation stands where a library the project could use exists.
For a repository split, account for every moved responsibility and both sides of each contract.

## Behavior, scope, and testing

Trace the feature's acceptance criteria through its design, plan, and implementation, including behavior across chunks.
Look for omissions, weakened success criteria, regressions, and tests that only restate the implementation.
Distinguish a real observable result from a completed code path.
For model-backed behavior, require evaluation criteria appropriate to the user's outcome rather than textual similarity alone.

## Data and security

When relevant, inspect identity, provenance, tenant/contributor boundaries, authorization, validation, erasure, and external data flows.
Distinguish implemented guarantees from future intentions in project docs.
Prefer mechanisms and existing project controls over adding speculative policy machinery.

## Removal

For a deletion round only.
Look for what can go without changing required behavior: tests that restate the implementation or duplicate another proof, speculative guards, abstractions that add indirection without serving a concrete need, comments narrating history, fields nothing reads, and hand-rolled adapters where an existing library serves.
Do not remove acceptance or recovery tests merely because the behavior is recoverable, or an abstraction merely because it has one caller.
Score each removal by the standard as an addition would be scored, with the evidence that nothing load-bearing depends on it.
For a guard or predicate, name the behavior it prevents and trace what removal would allow before recommending deletion.

## Product and interface

Inspect user intent, flows, failure states, accessibility, and the project's design conventions where the change has a user interface.
For a backend-only task, do not invent UI requirements.
