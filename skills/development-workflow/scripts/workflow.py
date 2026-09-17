#!/usr/bin/env python3
"""Small, offline helpers for configuration, scaffolding, and structural lint."""

from __future__ import annotations

import argparse
import json
import re
import sys
from os.path import relpath
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


BUNDLE = Path(__file__).resolve().parents[1]


def configuration() -> dict:
    config = json.loads((BUNDLE / "config.json").read_text())
    for key in ("orchestrator_model", "reviewer_model", "implementer_model"):
        if not isinstance(config[key], str) or not config[key].strip():
            raise ValueError(f"{key} must be a nonempty model name")
    if type(config["max_rounds"]) is not int or not 1 <= config["max_rounds"] <= 10:
        raise ValueError("max_rounds must be an integer from 1 to 10")
    if type(config["reviewer_count"]) is not int or config["reviewer_count"] not in (1, 2, 3):
        raise ValueError("reviewer_count must be 1, 2, or 3")
    return config


def scaffold(root: Path, feature: Path, plan: Path | None = None) -> list[Path]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")
    names = (feature,) if plan is None else (feature, plan)
    destinations = [(root / name).resolve() for name in names]
    if len(set(destinations)) != len(destinations):
        raise ValueError("feature and plan must be different files")
    if any(left in right.parents for left in destinations for right in destinations):
        raise ValueError("neither destination may be a parent of the other")
    for path in destinations:
        if not path.is_relative_to(root) or path.suffix.lower() != ".md":
            raise ValueError(f"expected a Markdown path inside {root}: {path}")
        if path.exists():
            raise ValueError(f"refusing to overwrite {path}")
        for parent in path.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"parent is not a directory: {parent}")
    feature_path = destinations[0]
    values = {
        "title": feature_path.stem.replace("-", " ").capitalize(),
        "implementation": "Use a short checklist of reviewable chunks, their dependencies, and acceptance evidence.\n"
        "Track progress here as the work is implemented and verified.",
    }
    if plan is not None:
        plan_path = destinations[1]
        values["feature_link"] = quote(relpath(feature_path, plan_path.parent).replace("\\", "/"), safe="/")
        plan_link = quote(relpath(plan_path, feature_path.parent).replace("\\", "/"), safe="/")
        values["implementation"] = f"See the [implementation plan]({plan_link}) for chunks, dependencies, and progress."
    for template, destination in zip(("feature.md", "plan.md"), destinations):
        content = (BUNDLE / "templates" / template).read_text().format(**values)
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects files created after the preflight.
        with destination.open("x", encoding="utf-8") as output:
            output.write(content)
    return destinations


def prose_lines(text: str):
    """Keep line numbers while excluding fenced code and HTML comments."""
    fence = None
    comment = False
    for number, original in enumerate(text.splitlines(), 1):
        line = original
        if fence:
            if re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
            yield number, ""
            continue
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match and not comment:
            fence = match[1]
            yield number, ""
            continue
        visible = ""
        while line:
            if comment:
                _, end, line = line.partition("-->")
                if not end:
                    break
                comment = False
            else:
                before, start, line = line.partition("<!--")
                visible += before
                if not start:
                    break
                comment = True
        yield number, visible


def cell_text(cell: str) -> str:
    cell = cell.strip().strip("`")
    match = re.fullmatch(r"\[([^\]]+)\]\([^)]*\)", cell)
    return (match[1] if match else cell).strip("` ")


def table_cells(line: str) -> list[str]:
    return re.split(r"(?<!\\)\|", line.strip().strip("|"))


def dependency_findings(lines: list[tuple[int, str]]) -> list[str]:
    findings = []
    index = 0
    while index < len(lines) - 1:
        number, line = lines[index]
        header = [cell_text(c).lower() for c in table_cells(line)]
        delimiter = table_cells(lines[index + 1][1])
        is_table = len(delimiter) == len(header) and all(
            re.fullmatch(r"\s*:?-{3,}:?\s*", c) for c in delimiter
        )
        key = "chunk" if "chunk" in header else "slug"
        if not is_table or key not in header or "depends on" not in header:
            index += 1
            continue
        graph = {}
        row_lines = {}
        index += 2
        while index < len(lines) and "|" in lines[index][1]:
            row_number, row = lines[index]
            cells = [cell_text(c) for c in table_cells(row)]
            index += 1
            if len(cells) != len(header):
                findings.append(f"{row_number}: malformed dependency row")
                continue
            slug = cells[header.index(key)]
            deps = cells[header.index("depends on")]
            if not slug:
                findings.append(f"{row_number}: empty chunk identifier")
                continue
            if slug in graph:
                findings.append(f"{row_number}: duplicate chunk {slug}")
                continue
            graph[slug] = [] if deps.lower() in ("", "—", "-", "none") else [
                cell_text(dep) for dep in deps.split(",")
            ]
            row_lines[slug] = row_number
        for slug, deps in graph.items():
            for dep in deps:
                if dep not in graph:
                    findings.append(f"{row_lines[slug]}: {slug} depends on undefined chunk {dep}")
                elif dep == slug:
                    findings.append(f"{row_lines[slug]}: {slug} depends on itself")
        # Kahn's algorithm avoids recursion limits even on long legitimate plans.
        remaining = {slug: set(deps) & graph.keys() for slug, deps in graph.items()}
        while ready := {slug for slug, deps in remaining.items() if not deps}:
            remaining = {slug: deps - ready for slug, deps in remaining.items() if slug not in ready}
        if remaining:
            findings.append(f"{number}: dependency cycle affects: {', '.join(sorted(remaining))}")
    return findings


LINK_START = re.compile(r"(?<!\\)\[[^\]]*\]\(\s*")
REFERENCE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)")


def link_targets(line: str):
    """Recognize common inline destinations and single-line reference definitions."""
    if definition := REFERENCE.match(line):
        yield definition[1].strip("<>")
        return
    for match in LINK_START.finditer(line):
        tail = line[match.end():]
        if tail.startswith("<"):
            if ">" in tail:
                yield tail[1:tail.index(">")]
            continue
        depth = 0
        destination = ""
        escaped = False
        for char in tail:
            if escaped:
                destination += char
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char.isspace() or (char == ")" and depth == 0):
                break
            depth += (char == "(") - (char == ")")
            destination += char
        if destination:
            yield destination


def lint(path: Path) -> list[str]:
    lines = list(prose_lines(path.read_text(encoding="utf-8")))
    findings = dependency_findings(lines)
    for number, line in lines:
        # Inline code frequently contains example links or proposed paths.
        line = re.sub(r"(`+).*?\1", "", line)
        for href in link_targets(line):
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.exists():
                findings.append(f"{number}: broken local link {href}")
    return [f"{path}:{finding}" for finding in findings]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("config", help="validate and display bundled model/budget defaults")
    init_parser = commands.add_parser("init", help="create a feature and optional plan without overwriting")
    init_parser.add_argument("root", type=Path)
    init_parser.add_argument("--feature", type=Path, required=True)
    init_parser.add_argument("--plan", type=Path)
    lint_parser = commands.add_parser("lint", help="check local links and explicit dependency tables")
    lint_parser.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args(argv)
    try:
        if args.command == "config":
            print(json.dumps(configuration(), indent=2))
        elif args.command == "init":
            for path in scaffold(args.root, args.feature, args.plan):
                print(path)
        else:
            findings = [finding for path in args.paths for finding in lint(path)]
            print("\n".join(findings) if findings else "Structural lint passed.")
            return int(bool(findings))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
