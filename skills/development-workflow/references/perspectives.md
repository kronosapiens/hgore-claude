# Review perspectives

Select perspectives after reading the project, not by a keyword table.
Use two reviewers normally; a third should have a distinct reason to exist.
One reviewer can cover related concerns.
Project persona files are optional supplements and should point to current guidance rather than reproduce it.

## Architecture and boundaries

Inspect ownership, interfaces, dependencies, state and write paths, and separation of mechanism from judgment where the project uses that distinction.
Check whether a new abstraction removes real duplication and whether each chunk has a coherent purpose.
For a repository split, account for every moved responsibility and both sides of each contract.

## Behavior, scope, and testing

Trace the requested outcomes through the design, plan, and implementation.
Look for omissions, weakened success criteria, regressions, and tests that only restate the implementation.
Distinguish a real observable result from a completed code path.
For model-backed behavior, require evaluation criteria appropriate to the user's outcome rather than textual similarity alone.

## Data and security

When relevant, inspect identity, provenance, tenant/contributor boundaries, authorization, validation, erasure, and external data flows.
Distinguish implemented guarantees from future intentions in project docs.
Prefer mechanisms and existing project controls over adding speculative policy machinery.

## Product and interface

Inspect user intent, flows, failure states, accessibility, and the project's design conventions where the change has a user interface.
For a backend-only task, do not invent UI requirements.
