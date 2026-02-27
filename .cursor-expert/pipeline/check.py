#!/usr/bin/env python3
"""Pipeline stage-gate invariant checker.

Validates plan, implement (scope), test, and review stages.
Includes tier routing invariant checks.
Usage:
  python .cursor/pipeline/check.py --issue <issue-id> --stage plan
  python .cursor/pipeline/check.py --issue <issue-id> --stage implement
  python .cursor/pipeline/check.py --issue <issue-id> --stage test
  python .cursor/pipeline/check.py --issue <issue-id> --stage review
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT_LIB = str(Path(__file__).resolve().parents[2] / "lib")
if ROOT_LIB not in sys.path:
    sys.path.insert(0, ROOT_LIB)

from pipeline_check_common import (  # noqa: E402
    InvariantViolation,
    check_implement as base_check_implement,
    check_plan,
    check_review as base_check_review,
    check_test as base_check_test,
    load_json,
    run_checker,
)

TIER_ORDER = {"fast": 0, "standard": 1, "high": 2}


def check_implement(issue_dir: Path) -> list[InvariantViolation]:
    violations = base_check_implement(issue_dir)
    plan = load_json(issue_dir / "plan.json")

    # Tier routing: if task classified as complex, no fast-tier agent should be used
    complexity = plan.get("complexity")
    worker_result = load_json(issue_dir / "worker-result.json")
    tier_used = worker_result.get("tier_used") if worker_result else None
    if complexity == "complex" and tier_used == "fast":
        violations.append(
            InvariantViolation(
                "tier_complex_no_fast",
                "Task classified as complex but worker used fast tier; use jg-worker-high",
            )
        )

    # Escalation history tier progression
    escalation_history = worker_result.get("escalation_history", [])
    violations.extend(check_escalation_history_tier_progression(escalation_history, "worker-result.json"))

    return violations


def check_escalation_history_tier_progression(escalation_history: list[dict[str, Any]], artifact_name: str) -> list[InvariantViolation]:
    """Ensure escalation_history entries show increasing tier level (fast < standard < high)."""
    violations: list[InvariantViolation] = []
    for i, entry in enumerate(escalation_history):
        from_tier = entry.get("from_tier")
        to_tier = entry.get("to_tier")
        if from_tier not in TIER_ORDER or to_tier not in TIER_ORDER:
            continue  # schema validates presence; tier validity handled elsewhere
        if TIER_ORDER[from_tier] >= TIER_ORDER[to_tier]:
            violations.append(
                InvariantViolation(
                    "escalation_tier_progression",
                    f"{artifact_name} escalation_history[{i}]: from_tier {from_tier} must be < to_tier {to_tier}",
                )
            )
    return violations


def check_test(issue_dir: Path) -> list[InvariantViolation]:
    violations = base_check_test(issue_dir)
    plan = load_json(issue_dir / "plan.json")
    test_result = load_json(issue_dir / "test-result.json")
    if not test_result:
        return violations

    # Tier routing: if task classified as complex, no fast-tier agent should be used
    complexity = plan.get("complexity") if plan else None
    tier_used = test_result.get("tier_used")
    if complexity == "complex" and tier_used == "fast":
        violations.append(
            InvariantViolation(
                "tier_complex_no_fast",
                "Task classified as complex but tester used fast tier; use jg-tester (standard) or higher",
            )
        )

    # Escalation history tier progression
    escalation_history = test_result.get("escalation_history", [])
    violations.extend(check_escalation_history_tier_progression(escalation_history, "test-result.json"))

    return violations


def check_review(issue_dir: Path) -> list[InvariantViolation]:
    violations = base_check_review(issue_dir)
    plan = load_json(issue_dir / "plan.json")
    review = load_json(issue_dir / "review-result.json")
    if not review:
        return violations

    # Tier routing: if task classified as complex, no fast-tier agent should be used
    complexity = plan.get("complexity") if plan else None
    tier_used = review.get("tier_used")
    if complexity == "complex" and tier_used == "fast":
        violations.append(
            InvariantViolation(
                "tier_complex_no_fast",
                "Task classified as complex but reviewer used fast tier; use jg-reviewer-high",
            )
        )

    return violations


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
