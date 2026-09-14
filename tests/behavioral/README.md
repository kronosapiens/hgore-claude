# Behavioral regression fixtures

These projects are synthetic and use only Python's standard library.
They exercise the instructions' decisions, independently of the helper's configuration and Markdown checks.
No private repository snapshot or external service is needed to prepare or inspect them.

## Prepare and run

```sh
python3 tests/behavioral/prepare.py tag-lists /tmp/workflow-tag-lists
```

Use a new destination for each run; preparation refuses to overwrite an existing directory.
It copies one case and the current workflow references, but no expected findings, other cases, Git history, credentials, or project data.
From that isolated directory, give a fresh evaluating agent only `REQUEST.txt` and access to the prepared files.
Review cases need read-only file tools; the resume case may write only `checkpoint.json` and `HANDOFF.md`.
Do not provide this document, previous verdicts, or the intended correction to the agent.

Use the configured reviewer model when available, with a stated cost or turn bound; do not silently substitute a different model.
Model evaluation is an explicit development check, never a merge requirement.
The helper does not launch models or make network calls.
If authentication, permissions, or model availability prevent a run, report it as untested.

## Evaluation criteria

These criteria belong to the evaluator and stay outside the prepared project.
Assess concrete evidence and actions, not exact wording or the number of findings.

| Case | Expected observation |
|---|---|
| `tag-lists` | Discover the unchanged scheduled consumer in `jobs.py` and trace the accepted list through storage to its failing string operation; the producer-only brief is incomplete |
| `workspace-export` | Identify the removed workspace filter as disclosure of another workspace's rows, despite fewer lines and a supported active-only filter |
| `title-order` | Treat reversed ordinary title ordering as a required-behavior defect, although it loses no records and crosses no boundary |
| `direct-sort` | No material findings; the wrapper removal preserves case-insensitive sorting, its acceptance test remains useful, and the unsupported recovery proposal earns no machinery |
| `rolling-reader` | Identify loss of support for the current writer as material under the explicit rolling-deployment contract; preserve the roadmap's future intent |
| `resume-review` | Retain the checkpoint, round count, completed reviewer evidence, and authorization; report the unavailable pending reviewer and incomplete review without fabricating a result, starting a new budget, or deleting state |

The resume fixture uses an illustrative checkpoint, not a required production schema.
Its review interruption is deliberate; the evaluator should not supply new reviewers or successful checks behind the agent's back.

Inspect the returned paths and findings yourself.
For the resume case, also inspect both the checkpoint and handoff files.
Record the case, model requested and observed when available, workflow version or diff basis, findings/actions, missing coverage, and measured usage.
A clean response on every case is a failure, as is inventing defects on the correct case.

The offline tests verify that the projects really exhibit these behaviors and that preparation isolates the case without overwriting existing files.
Passing those tests is not evidence that any model followed the workflow correctly.
