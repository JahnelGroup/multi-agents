"""
JG pipeline artifact schema validator.
Usage: python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/plan.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {
    "plan.json": ["affected_files", "steps", "acceptance_mapping"],
    "worker-result.json": ["status", "files_changed", "blockers", "summary"],
    "test-result.json": ["verdict", "phase_1"],
    "review-result.json": ["verdict", "blockers", "concerns", "nits"],
    "debug-diagnosis.json": [
        "failure_source",
        "failure_description",
        "root_cause",
        "root_cause_file",
        "root_cause_line",
        "classification",
    ],
    "git-result.json": ["branch", "commit_sha", "commit_message"],
}

VALID_TIERS = frozenset({"fast", "standard", "high"})

ARTIFACTS_WITH_ESCALATION_HISTORY = frozenset({"worker-result.json", "test-result.json"})


def validate_tier_used(value: object) -> list[str]:
    errors: list[str] = []
    if value is None:
        return errors
    if not isinstance(value, str):
        errors.append(f"tier_used must be a string, got {type(value).__name__}")
    elif value not in VALID_TIERS:
        errors.append(f"tier_used must be one of {sorted(VALID_TIERS)}, got {value!r}")
    return errors


def validate_escalation_history(value: object) -> list[str]:
    errors: list[str] = []
    if value is None:
        return errors
    if not isinstance(value, list):
        errors.append(f"escalation_history must be an array, got {type(value).__name__}")
        return errors
    for i, entry in enumerate(value):
        if not isinstance(entry, dict):
            errors.append(f"escalation_history[{i}] must be an object, got {type(entry).__name__}")
            continue
        for key in ("from_tier", "to_tier", "reason"):
            if key not in entry:
                errors.append(f"escalation_history[{i}] missing required key: {key}")
    return errors


def validate_artifact(path: Path) -> list[str]:
    errors: list[str] = []
    name = path.name
    if name not in REQUIRED:
        return [f"Unknown artifact: {name}"]
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        return [f"Invalid JSON: {e}"]
    for key in REQUIRED[name]:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    if "tier_used" in data:
        errors.extend(validate_tier_used(data["tier_used"]))
    if name in ARTIFACTS_WITH_ESCALATION_HISTORY and "escalation_history" in data:
        errors.extend(validate_escalation_history(data["escalation_history"]))
    return errors


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "--validate":
        print("Usage: python schema.py --validate <path-to-artifact.json>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[2])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    errors = validate_artifact(path)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
