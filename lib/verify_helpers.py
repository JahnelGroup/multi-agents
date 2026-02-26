"""Shared assertion helpers for tutorial exercise verifiers.

Tier-specific verify.py files import from this module to reduce duplication.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

CheckResult = tuple[str, bool, str]
ExerciseChecker = Callable[[], list[CheckResult]]


def check(name: str, passed: bool, msg: str) -> CheckResult:
    return (name, passed, msg)


def run_cmd(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def load_and_validate_json(
    path: Path,
    prefix: str,
) -> tuple[dict[str, Any] | None, list[CheckResult]]:
    """Load a JSON file, returning (parsed_data, check_results).

    Emits ``{prefix}_exists`` and ``{prefix}_valid_json`` checks.
    Returns ``(None, results)`` when the file is missing or unparseable.
    """
    results: list[CheckResult] = []
    results.append(check(f"{prefix}_exists", path.exists(), str(path)))
    if not path.exists():
        return None, results
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        results.append(check(f"{prefix}_valid_json", False, str(exc)))
        return None, results
    results.append(check(f"{prefix}_valid_json", True, "Valid JSON"))
    return data, results


def check_json_has_keys(
    data: dict[str, Any],
    keys: list[str],
    prefix: str,
) -> list[CheckResult]:
    """Check that *data* contains every key in *keys*."""
    return [check(f"{prefix}_{key}", key in data, f"{key} field") for key in keys]


def check_provenance(
    artifact_path: Path,
    expected_agent: str,
    label: str | None = None,
) -> CheckResult:
    """Assert that an artifact's ``produced_by`` equals *expected_agent*."""
    lab = label or f"{artifact_path.stem}_provenance"
    if not artifact_path.exists():
        return check(lab, False, f"Artifact not found: {artifact_path}")
    try:
        data = json.loads(artifact_path.read_text())
    except json.JSONDecodeError:
        return check(lab, False, "Invalid JSON")
    actual = data.get("produced_by")
    if actual is None:
        return check(lab, False, f"Missing produced_by (expected {expected_agent!r})")
    passed = actual == expected_agent
    msg = f"produced_by: {actual!r}" + ("" if passed else f" (expected {expected_agent!r})")
    return check(lab, passed, msg)


def check_sections(
    content: str,
    sections: list[str],
    prefix: str,
) -> list[CheckResult]:
    """Check that *content* contains markdown ``## <section>`` headings."""
    results: list[CheckResult] = []
    for section in sections:
        has_section = bool(
            re.search(rf"^##\s+{re.escape(section)}", content, re.IGNORECASE | re.MULTILINE)
        )
        safe = section.lower().replace(" ", "_").replace("-", "_").replace(".", "")
        results.append(check(f"{prefix}_{safe}", has_section, f"Section: {section}"))
    return results


def check_word_count(text: str, min_words: int, check_name: str) -> CheckResult:
    """Assert that *text* has at least *min_words* words."""
    word_count = len(text.split())
    return check(check_name, word_count >= min_words, f"{word_count} words (need >={min_words})")


def validate_schema_with(
    schema_py: Path,
    artifact_path: Path,
) -> tuple[bool, str]:
    """Run ``schema.py --validate`` on an artifact and return (ok, output)."""
    if not schema_py.exists():
        return False, f"schema.py not found at {schema_py}"
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    proc = subprocess.run(
        [sys.executable, str(schema_py), "--validate", str(artifact_path)],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def verifier_main(
    checkers: dict[int, ExerciseChecker],
    description: str,
    show_exercise_headers: bool = True,
) -> None:
    """Shared CLI entry-point for exercise verifiers."""
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--exercise",
        type=int,
        choices=sorted(checkers.keys()),
        help="Exercise number",
    )
    group.add_argument("--all", action="store_true", help="Run all exercises")
    args = parser.parse_args()

    exercises = sorted(checkers.keys()) if args.all else [args.exercise]
    all_results: list[CheckResult] = []

    for ex in exercises:
        if show_exercise_headers:
            print(f"\n=== Exercise {ex:02d} ===")
        results = checkers[ex]()
        all_results.extend(results)
        for name, passed, msg in results:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {name}: {msg}")

    total_passed = sum(1 for _, p, _ in all_results if p)
    total = len(all_results)
    print(f"\n{total_passed}/{total} checks passed", end="")
    if total_passed == total:
        print(" -- ALL PASS")
        sys.exit(0)
    else:
        print(" -- FAIL")
        sys.exit(1)
