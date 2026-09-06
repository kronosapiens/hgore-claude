#!/usr/bin/env python3
"""Compatibility entrypoint; install development-workflow beside this skill."""

import runpy
import sys
from pathlib import Path

helper = Path(__file__).resolve().parents[1] / "development-workflow/scripts/workflow.py"
if not helper.is_file():
    sys.exit("Missing development-workflow; install it alongside plan-lint.")
sys.argv = [str(helper), "lint", *sys.argv[1:]]
runpy.run_path(str(helper), run_name="__main__")
