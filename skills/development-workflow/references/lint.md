# Structural lint

Run the bundled Python script on the Markdown artifacts being authored or reviewed:

~~~sh
python3 "<skill-directory>/scripts/workflow.py" lint <path>
~~~

Python 3.10+ is required; the script uses only the standard library.
Replace `<skill-directory>` with the absolute installed primary skill directory, as described in [the entry point](../SKILL.md#start).
For a feature issue, lint its [working copy](context.md#select-and-edit-the-feature); include supporting documents when they are part of the work.
Exit status is 0 for no findings, 1 for structural findings, and 2 for usage, configuration, or file errors.

The lint checks common inline local Markdown links, single-line link definitions, and dependency tables with `Chunk` (or `Slug`) and `Depends on` columns.
It checks duplicates, undefined dependencies, self-dependencies, and cycles.
Use comma-separated chunk identifiers or `—` for no dependency.
Other table columns and document sections are freeform.

Markdown links assert that their targets exist now.
Write proposed new file names as inline code until they exist; the lint does not reject a design for mentioning a future path.
An issue does not resolve repository-relative links, so a feature issue links repository files as GitHub URLs or names them in inline code.
Templates are examples and are not lint targets until instantiated.
The lint does not fetch remote URLs or try to assess implementation quality.
It does not infer a dependency graph from arbitrary prose or validate Markdown heading anchors.
Reviewers still inspect semantic dependencies, acceptance criteria, scope, and whether cited sections support their claims.

There are no gates based on the word `and`, line counts, mandatory briefs, ownership overlap, or a fixed section order.
