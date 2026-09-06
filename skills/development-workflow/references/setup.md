# Setup

The primary skill is self-contained: its configuration, reviewer guidance, templates, and scripts install together.
It does not require a root `personas/` directory or a `features/` tree.
Install through `npx skills add`, selecting `development-workflow` for Claude Code.
Optional legacy aliases require the primary skill to be installed beside them.
See the repository README for the exact installation commands.

The `init` operation scaffolds only the two documents requested by the user.
For example:

~~~sh
python3 "${CLAUDE_SKILL_DIR}/scripts/workflow.py" init <project-root> --spec spec/example.md --plan spec/example-plan.md
~~~

The target directory must already exist.
The script preflights both destination files, rejects paths outside the target, and refuses to overwrite either file.
It creates parent directories within the target as needed.
The generated plan links its spec using a relative path.
Edit existing documents through the authoring workflow instead of forcing a scaffold over them.

For an existing project, initialization is optional.
Read its docs, then run `design` or `plan` on the appropriate paths directly.
Do not install hooks, a statusline, settings overrides, or personas as an implicit setup step.
Project-specific model/budget overrides belong in `.development-workflow.json` only when wanted.
