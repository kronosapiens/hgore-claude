# Edge cases

An edge case earns code by its consequence and its likelihood, never by the fact that someone thought of it.
Score every candidate — in a design, a brief, a review finding, or a test — before it becomes any of those.

## Likelihood

Estimate how often the scenario arises per ordinary act of the person using the feature: a click, a submission, a connection, a message read.
For background work, count per item processed on their behalf: a record synced, a message judged, a job run.
A scenario that arises in fewer than one in a thousand such acts is not a bug.
It earns no code, no test, and no review finding; at most a sentence in the design naming the cost, when a reader would otherwise assume it is handled.
A stack of independent coincidences — a rare recovery path, during which the user also did something unusual, followed by a third unrelated event — is below the floor by construction.
Two things are not measured at the user's rate: a security class, whose rate is the attacker's, and a failure that persists, which once it happens happens on every run after, so its rate is measured from then on.

## Consequence

Above the floor, the consequence decides.

- **Tier 1 — code.** A security class (injection, a credential used across users or tenants), or a process that sticks with no run or act that ever clears it.
- **Tier 2 — code when a named person reaches it in ordinary use.** A record lost or wrongly written, or data crossing a user, tenant, or system boundary.
  A named person is a user doing a thing the product invites: a colleague continuing a thread, a user with a second address, a user scheduling an action.
  Without one, the outcome is a sentence in the design naming the cost, and nothing else.
- **Tier 3 — nothing.** Anything the design already recovers from: the next run, the next click, the user's retry.
  A 500 on a hand-typed URL, a stale count until the next run, a wrong label until the next sync.
  No code, no test, and no design sentence unless a reader would otherwise assume it is handled.

A change that strictly narrows existing code — a tighter predicate, a branch removed — may be taken at any tier, since it removes rather than adds.

## Corollaries

- **Reality before guards.** A vendor or environment behavior that a pilot or a manual check can observe — an address form, an encoding tolerance, what a scheduled action looks like — is checked before any code guards it.
- **One test per behavior, not per sentence.** Only tier 1 and tier 2 code earns a test, and the test proves the consequence, not the predicate.
- **In review, `material` means tier 1, or tier 2 with the person and the rate named.** Everything else is `optional`, and an optional finding is never applied in the round it was found; it goes to the handoff's follow-up list for the user.
- **In a design, name the cases that earn code and the costs declined.** Do not enumerate every conceivable case; each named case tends to become a code path, a test, and a finding.
