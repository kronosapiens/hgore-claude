# Model routing

Model roles and the round budget come from `config.json`, overlaid by the project configuration and explicit user choices.
The default is Fable orchestration with Opus review.
Use the current explicitly selected orchestrator when the user has chosen one.
This pack does not implement a cross-provider agent runner.

## Claude Code

Start the default session with `claude --model fable`, or select `/model fable` in an existing session.
The configuration's `orchestrator_model` is the requested session model, not an API that switches the active session.
If the selected model differs, disclose it; do not claim configuration alone changed the model.
Resolve a material unavailable-model mismatch before spending the review budget.

For every reviewer, pass the resolved `reviewer_model` explicitly in the Agent call's `model` parameter.
Use a fresh general-purpose agent, with read-only instructions from [reviewer.md](reviewer.md).
Do not rely on Explore/Plan defaults or inherit the expensive session model accidentally.
Two independent reviewers are the default; one serves a small change, and three when the task merits a distinct additional perspective.
The implementer that builds from the orchestrator's brief is a fresh general-purpose agent on `implementer_model`, passed explicitly in the Agent call, and is resumed across the revision rounds and the deletion round rather than re-spawned, so it keeps the context of what it built.
The deletion round and the final audit are each one new reviewer using the same configured reviewer model.
Reviewer agents must not spawn other agents; the orchestrator owns the budget.

Check host-reported model information when available, including substitution warnings and Claude Code's `/tasks` display.
Prefer an agent result's `resolvedModel` or captured host telemetry when exposed; a missing substitution warning is not a model observation.
Record requested model, observed model, and any fallback separately.
If observation is unavailable, say `observed: unavailable` rather than copying the requested name into that field.
An unexpected substitution is a routing issue to resolve, not evidence that the requested model was tested.

If the host cannot run the requested reviewers, report the limitation and prepare the review inputs without claiming an independent review occurred.
An explicitly authorized substitute may be used and must be recorded.
Never silently replace unavailable reviewers with the orchestrator reviewing its own work.

## Sources

Claude Code supports per-invocation model selection and may substitute models under organization settings.
See [subagent model selection](https://code.claude.com/docs/en/sub-agents#choose-a-model).
For session selection and Fable availability, see [model configuration](https://code.claude.com/docs/en/model-config#work-with-fable).
