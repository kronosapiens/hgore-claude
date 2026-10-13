# Close a feature

Resolve the feature issue from the request, then read its acceptance criteria and available evidence.
Use the user's statement of completion and known results; do not reconstruct every commit merely to confirm a stated fact.
Distinguish reviewed, implemented, and verified work, and preserve any explicitly deferred or unverified scope.
Check the feature's combined behavior against its acceptance criteria, including integration across chunks where relevant.
Run missing required checks when possible; unverified criteria keep the feature incomplete.
Incomplete required reviews and unresolved material findings also prevent completion.
Only the user can authorize deferring required scope; never shrink the feature merely to close it.

Update relevant project docs according to their [purpose and status](context.md#feature-lifecycle-and-maintained-docs), recording delivered behavior and enduring rationale without overwriting future intent.
Use useful inline comments for rationale that belongs in code; do not duplicate the whole feature issue into project docs.
If no maintained docs cover a changed contract, add a focused document only when that knowledge needs to persist.
Record a concise completion outcome and verification evidence in the issue body, linking updated docs where useful.
The feature completes when its issue closes, which requires verified acceptance and finished doc updates.
The implementing PR's `Closes #<N>` closes it at merge; when the user asks to close the feature and no PR remains, run `gh issue close <N> --reason completed`.

The closed issue is the historical record.
Later enhancements normally get a new feature with their own scope and acceptance criteria, using maintained docs and current code as the baseline.
Do not create a closure ledger or permanent decision history.
Follow the [review checkpoint lifecycle](review.md#checkpoint-lifecycle) for run-state cleanup; retain project artifacts unless their removal is requested or clearly part of the agreed task.

Closing a feature does not authorize a commit, push, PR update, or merge.
Use already-given authorization when it covers those actions; otherwise return the local changes for review.
