# Workflow contract

The [README](README.md) covers installation and use.
The executable entry point is [development-workflow](skills/development-workflow/SKILL.md).
Describe the intended outcome naturally; choosing an operation does not expand scope or authorization.

## Ownership of instructions

Each detailed policy has one owning reference.
This document summarizes their roles; follow the linked procedure for execution details.

| Subject | Owner |
|---|---|
| Scope, document meaning, and project conventions | [Project context](skills/development-workflow/references/context.md) |
| Feature design, foundations, and implementation order | [Authoring](skills/development-workflow/references/author.md) |
| Required correctness and additional defensive work | [Defensive-work standard](skills/development-workflow/references/edge-cases.md) |
| Producer and consumer discovery | [Data flow](skills/development-workflow/references/data-flow.md) |
| Review schedule, dispositions, stopping, and checkpoints | [Review procedure](skills/development-workflow/references/review.md) |
| Model selection, invocation, and observed-model reporting | [Model routing](skills/development-workflow/references/models.md) |
| Implementation and verification | [Execution](skills/development-workflow/references/execute.md) |
| Feature acceptance and document updates | [Completion](skills/development-workflow/references/finish.md) |
| Authorized Git and PR actions | [Publishing](skills/development-workflow/references/ship.md) |

## Features and project context

Organize work around a bounded outcome and observable acceptance criteria.
Use the project's document conventions, with one feature document as the default when no convention exists.
Separate plans and chunk documents are optional aids; they do not create extra approval stages.
Distinguish current behavior, intended direction, active work, and historical context when reading or updating documents.
Project requirements determine compatibility and recovery obligations, with simple implementation as the default when no stronger requirement applies.

Establish required foundations before their dependent feature behavior, justified by concrete consumers.
For changes to stored shapes, parsing, or selection, discover producers and consumers beyond the brief and diff.
Verify the combined feature outcome across chunks before marking it complete.
Keep rationale with its design and carry enduring knowledge into the appropriate project documents without erasing future intent.

## Review and judgment

The orchestrator owns the artifact, finding dispositions, edits, and verification.
The current agent orchestrates; automatic selection prefers a cheaper capable implementer and chooses reviewers for independent critical review.
Explicit model choices in the request or existing agent instructions take precedence over automatic selection; no project-specific configuration file is needed.
Independent reviewers inspect raw evidence and try to falsify the proposed result without inheriting the author's defense.
The bounded review procedure includes revision, an applicable removal pass, and a fresh final audit.
Ordinary disagreements are investigated within that procedure; missing product decisions or authority are surfaced to the user.

Required behavior receives appropriate verification.
Additional defensive machinery is screened as expected, evidenced, or speculative, then assessed by consequence and existing recovery.
A plausible failure story alone does not justify more code.
Review findings are evidence for judgment, not permission to publish or permanent constraints on future work.

## Handoff and continuity

Report what changed, what was verified, and what remains incomplete.
Review readiness, feature completion, and publishing authorization are distinct.
Preserve an uncommitted checkpoint for unfinished work and resume it under the review procedure's remaining budget.
Completed or explicitly abandoned runs release their temporary state; project artifacts remain according to their own lifecycle.

Local corrections stay within the user's authorized scope.
Commits, pushes, PR updates, comments, merges, and deployments require the appropriate user authorization, including authority already given.
A passing review grants none, and this pack does not require repositories to make automated review verdicts merge-blocking.
