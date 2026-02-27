#!/usr/bin/env python3
"""Practitioner tutorial exercise verifier."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

TUTORIALS_DIR = Path(__file__).resolve().parent
PRACTITIONER_DIR = TUTORIALS_DIR.parent
REPO_ROOT = PRACTITIONER_DIR.parent
SANDBOX_DIR = REPO_ROOT / "sandbox"
PIPELINE_DIR = SANDBOX_DIR / ".pipeline" / "ISSUE-42"
SCHEMA_PY = SANDBOX_DIR / ".cursor" / "pipeline" / "schema.py"
CHECK_PY = SANDBOX_DIR / ".cursor" / "pipeline" / "check.py"

_HELPERS_DIR = str(REPO_ROOT / "lib")
if _HELPERS_DIR not in sys.path:
    sys.path.insert(0, _HELPERS_DIR)

from verify_helpers import (  # noqa: E402
    check,
    check_json_has_keys,
    check_provenance,
    check_sections,
    check_word_count,
    load_and_validate_json,
    run_cmd,
    validate_schema_with,
    verifier_main,
)


def check_ex01() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
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
    results: list[tuple[str, bool, str]] = []
    plan_path = PIPELINE_DIR / "plan.json"
    data, json_results = load_and_validate_json(plan_path, "02_plan")
    results.append(check("02_plan_exists", plan_path.exists(), str(plan_path)))
    if data is not None:
        passed, msg = validate_schema_with(SCHEMA_PY, plan_path)
        results.append(check("02_plan_schema", passed, msg))
        results.extend(check_json_has_keys(data, ["affected_files", "steps", "acceptance_mapping"], "02"))
        affected = data.get("affected_files", [])
        if affected:
            plausible = all(
                f.startswith("src/") or f.startswith("test/") or f.startswith("tests/")
                or f.startswith("sandbox/") or f.endswith(".ts") or f.endswith(".js")
                for f in affected
            )
            results.append(check("02_affected_files_plausible", plausible,
                f"{len(affected)} paths; all plausible" if plausible else "Implausible path in affected_files"))
        results.append(check_provenance(plan_path, "jg-subplanner"))
    if CHECK_PY.exists() and PIPELINE_DIR.is_dir():
        code, output = run_cmd(
            [sys.executable, str(CHECK_PY), "--issue", "ISSUE-42", "--stage", "plan"],
            cwd=str(SANDBOX_DIR),
        )
        results.append(check("02_check_py_plan", code == 0, output[:200]))
    return results


def check_ex03() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    wr = PIPELINE_DIR / "worker-result.json"
    results.append(check("03_worker_result_exists", wr.exists(), str(wr)))
    if wr.exists():
        passed, msg = validate_schema_with(SCHEMA_PY, wr)
        results.append(check("03_worker_result_schema", passed, msg))
        try:
            data = json.loads(wr.read_text())
            results.append(check("03_status_completed", data.get("status") == "completed", f"status: {data.get('status')}"))
            results.append(check("03_has_files_changed", "files_changed" in data, "files_changed field"))
            files_changed = data.get("files_changed", [])
            if files_changed:
                missing = [f for f in files_changed if not (SANDBOX_DIR / f).exists()]
                results.append(check(
                    "03_files_changed_exist",
                    len(missing) == 0,
                    f"All {len(files_changed)} files exist on disk" if not missing else f"Missing on disk: {missing[:5]}",
                ))
        except json.JSONDecodeError as e:
            results.append(check("03_valid_json", False, str(e)))
        results.append(check_provenance(wr, "jg-worker"))
    for f in ["src/auth/login.ts", "src/auth/middleware.ts", "src/auth/login.test.ts", "src/auth/middleware.test.ts"]:
        path = SANDBOX_DIR / f
        results.append(check(f"03_{Path(f).stem}", path.exists(), str(path)))
    code, output = run_cmd(["npm", "test"], cwd=str(SANDBOX_DIR))
    results.append(check("03_npm_test", code == 0, output[:200]))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    provenance_map = {
        "test-result-fail.json": "jg-tester",
        "debug-diagnosis.json": "jg-debugger",
        "test-result-pass.json": "jg-tester",
    }
    for name in ["test-result-fail.json", "debug-diagnosis.json", "test-result-pass.json"]:
        path = PIPELINE_DIR / name
        results.append(check(f"04_{name}_exists", path.exists(), str(path)))
        if path.exists():
            schema_name = path
            if "test-result-" in name:
                tmp = PIPELINE_DIR / "test-result.json"
                shutil.copy2(path, tmp)
                schema_name = tmp
            passed, msg = validate_schema_with(SCHEMA_PY, schema_name)
            results.append(check(f"04_{name}_schema", passed, msg))
            if "test-result-" in name and (PIPELINE_DIR / "test-result.json").exists():
                (PIPELINE_DIR / "test-result.json").unlink()
            results.append(check_provenance(path, provenance_map[name]))
    diag = PIPELINE_DIR / "debug-diagnosis.json"
    if diag.exists():
        try:
            data = json.loads(diag.read_text())
            results.extend(check_json_has_keys(data, ["root_cause", "classification"], "04"))
        except json.JSONDecodeError as e:
            results.append(check("04_diag_json", False, str(e)))
    code, output = run_cmd(["npm", "test"], cwd=str(SANDBOX_DIR))
    results.append(check("04_npm_test_passes", code == 0, output[:200]))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    provenance_map = {
        "review-result.json": "jg-reviewer",
        "git-result.json": "jg-git",
    }
    for name in ["review-result.json", "git-result.json"]:
        path = PIPELINE_DIR / name
        results.append(check(f"05_{name}_exists", path.exists(), str(path)))
        if path.exists():
            passed, msg = validate_schema_with(SCHEMA_PY, path)
            results.append(check(f"05_{name}_schema", passed, msg))
            results.append(check_provenance(path, provenance_map[name]))
    rr = PIPELINE_DIR / "review-result.json"
    if rr.exists():
        try:
            rdata = json.loads(rr.read_text())
            all_findings = rdata.get("blockers", []) + rdata.get("concerns", []) + rdata.get("nits", [])
            findings_with_file = [f for f in all_findings if isinstance(f, dict) and f.get("file")]
            if findings_with_file:
                bad = [f["file"] for f in findings_with_file if not (SANDBOX_DIR / f["file"]).exists()]
                results.append(check(
                    "05_review_findings_files_exist",
                    len(bad) == 0,
                    f"All {len(findings_with_file)} finding files exist" if not bad else f"Findings reference missing files: {bad[:3]}",
                ))
        except (json.JSONDecodeError, KeyError):
            pass
    gr = PIPELINE_DIR / "git-result.json"
    if gr.exists():
        try:
            data = json.loads(gr.read_text())
            results.extend(check_json_has_keys(data, ["branch", "commit_sha"], "05"))
            branch_name = data.get("branch", "")
            if branch_name:
                code, output = run_cmd(["git", "branch", "--list", branch_name], cwd=str(SANDBOX_DIR))
                branch_exists = branch_name in output
                results.append(check("05_git_branch_exists", branch_exists,
                    f"Branch '{branch_name}' exists" if branch_exists else f"Branch '{branch_name}' not found in git"))
        except json.JSONDecodeError as e:
            results.append(check("05_git_json", False, str(e)))
    if CHECK_PY.exists():
        code, output = run_cmd(
            [sys.executable, str(CHECK_PY), "--issue", "ISSUE-42", "--stage", "review"],
            cwd=str(SANDBOX_DIR),
        )
        results.append(check("05_check_py_review", code == 0, output[:200]))

    hitl_path = TUTORIALS_DIR / "outputs" / "05-hitl-analysis.md"
    results.append(check("05_hitl_exists", hitl_path.exists(), str(hitl_path)))
    if hitl_path.exists():
        hitl_content = hitl_path.read_text()
        results.extend(check_sections(hitl_content, ["When to block", "Approval flow", "Risk without HITL"], "05_hitl"))
        results.append(check_word_count(hitl_content, 80, "05_hitl_depth"))

    return results


def check_ex06() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
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
        has_description = bool(re.search(r"description:\s*\S", content))
        results.append(check("06_has_description", has_description, "description field with value"))
        fm_end = content.find("---", 3)
        body = content[fm_end + 3:].strip() if fm_end > 0 else ""
        body_lower = body.lower()
        results.append(check("06_body_lint_result", "lint-result" in body_lower, "Body mentions lint-result artifact"))
        has_verdict = "verdict" in body_lower or ("pass" in body_lower and "fail" in body_lower)
        results.append(check("06_body_verdict", has_verdict, "Body mentions verdict or PASS/FAIL schema"))
        results.append(check_word_count(body, 30, "06_body_length"))
    agents_md = SANDBOX_DIR / ".cursor" / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text().lower()
        results.append(check("06_agents_md_linter", "team-linter" in content, "AGENTS.md references team-linter"))
        results.append(check("06_agents_md_lint_result", "lint-result" in content, "AGENTS.md references lint-result"))
    else:
        results.append(check("06_agents_md_exists", False, str(agents_md)))
    return results


def check_ex07() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    rule_path = SANDBOX_DIR / ".cursor" / "rules" / "jg-test-before-commit.mdc"
    results.append(check("07_rule_exists", rule_path.exists(), str(rule_path)))
    if not rule_path.exists():
        return results
    content = rule_path.read_text()
    has_frontmatter = content.startswith("---") and content.count("---") >= 2
    results.append(check("07_has_frontmatter", has_frontmatter, "Valid frontmatter"))
    has_description = bool(re.search(r"description:\s*\S", content))
    results.append(check("07_has_description", has_description, "description field with value"))
    has_always_apply = "alwaysapply:" in content.lower()
    results.append(check("07_has_always_apply", has_always_apply, "alwaysApply field"))
    has_when = bool(re.search(r"##\s*When to Apply", content, re.IGNORECASE))
    results.append(check("07_has_when_section", has_when, "## When to Apply section"))
    fm_end = content.find("---", 3)
    body = content[fm_end + 3:].strip() if fm_end > 0 else ""
    body_lower = body.lower()
    results.append(check_word_count(body, 30, "07_body_length"))
    results.append(check("07_refs_test_result", "test-result.json" in body_lower, "Body references test-result.json"))
    results.append(check("07_refs_verdict", "verdict" in body_lower, "Body references verdict field"))
    results.append(check("07_refs_pass", "pass" in body_lower, "Body references PASS value"))
    has_rule_section = bool(re.search(r"##\s*Rule\b", body))
    results.append(check("07_has_rule_section", has_rule_section, "## Rule section"))
    has_exempt_section = bool(re.search(r"##\s*Exempt", body, re.IGNORECASE))
    results.append(check("07_has_exempt_section", has_exempt_section, "## Exempt section"))
    return results


def check_ex08() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    skill_path = SANDBOX_DIR / ".cursor" / "skills" / "jg-sandbox-test-runner" / "SKILL.md"
    results.append(check("08_skill_exists", skill_path.exists(), str(skill_path)))
    if not skill_path.exists():
        return results
    content = skill_path.read_text()
    has_frontmatter = content.startswith("---") and content.count("---") >= 2
    results.append(check("08_has_frontmatter", has_frontmatter, "Valid frontmatter"))
    has_name = "name:" in content.lower() and "jg-sandbox-test-runner" in content.lower()
    results.append(check("08_has_name", has_name, "name: jg-sandbox-test-runner"))
    has_description = bool(re.search(r"description:\s*\S", content))
    results.append(check("08_has_description", has_description, "description field with value"))
    fm_end = content.find("---", 3)
    body = content[fm_end + 3:].strip() if fm_end > 0 else ""
    body_lower = body.lower()
    results.append(check_word_count(body, 40, "08_body_length"))
    mentions_test = "npm test" in body_lower or "npm run test" in body_lower or "jest" in body_lower
    results.append(check("08_mentions_test", mentions_test, "Mentions test command"))
    results.extend(check_sections(
        body,
        ["When to Use", "Running Tests", "Interpreting Results", "Writing Test Artifacts", "Anti-patterns"],
        "08_section",
    ))
    results.append(check("08_refs_test_result", "test-result.json" in body_lower, "Body references test-result.json"))
    results.append(check("08_refs_verdict", "verdict" in body_lower, "Body references verdict field"))
    return results


def check_ex09() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    outputs_dir = TUTORIALS_DIR / "outputs"
    path = outputs_dir / "09-benchmarker-intro.md"
    results.append(check("09_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    content_lower = content.lower()

    results.extend(check_sections(
        content,
        ["benchmarker role", "verdict definitions", "per-agent focus", "when to review"],
        "09_section",
    ))

    verdict_match = re.search(r"##\s*verdict\s*definitions(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if verdict_match:
        verdict_text = verdict_match.group(1).lower()
        for v in ["excellent", "correct", "monitor", "tune", "upgrade"]:
            results.append(check(f"09_verdict_{v}", v in verdict_text, f"Mentions verdict '{v}'"))

    focus_match = re.search(r"##\s*per-agent\s*focus(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if focus_match:
        focus_text = focus_match.group(1).lower()
        agent_roles = ["planner", "worker", "tester", "reviewer", "debugger"]
        found = sum(1 for r in agent_roles if r in focus_text)
        results.append(check("09_agent_roles", found >= 3, f"{found} agent roles mentioned (need >=3)"))

    review_match = re.search(r"##\s*when\s*to\s*review(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if review_match:
        results.append(check_word_count(review_match.group(1), 30, "09_review_length"))

    return results


def check_ex10() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    outputs_dir = TUTORIALS_DIR / "outputs"
    path = outputs_dir / "10-resume-analysis.md"
    results.append(check("10_file_exists", path.exists(), str(path)))
    if path.exists():
        results.append(check_word_count(path.read_text(), 50, "10_depth"))
    return results


def check_ex11() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    outputs_dir = TUTORIALS_DIR / "outputs"
    path = outputs_dir / "11-observability-analysis.md"
    results.append(check("11_file_exists", path.exists(), str(path)))
    if path.exists():
        results.append(check_word_count(path.read_text(), 50, "11_depth"))
    return results


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05, 6: check_ex06, 7: check_ex07, 8: check_ex08, 9: check_ex09, 10: check_ex10, 11: check_ex11}

if __name__ == "__main__":
    verifier_main(CHECKERS, "Practitioner tutorial verifier")
