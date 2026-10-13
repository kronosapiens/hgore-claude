# Setup

The primary skill is self-contained: its configuration, reviewer guidance, templates, and scripts install together.
It does not require a root `personas/` directory or a `features/` tree.
Feature work needs the GitHub CLI (`gh`), authenticated for the repository that owns the feature.
Install through `npx skills add`, selecting `development-workflow` for the current host, such as Codex or Claude Code.
Use `--global` to make it available across projects.
The user can also point the agent directly at the primary `SKILL.md` in a local checkout.
Optional legacy aliases require the primary skill to be installed beside them.
See the repository README for the exact installation commands.

The `init` operation creates the feature issue in the repository that owns the feature:

~~~sh
gh issue create --repo <owner/repo> --title "<feature name>" --label feature --body-file "<skill-directory>/templates/feature.md"
~~~

Replace `<skill-directory>` with the absolute installed primary skill directory, as described in [the entry point](../SKILL.md#start).
Use the project's established label for feature specs in place of `feature`, creating the label first with `gh label create` if the repository lacks it.
Edit an existing feature issue through the authoring workflow instead of creating another.

No other project initialization is needed; read the project's docs, then run `design` or `plan` on the selected feature directly.
Do not install hooks, a statusline, settings overrides, or personas as an implicit setup step.
State model and budget preferences in the invocation or existing agent instructions; no project-specific configuration file is needed.
