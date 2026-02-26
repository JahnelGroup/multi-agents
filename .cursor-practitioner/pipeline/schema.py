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
