# Remaining questions

Use the recent review report or the user's supplied findings.
If neither is available, ask for the artifact or report that needs attention rather than inventing blockers.

For `explain`, summarize the material unresolved questions, their evidence, and a recommended choice.
Group questions when one answer resolves several of them.
Explaining is read-only and does not restart the review loop or apply changes.

For `resolve`, investigate each material question using current project code, documents, and primary sources when needed.
Apply the user's selected resolution or an ordinary technical correction already within the requested scope.
Keep current rationale in the owning spec or code comment.
If the user is asking only for recommendations, present them without editing.
After authorized edits, run a new bounded review when the user has requested continued implementation or review.
Do not reset an unfinished run's counter just to evade its limit.
If a previous run already handed off at its limit, the user's request to resolve and continue authorizes a new run.
No decision log is created.
