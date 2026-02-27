#!/usr/bin/env python3
"""Pipeline stage-gate invariant checker.

Validates plan, implement (scope), test, and review stages.
Usage:
  python .cursor/pipeline/check.py --issue <issue-id> --stage plan
  python .cursor/pipeline/check.py --issue <issue-id> --stage implement
  python .cursor/pipeline/check.py --issue <issue-id> --stage test
  python .cursor/pipeline/check.py --issue <issue-id> --stage review
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT_LIB = str(Path(__file__).resolve().parents[2] / "lib")
if ROOT_LIB not in sys.path:
    sys.path.insert(0, ROOT_LIB)

from pipeline_check_common import (  # noqa: E402
    check_implement,
    check_plan,
    check_review,
    check_test,
    run_checker,
)


STAGE_CHECKERS = {
    "plan": check_plan,
    "implement": check_implement,
    "test": check_test,
    "review": check_review,
}


def main() -> None:
    sys.exit(run_checker(STAGE_CHECKERS, "JG pipeline stage-gate invariant checker"))


if __name__ == "__main__":
    main()
