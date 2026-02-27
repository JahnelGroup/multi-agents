"""Shared stage-gate invariant checks for pipeline artifacts."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


class InvariantViolation:
    def __init__(self, check: str, message: str, severity: str = "error") -> None:
        self.check = check
        self.message = message
        self.severity = severity

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.check}: {self.message}"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())  # type: ignore[no-any-return]
    except json.JSONDecodeError:
        return {}


def check_plan(issue_dir: Path) -> list[InvariantViolation]:
    violations: list[InvariantViolation] = []
    plan = load_json(issue_dir / "plan.json")

    if not plan:
        violations.append(InvariantViolation("plan_exists", "plan.json not found or empty"))
        return violations

    affected = set(plan.get("affected_files", []))
    steps = plan.get("steps", [])
    ac_mapping = plan.get("acceptance_mapping", {})

    if not affected:
        violations.append(InvariantViolation("affected_files", "No affected_files listed"))
    if not steps:
        violations.append(InvariantViolation("steps", "No steps listed"))
    if not ac_mapping:
        violations.append(InvariantViolation("ac_mapping", "No acceptance_mapping entries"))

    for ac_text, test_path in ac_mapping.items():
        if not test_path:
            violations.append(
                InvariantViolation("ac_test_mapped", f"AC has no test mapping: {ac_text[:80]!r}")
            )

    for changed_file in affected:
        if not any(step.get("file") == changed_file for step in steps):
            violations.append(
                InvariantViolation("file_has_step", f"File in affected_files has no step: {changed_file}")
            )

    for step in steps:
        step_file = step.get("file", "")
        if step_file and step_file not in affected:
            violations.append(
                InvariantViolation("step_in_affected", f"Step file not in affected_files: {step_file}")
            )

    return violations


def check_implement(issue_dir: Path) -> list[InvariantViolation]:
    violations: list[InvariantViolation] = []
    plan = load_json(issue_dir / "plan.json")
    if not plan:
        violations.append(InvariantViolation("plan_exists", "plan.json not found"))
        return violations

    affected = set(plan.get("affected_files", []))
    result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True, check=False)
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, check=False
    )
    changed = set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
    new_files = set(untracked.stdout.strip().split("\n")) if untracked.stdout.strip() else set()
    all_changed = (changed | new_files) - {""}

    extra = all_changed - affected
    for changed_file in sorted(extra):
        if changed_file.startswith(".pipeline/"):
            continue
        violations.append(
            InvariantViolation("scope_extra", f"File changed but not in plan affected_files: {changed_file}")
        )

    missing = affected - all_changed
    for changed_file in sorted(missing):
        violations.append(
            InvariantViolation(
                "scope_missing",
                f"File in plan affected_files but not changed: {changed_file}",
                severity="warning",
            )
        )

    return violations


def check_test(issue_dir: Path) -> list[InvariantViolation]:
    violations: list[InvariantViolation] = []
    test_result = load_json(issue_dir / "test-result.json")
    if not test_result:
        violations.append(InvariantViolation("test_result_exists", "test-result.json not found or empty"))
        return violations

    phase_1 = test_result.get("phase_1", {})
    phase_1_failed = any(v.get("result") == "FAIL" for v in phase_1.values())
    has_phase_2 = test_result.get("phase_2") is not None
    if phase_1_failed and has_phase_2:
        violations.append(InvariantViolation("phase_2_gated", "Phase 2 ran despite Phase 1 failure"))

    classification = test_result.get("classification")
    if classification is not None and classification not in ("fix_target", "plan_defect"):
        violations.append(
            InvariantViolation("classification_valid", f"Invalid classification (tester should leave null): {classification}")
        )

    return violations


def check_review(issue_dir: Path) -> list[InvariantViolation]:
    violations: list[InvariantViolation] = []
    review = load_json(issue_dir / "review-result.json")
    if not review:
        violations.append(InvariantViolation("review_result_exists", "review-result.json not found or empty"))
        return violations

    verdict = review.get("verdict")
    blockers = review.get("blockers", [])
    if verdict == "PASS" and blockers:
        violations.append(InvariantViolation("verdict_consistent", f"Verdict PASS but {len(blockers)} blocker(s)"))

    for finding_type, findings in [("blocker", blockers), ("concern", review.get("concerns", []))]:
        for idx, finding in enumerate(findings):
            if not isinstance(finding, dict):
                continue
            if not finding.get("file"):
                violations.append(InvariantViolation("finding_has_file", f"{finding_type}[{idx}] missing 'file'"))
            if not finding.get("line"):
                violations.append(InvariantViolation("finding_has_line", f"{finding_type}[{idx}] missing 'line'"))

    return violations


def run_checker(stage_checkers: dict[str, Callable[[Path], list[InvariantViolation]]], description: str) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--issue", required=True, help="Issue ID (e.g. SPEC-X-002)")
    parser.add_argument("--stage", required=True, choices=list(stage_checkers.keys()), help="Stage to validate")
    parser.add_argument("--pipeline-dir", default=None, help="Override .pipeline directory (default: .pipeline)")
    args = parser.parse_args()

    pipeline_dir = Path(args.pipeline_dir) if args.pipeline_dir else (Path.cwd() / ".pipeline")
    issue_dir = pipeline_dir / args.issue
    if not issue_dir.exists():
        print(f"ERROR: Pipeline directory not found: {issue_dir}")
        return 2

    checker = stage_checkers[args.stage]
    violations = checker(issue_dir)

    errors = [v for v in violations if v.severity == "error"]
    warnings = [v for v in violations if v.severity == "warning"]

    for violation in violations:
        print(violation)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) - FAIL")
        return 1
    if warnings:
        print(f"\n{len(warnings)} warning(s) - PASS with warnings")
    else:
        print(f"\nAll invariants passed for stage '{args.stage}' - PASS")
    return 0

