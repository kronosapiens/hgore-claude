# Setup

The primary skill is self-contained: its configuration, reviewer guidance, templates, and scripts install together.
It does not require a root `personas/` directory or a `features/` tree.
Install through `npx skills add`, selecting `development-workflow` for Claude Code.
Optional legacy aliases require the primary skill to be installed beside them.
See the repository README for the exact installation commands.

The `init` operation scaffolds one feature document by default.
For example:

~~~sh
python3 "${CLAUDE_SKILL_DIR}/scripts/workflow.py" init <project-root> --feature docs/features/csv-export.md
~~~

Add `--plan docs/plans/csv-export.md` only when a separate implementation plan is wanted.
The target directory must already exist.
The script preflights every destination file, rejects paths outside the target, and refuses to overwrite existing files.
It creates parent directories within the target as needed.
When a plan is requested, the generated feature and plan link to each other using relative paths.
Edit existing documents through the authoring workflow instead of forcing a scaffold over them.

For an existing project, initialization is optional.
Read its docs, then run `design` or `plan` on the selected feature or existing artifacts directly.
Do not install hooks, a statusline, settings overrides, or personas as an implicit setup step.
Project-specific model/budget overrides belong in `.development-workflow.json` only when wanted.
