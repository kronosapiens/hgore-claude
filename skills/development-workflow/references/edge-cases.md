# Correctness and defensive work

Verify explicit user requirements and ordinary supported behavior in proportion to their consequence.
Filtering, sorting, rendering, and other feature behavior deserve verification even when a defect would neither lose data nor cross a boundary.
The screening below governs additional defensive machinery, not whether the requested feature works.
An agent cannot turn a speculative scenario into a requirement merely by adding it to a plan or acceptance list.

## Frequency

Before adding defensive machinery, classify the trigger against a relevant operation: a submission, a sync item, or a job run.

| Category | Evidence | Treatment |
|---|---|---|
| Expected | The trigger is part of normal supported use, such as ordinary input variation, routine concurrency, or known service behavior | Assess consequence and existing recovery |
| Evidenced | An incident, reproduction, or relevant documentation establishes an unusual failure | Assess consequence and likely recurrence in this project |
| Speculative | The scenario is merely possible, particularly when it needs several independent unusual events | Default to no additional machinery |

A plausible story or named user is not evidence of frequency.
Explain why the trigger is ordinary or what demonstrates that it occurs; documentation of a possibility alone does not establish likely recurrence.
Multiple independent unusual events lining up are presumptively speculative; events caused by the same failure are not independent coincidences.
Use observed rates when available, but do not invent probabilities or conduct a statistical study merely to justify a guard.
When evidence is weak, prefer the simpler implementation and state a consequential limitation only when a reader would otherwise assume it is handled.
If a vendor behavior can be checked directly, inspect it before adding code for it.

Two exceptions apply to speculative frequency: security is evaluated against an attacker's behavior, and a persistent failure is evaluated by its repeated consequences after the initial trigger.
Name the concrete exposed mechanism or condition that remains stuck; the words security or persistence alone do not establish an exception.

## Consequence and findings

Expected or evidenced does not automatically mean additional handling is warranted.
If existing recovery meets the feature's correctness, timeliness, and durability requirements, leave additional machinery out.
A retry is not sufficient when it cannot restore the required result or undo an improper disclosure.
Follow the project's actual requirements under [project context](context.md); do not invent stricter reliability promises.

A finding is `material` when it demonstrates a failure of required behavior, a consequential defect or security exception supported by this standard, or substantial unnecessary machinery with a concrete cost.
Use `optional` for improvements that do not establish such a failure or cost.
Unsupported speculative hardening is not a finding.
The [review procedure](review.md) owns how findings are handled and when work stops.

## Verification and removal

Choose tests from observable behavior and meaningful regression risks rather than individual design sentences or implementation predicates.
Use as many distinct cases as the behavior needs; avoid duplicate proofs and arbitrary test counts.
Additional defensive handling earns a test when it earns code under this standard.

Assess simplification by its effect on behavior, not the number of lines removed.
Removing or tightening a predicate can change accepted inputs, selected records, permissions, or disclosures; trace those effects using [data-flow review](data-flow.md).
A behavior-preserving removal needs evidence that required behavior still holds, without inventing a new edge case to justify the cleanup.
