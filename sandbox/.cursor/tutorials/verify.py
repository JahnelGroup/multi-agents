#!/usr/bin/env python3
"""Practitioner tutorial exercise verifier."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TUTORIALS_DIR = Path(__file__).resolve().parent
PRACTITIONER_DIR = TUTORIALS_DIR.parent
REPO_ROOT = PRACTITIONER_DIR.parent
SANDBOX_DIR = REPO_ROOT / "sandbox"
PIPELINE_DIR = SANDBOX_DIR / ".pipeline" / "ISSUE-42"
SCHEMA_PY = SANDBOX_DIR / ".cursor" / "pipeline" / "schema.py"
CHECK_PY = SANDBOX_DIR / ".cursor" / "pipeline" / "check.py"


def check(name: str, passed: bool, msg: str) -> tuple[str, bool, str]:
    return (name, passed, msg)


def run_cmd(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def validate_schema(artifact_path: Path) -> tuple[bool, str]:
    if not SCHEMA_PY.exists():
        return False, f"schema.py not found at {SCHEMA_PY}"
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    code, output = run_cmd([sys.executable, str(SCHEMA_PY), "--validate", str(artifact_path)])
    return code == 0, output


def check_ex01() -> list[tuple[str, bool, str]]:
    results = []
    cursor_dir = SANDBOX_DIR / ".cursor"
    results.append(check("01_cursor_dir", cursor_dir.is_dir(), str(cursor_dir)))
    agents_dir = cursor_dir / "agents"
    results.append(check("01_agents_dir", agents_dir.is_dir(), str(agents_dir)))
    if agents_dir.is_dir():
        agent_files = list(agents_dir.glob("*.md"))
        results.append(check("01_agent_count", len(agent_files) >= 4, f"{len(agent_files)} agent files"))
    for name in ["jg-planner.md", "jg-worker.md"]:
        path = agents_dir / name
        results.append(check(f"01_{name}", path.exists(), str(path)))
    rules_dir = cursor_dir / "rules"
    results.append(check("01_rules_dir", rules_dir.is_dir(), str(rules_dir)))
    if rules_dir.is_dir():
        rule_files = list(rules_dir.glob("*.mdc"))
        results.append(check("01_rule_count", len(rule_files) >= 1, f"{len(rule_files)} rule files"))
    pipeline_dir = cursor_dir / "pipeline"
    results.append(check("01_schema_py", (pipeline_dir / "schema.py").exists(), "schema.py"))
    results.append(check("01_check_py", (pipeline_dir / "check.py").exists(), "check.py"))
    results.append(check("01_node_modules", (SANDBOX_DIR / "node_modules").is_dir(), "node_modules"))
    code, output = run_cmd(["npm", "test"], cwd=str(SANDBOX_DIR))
    results.append(check("01_npm_test", code == 0, output[:200]))
    return results


def check_ex02() -> list[tuple[str, bool, str]]:
    results = []
    plan = PIPELINE_DIR / "plan.json"
    results.append(check("02_plan_exists", plan.exists(), str(plan)))
    if plan.exists():
        passed, msg = validate_schema(plan)
        results.append(check("02_plan_schema", passed, msg))
        try:
            data = json.loads(plan.read_text())
            results.append(check("02_has_affected_files", "affected_files" in data, "affected_files field"))
            results.append(check("02_has_steps", "steps" in data, "steps field"))
            results.append(check("02_has_acceptance", "acceptance_mapping" in data, "acceptance_mapping field"))
        except json.JSONDecodeError as e:
            results.append(check("02_valid_json", False, str(e)))
    return results


def check_ex03() -> list[tuple[str, bool, str]]:
    results = []
    wr = PIPELINE_DIR / "worker-result.json"
    results.append(check("03_worker_result_exists", wr.exists(), str(wr)))
    if wr.exists():
        passed, msg = validate_schema(wr)
        results.append(check("03_worker_result_schema", passed, msg))
        try:
            data = json.loads(wr.read_text())
            results.append(check("03_status_completed", data.get("status") == "completed", f"status: {data.get('status')}"))
            results.append(check("03_has_files_changed", "files_changed" in data, "files_changed field"))
        except json.JSONDecodeError as e:
            results.append(check("03_valid_json", False, str(e)))
    for f in ["src/auth/login.ts", "src/auth/middleware.ts", "src/auth/login.test.ts", "src/auth/middleware.test.ts"]:
        path = SANDBOX_DIR / f
        results.append(check(f"03_{Path(f).stem}", path.exists(), str(path)))
    code, output = run_cmd(["npm", "test"], cwd=str(SANDBOX_DIR))
    results.append(check("03_npm_test", code == 0, output[:200]))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results = []
    for name in ["test-result-fail.json", "debug-diagnosis.json", "test-result-pass.json"]:
        path = PIPELINE_DIR / name
        results.append(check(f"04_{name}_exists", path.exists(), str(path)))
        if path.exists():
            schema_name = path
            if "test-result-" in name:
                tmp = PIPELINE_DIR / "test-result.json"
                shutil.copy2(path, tmp)
                schema_name = tmp
            passed, msg = validate_schema(schema_name)
            results.append(check(f"04_{name}_schema", passed, msg))
            if "test-result-" in name and (PIPELINE_DIR / "test-result.json").exists():
                (PIPELINE_DIR / "test-result.json").unlink()
    diag = PIPELINE_DIR / "debug-diagnosis.json"
    if diag.exists():
        try:
            data = json.loads(diag.read_text())
            results.append(check("04_has_root_cause", "root_cause" in data, "root_cause field"))
            results.append(check("04_has_classification", "classification" in data, "classification field"))
        except json.JSONDecodeError as e:
            results.append(check("04_diag_json", False, str(e)))
    code, output = run_cmd(["npm", "test"], cwd=str(SANDBOX_DIR))
    results.append(check("04_npm_test_passes", code == 0, output[:200]))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results = []
    for name in ["review-result.json", "git-result.json"]:
        path = PIPELINE_DIR / name
        results.append(check(f"05_{name}_exists", path.exists(), str(path)))
        if path.exists():
            passed, msg = validate_schema(path)
            results.append(check(f"05_{name}_schema", passed, msg))
    gr = PIPELINE_DIR / "git-result.json"
    if gr.exists():
        try:
            data = json.loads(gr.read_text())
            results.append(check("05_has_branch", "branch" in data, "branch field"))
            results.append(check("05_has_commit", "commit_sha" in data, "commit_sha field"))
        except json.JSONDecodeError as e:
            results.append(check("05_git_json", False, str(e)))
    return results


def check_ex06() -> list[tuple[str, bool, str]]:
    results = []
    linter = SANDBOX_DIR / ".cursor" / "agents" / "team-linter.md"
    results.append(check("06_team_linter_exists", linter.exists(), str(linter)))
    if linter.exists():
        content = linter.read_text()
        has_frontmatter = content.startswith("---") and content.count("---") >= 2
        results.append(check("06_has_frontmatter", has_frontmatter, "Valid frontmatter"))
        has_name = "name:" in content.lower() and "team-linter" in content.lower()
        results.append(check("06_has_name", has_name, "name: team-linter"))
        has_model = "model:" in content.lower()
        results.append(check("06_has_model", has_model, "model field"))
    agents_md = SANDBOX_DIR / ".cursor" / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text().lower()
        results.append(check("06_agents_md_linter", "team-linter" in content, "AGENTS.md references team-linter"))
        results.append(check("06_agents_md_lint_result", "lint-result" in content, "AGENTS.md references lint-result"))
    else:
        results.append(check("06_agents_md_exists", False, str(agents_md)))
    return results


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05, 6: check_ex06}


def main() -> None:
    parser = argparse.ArgumentParser(description="Practitioner tutorial verifier")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--exercise", type=int, choices=range(1, 7), help="Exercise number (1-6)")
    group.add_argument("--all", action="store_true", help="Run all exercises")
    args = parser.parse_args()

    exercises = list(CHECKERS.keys()) if args.all else [args.exercise]
    all_results: list[tuple[str, bool, str]] = []

    for ex in exercises:
        print(f"\n=== Exercise {ex:02d} ===")
        results = CHECKERS[ex]()
        all_results.extend(results)
        for name, passed, msg in results:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {name}: {msg}")

    passed = sum(1 for _, p, _ in all_results if p)
    total = len(all_results)
    print(f"\n{passed}/{total} checks passed", end="")
    if passed == total:
        print(" -- ALL PASS")
        sys.exit(0)
    else:
        print(" -- FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
