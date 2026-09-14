"""Prepare one synthetic evaluation without exposing its expected result."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil


HERE = Path(__file__).resolve().parent
CASES = HERE / "cases"
REFERENCES = HERE.parents[1] / "skills/development-workflow/references"


def prepare(case: str, destination: Path) -> Path:
    available = {path.name for path in CASES.iterdir() if path.is_dir()}
    if case not in available:
        raise ValueError(f"unknown case: {case}")
    destination = destination.expanduser().resolve()
    # Never overwrite an existing evaluation or project.
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(CASES / case, destination, dirs_exist_ok=True)
    shutil.copytree(REFERENCES, destination / "instructions")
    checkpoint = destination / "checkpoint.json"
    if checkpoint.exists():
        state = json.loads(checkpoint.read_text(encoding="utf-8"))
        state["project_root"] = str(destination)
        state["artifact_sha256"] = hashlib.sha256(
            (destination / "app.py").read_bytes()
        ).hexdigest()
        checkpoint.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted(p.name for p in CASES.iterdir() if p.is_dir()))
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        root = prepare(args.case, args.destination)
    except (ValueError, OSError) as error:
        parser.exit(2, f"error: {error}\n")
    print(root)
    print("Run a fresh agent from this directory with the request in REQUEST.txt.")
    print("Keep the evaluator's README and other cases outside its context.")


if __name__ == "__main__":
    main()
