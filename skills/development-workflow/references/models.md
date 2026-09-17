# Model routing

Explicit choices in the current request override standing preferences in applicable agent instructions, which override bundled `config.json` defaults for model roles and the round budget.
Accept model choices in ordinary language, such as "Use gpt-5.6-sol for implementation."
No project-specific configuration file is read or required.
The defaults are `orchestrator_model: current`, `implementer_model: auto`, and `reviewer_model: auto`.
`current` and `auto` are instructions resolved by the orchestrator, not model IDs to pass to agent tools.
The Python helper validates bundled defaults; the orchestrator applies instruction overrides and selects host models.
This pack uses native host agent tools and does not implement a cross-provider runner.

## Select models

The current session remains the orchestrator.
A concrete `orchestrator_model`, including a legacy `fable` value, records session intent; it never switches the running host model.
Disclose a mismatch without claiming configuration changed the session.

For an explicitly pinned implementer or reviewer, use that model when the host supports it.
Do not silently replace a pinned choice.
If it is unavailable, report the limitation and obtain an explicit substitute before invoking that role.

For `auto`, inspect the models actually available through the host before choosing.
Assess coding and tool capability, context needs, and task complexity before comparing cost.
Prefer a demonstrated project choice when it remains suitable; otherwise use current official model guidance and available host cost information.
Do not infer availability, prices, or capability from a model's name or remembered model lists.
For implementation, prefer a lower-cost model than the current orchestrator when it can handle the brief; do not blindly select the cheapest.
Choose reviewers independently for their ability to challenge the artifact and inspect evidence; the cheapest implementer is not automatically a suitable reviewer.
If no satisfactory cheaper implementer can be established, explain the limitation rather than inventing a candidate or silently using the expensive parent.
Prepare the brief and other independent work while any required model choice remains unresolved.

Before invocation, announce the concrete selected implementer and reviewer models and a short reason for each.
Supported choices within `auto` need no extra confirmation.
Keep selections stable for the run and report any necessary change explicitly.
Pass the selected concrete model to the host tool; never pass `auto` or rely on accidental inheritance.
For execution, delegate implementation to the selected agent with the brief described in [execution](execute.md).
Keep the same implementer through revisions and the deletion round, following [execution](execute.md) and [review](review.md).

Explicit tested model choices in the invocation or existing agent instructions are preferable when repeatability matters.
Evaluate prospective cheaper models on representative project tasks using tests, independent review, and total usage including retries.
Automatic selection does not establish equivalent quality or guarantee savings.

## Native host tools

Use fresh independent reviewer context, providing the [reviewer prompt](reviewer.md), scope, perspective, relevant paths, and verification evidence.
Do not include the author's defense or other reviewers' findings.
Reviewers must not spawn other agents; the orchestrator owns the budget.
The [review procedure](review.md) controls reviewer counts and stages.

In Codex, use the available native subagent tool with an explicit `model` and fresh reviewer context, such as `spawn_agent` with `fork_turns: none` when those fields exist.
Resume the same implementer with the host's follow-up tool.
Some Codex tools disallow model overrides when forking full history; follow the actual schema and provide the brief explicitly instead.
An API model listing alone does not establish access through the current Codex host.

In Claude Code, use a general-purpose Agent with the selected model explicitly supplied in `model`.
Resume the same implementer using the host's resume facility.
Use supported host identifiers rather than assuming every public model name is accepted.
Do not rely on Explore/Plan defaults or inherit the session model accidentally.

If native tools cannot invoke the requested independent reviewers, report the limitation and prepare review inputs without claiming independent review occurred.
Never silently replace them with the orchestrator reviewing its own work.

## Report actual routing

Record configured directives or pins, concrete requested models, observed models, and any fallback separately.
Use host telemetry when exposed, such as an agent result's `resolvedModel`, substitution warnings, or Claude Code's `/tasks` display.
A missing substitution warning is not a model observation.
If telemetry is unavailable, report `observed: unavailable` rather than copying the requested model.
An unexpected substitution is a routing issue to resolve, not evidence that the requested model was tested.
Report measured usage and cost only when exposed; otherwise label them unavailable.

## Sources

Codex supports per-agent model settings and inheritance; see [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Claude Code supports per-invocation selection and organization-controlled substitution; see [subagent model selection](https://code.claude.com/docs/en/sub-agents#choose-a-model) and [model configuration](https://code.claude.com/docs/en/model-config).
