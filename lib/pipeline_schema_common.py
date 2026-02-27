"""Shared schema validation utilities for pipeline artifacts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_KEYS = {
    "plan.json": ["affected_files", "steps", "acceptance_mapping"],
    "worker-result.json": ["status", "files_changed", "blockers", "summary"],
    "worker-result-fast.json": ["status", "files_changed", "blockers", "summary"],
    "test-result.json": ["verdict", "phase_1"],
    "test-result-fail.json": ["verdict", "phase_1"],
    "test-result-pass.json": ["verdict", "phase_1"],
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


def load_artifact(path: Path) -> tuple[str, dict[str, Any] | None, list[str]]:
    name = path.name
    if name not in REQUIRED_KEYS:
        return name, None, [f"Unknown artifact: {name}"]
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        return name, None, [f"Invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return name, None, [f"Artifact root must be an object, got {type(data).__name__}"]
    return name, data, []


def validate_required_keys(name: str, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_KEYS[name]:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    return errors

