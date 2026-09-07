# {title} — Implementation plan

Feature: [Feature definition]({feature_link})
Status: draft

## Approach

Describe the implementation shape and relevant project conventions.

## Chunks

| Chunk | Repository | Depends on | Work | Status | Acceptance evidence |
|---|---|---|---|---|---|

Add one row per coherent change.
Use comma-separated chunk identifiers in Depends on, or `—` when there is no dependency.
Several sequential chunks may touch the same file.
Keep later implementation details coarse until the code they depend on exists.

## Verification

Name the repository checks and observable outcomes that demonstrate completion.
Connect chunk evidence to the feature's acceptance criteria and verify their combined behavior.
Record unavailable checks and remaining questions explicitly.
