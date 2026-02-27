#!/usr/bin/env python3
"""Expert tutorial exercise verifier."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TUTORIALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TUTORIALS_DIR.parents[2]
EXPERT_DIR = REPO_ROOT / ".cursor-expert"
SANDBOX_DIR = REPO_ROOT / "sandbox"
OUTPUTS_DIR = TUTORIALS_DIR / "outputs"
SCHEMA_PY = EXPERT_DIR / "pipeline" / "schema.py"
CHECK_PY = EXPERT_DIR / "pipeline" / "check.py"

_HELPERS_DIR = str(REPO_ROOT / "lib")
if _HELPERS_DIR not in sys.path:
    sys.path.insert(0, _HELPERS_DIR)

from verify_helpers import (  # noqa: E402
    check,
    check_provenance,
    check_sections,
    check_word_count,
    load_and_validate_json,
    run_cmd,
    validate_schema_with,
    verifier_main,
)


EXPECTED_TIERS = {1: "trivial", 3: "complex", 5: "complex"}

TIER_MAP = {
    "NOTIF-001": {"worker": "fast", "tester": "fast", "reviewer": "fast", "has_plan": False, "worker_agent": "jg-worker-fast"},
    "NOTIF-002": {"worker": "standard", "tester": "standard", "reviewer": "standard", "has_plan": True, "worker_agent": "jg-worker"},
    "NOTIF-003": {"worker": "high", "reviewer": "high", "has_plan": True, "worker_agent": "jg-worker-high"},
}


def check_ex01() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    data, json_results = load_and_validate_json(OUTPUTS_DIR / "01-classifications.json", "01")
    results.extend(json_results)
    if data is None:
        return results
    results.append(check("01_count", len(data) == 5, f"{len(data)} classifications (need 5)"))
    required = ["task", "file_count", "domain_scope", "signals", "tier", "agents"]
    for i, item in enumerate(data):
        for field in required:
            results.append(check(f"01_item{i+1}_{field}", field in item, f"Item {i+1} has {field}"))
        if "tier" in item:
            valid_tiers = {"trivial", "standard", "complex"}
            results.append(check(f"01_item{i+1}_tier_valid", item["tier"] in valid_tiers, f"tier={item['tier']}"))
    for idx, expected_tier in EXPECTED_TIERS.items():
        if idx - 1 < len(data) and "tier" in data[idx - 1]:
            results.append(check(
                f"01_item{idx}_tier_correct",
                data[idx - 1]["tier"] == expected_tier,
                f"Expected {expected_tier}, got {data[idx - 1]['tier']}",
            ))
    return results


def check_ex02() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    pipeline = SANDBOX_DIR / ".pipeline"
    for issue, config in TIER_MAP.items():
        issue_dir = pipeline / issue
        results.append(check(f"02_{issue}_dir", issue_dir.is_dir(), str(issue_dir)))
        if not issue_dir.is_dir():
            continue
        if config["has_plan"]:
            plan = issue_dir / "plan.json"
            results.append(check(f"02_{issue}_plan", plan.exists(), str(plan)))
        else:
            plan = issue_dir / "plan.json"
            results.append(check(f"02_{issue}_no_plan", not plan.exists(), "Trivial task should skip plan"))
        for artifact in ["worker-result.json", "test-result.json", "review-result.json", "git-result.json"]:
            path = issue_dir / artifact
            results.append(check(f"02_{issue}_{artifact}", path.exists(), str(path)))
            if path.exists():
                passed, msg = validate_schema_with(SCHEMA_PY, path)
                results.append(check(f"02_{issue}_{artifact}_schema", passed, msg))
                if "tier_used" in config.get("worker", "") or artifact in ["worker-result.json", "review-result.json"]:
                    try:
                        data = json.loads(path.read_text())
                        if "tier_used" in data:
                            agent_type = artifact.replace(".json", "").replace("-result", "").replace("test", "tester")
                            if agent_type == "worker" and "worker" in config:
                                results.append(check(
                                    f"02_{issue}_{artifact}_tier",
                                    data["tier_used"] == config["worker"],
                                    f"tier_used={data['tier_used']}, expected={config['worker']}",
                                ))
                    except (json.JSONDecodeError, KeyError):
                        pass
                if artifact == "worker-result.json" and "worker_agent" in config:
                    results.append(check_provenance(
                        path,
                        config["worker_agent"],
                        label=f"{issue_dir.name}_{Path(artifact).stem}_provenance",
                    ))
                if artifact == "worker-result.json":
                    # Skip files_changed_exist for NOTIF examples: sandbox may not have
                    # the full mocked feature implementation; we validate schema and tier only.
                    pass
    if CHECK_PY.exists():
        for issue, config in TIER_MAP.items():
            issue_dir = pipeline / issue
            if not issue_dir.is_dir():
                continue
            if config["has_plan"]:
                code, output = run_cmd(
                    [sys.executable, str(CHECK_PY), "--issue", issue, "--stage", "plan"],
                    cwd=str(SANDBOX_DIR),
                )
                results.append(check(f"02_{issue}_check_plan", code == 0, output[:200]))
            code, output = run_cmd(
                [sys.executable, str(CHECK_PY), "--issue", issue, "--stage", "review"],
                cwd=str(SANDBOX_DIR),
            )
            results.append(check(f"02_{issue}_check_review", code == 0, output[:200]))
    return results


def check_ex03() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    esc_dir = SANDBOX_DIR / ".pipeline" / "NOTIF-002-escalation"
    results.append(check("03_dir_exists", esc_dir.is_dir(), str(esc_dir)))
    fast_wr = esc_dir / "worker-result-fast.json" if esc_dir.is_dir() else Path("/nonexistent")
    results.append(check("03_fast_tier_artifact", fast_wr.exists(),
        "Fast-tier worker-result-fast.json exists (proves escalation path)" if fast_wr.exists()
        else "Missing worker-result-fast.json -- escalation start not recorded"))
    if fast_wr.exists():
        try:
            fast_data = json.loads(fast_wr.read_text())
            results.append(check("03_fast_status_escalate",
                fast_data.get("status") == "escalate",
                f"Fast-tier status: {fast_data.get('status')!r} (expected 'escalate')"))
        except (json.JSONDecodeError, KeyError):
            pass
    wr = esc_dir / "worker-result.json" if esc_dir.is_dir() else Path("/nonexistent")
    results.append(check("03_worker_result", wr.exists(), str(wr)))
    if wr.exists():
        try:
            data = json.loads(wr.read_text())
            has_esc = "escalation_history" in data and len(data["escalation_history"]) > 0
            results.append(check("03_has_escalation_history", has_esc, "escalation_history present"))
            if has_esc:
                esc = data["escalation_history"][0]
                results.append(check("03_from_tier", esc.get("from_tier") == "fast", f"from_tier={esc.get('from_tier')}"))
                results.append(check("03_to_tier", esc.get("to_tier") == "standard", f"to_tier={esc.get('to_tier')}"))
                results.append(check("03_has_reason", bool(esc.get("reason")), "Has reason"))
            fc = data.get("files_changed", [])
            if fc:
                missing = [f for f in fc if not (SANDBOX_DIR / f).exists()]
                results.append(check(
                    "03_files_changed_exist",
                    len(missing) == 0,
                    f"All {len(fc)} files exist on disk" if not missing else f"Missing: {missing[:5]}",
                ))
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            results.append(check("03_parse", False, str(e)))
        results.append(check_provenance(wr, "jg-worker"))
    if CHECK_PY.exists() and esc_dir.is_dir():
        plan_path = esc_dir / "plan.json"
        if plan_path.exists():
            code, output = run_cmd(
                [sys.executable, str(CHECK_PY), "--issue", "NOTIF-002-escalation", "--stage", "plan"],
                cwd=str(SANDBOX_DIR),
            )
            results.append(check("03_check_plan", code == 0, output[:200]))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    data, json_results = load_and_validate_json(OUTPUTS_DIR / "04-cost-analysis.json", "04")
    results.extend(json_results)
    if data is None:
        return results
    strategies = data.get("strategies", {})
    for name in ["all_standard", "tiered_routing", "standard_with_rework"]:
        results.append(check(f"04_{name}_exists", name in strategies, f"Strategy: {name}"))
        if name in strategies:
            for field in ["total_invocations", "total_tokens", "total_cost", "notes"]:
                results.append(check(f"04_{name}_{field}", field in strategies[name], f"{name}.{field}"))
    if "all_standard" in strategies and "tiered_routing" in strategies:
        costs_differ = strategies["all_standard"].get("total_cost") != strategies["tiered_routing"].get("total_cost")
        results.append(check("04_costs_differ", costs_differ, "Strategies have different costs"))
    rec = data.get("recommendation", "")
    results.append(check_word_count(rec, 20, "04_recommendation_length"))
    results.append(check("04_has_breakeven", "breakeven_analysis" in data, "Has breakeven_analysis"))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    path = OUTPUTS_DIR / "05-architecture.md"
    results.append(check("05_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    sections = [
        "Agent Inventory", "Pipeline Flow", "Tier Routing Rules",
        "Cost Projections", "Monitoring Strategy", "Escalation Policy", "Rollback Plan",
    ]
    results.extend(check_sections(content, sections, "05_section"))
    has_table = bool(re.search(r"\|.*\|.*\|", content))
    results.append(check("05_has_table", has_table, "Has markdown table in Agent Inventory"))
    has_mermaid = bool(re.search(r"```mermaid", content, re.IGNORECASE))
    results.append(check("05_has_mermaid", has_mermaid, "Has mermaid diagram in Pipeline Flow"))
    has_dollars = bool(re.search(r"\$\d", content))
    results.append(check("05_has_costs", has_dollars, "Has dollar amounts in Cost Projections"))
    metrics = ["retry rate", "escalation rate", "cost per issue", "cycle time", "latency", "success rate"]
    found_metrics = sum(1 for m in metrics if m.lower() in content.lower())
    results.append(check("05_metrics_count", found_metrics >= 3, f"{found_metrics} metrics found (need >=3)"))
    return results


def check_ex06() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    path = OUTPUTS_DIR / "06-config-design.md"
    results.append(check("06_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()

    results.extend(check_sections(
        content,
        ["Rules Design", "Skills Design", "Agent Inventory", "AGENTS.md Registry", "Activation Flow"],
        "06_section",
    ))

    rules_match = re.search(r"##\s*rules\s*design(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if rules_match:
        rules_text = rules_match.group(1).lower()
        for term in ["description", "alwaysapply", ".mdc"]:
            results.append(check(f"06_rules_{term.replace('.', '')}", term in rules_text, f"Rules Design mentions '{term}'"))
        rule_names = re.findall(r"jg-[\w-]+\.mdc|[\w-]+-[\w-]+\.mdc", rules_text)
        results.append(check("06_rules_count", len(rule_names) >= 3, f"{len(rule_names)} rule names (need >=3)"))

    skills_match = re.search(r"##\s*skills\s*design(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if skills_match:
        skills_text = skills_match.group(1).lower()
        for term in ["skill.md", "name", "description"]:
            results.append(check(f"06_skills_{term.replace('.', '')}", term in skills_text, f"Skills Design mentions '{term}'"))
        skill_names = re.findall(r"[\w-]+-[\w-]+(?=/skill\.md| skill| --)", skills_text)
        if not skill_names:
            skill_names = re.findall(r"`([\w][\w-]+-[\w-]+[\w])`", skills_text)
        if not skill_names:
            skill_names = re.findall(r"\*\*(\w[\w-]+)\*\*", skills_match.group(1))
        results.append(check("06_skills_count", len(skill_names) >= 2, f"{len(skill_names)} skill names (need >=2)"))

    inv_match = re.search(r"##\s*agent\s*inventory(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if inv_match:
        has_table = bool(re.search(r"\|.*\|.*\|", inv_match.group(1)))
        results.append(check("06_agent_table", has_table, "Agent Inventory has markdown table"))

    has_mermaid = bool(re.search(r"```mermaid", content, re.IGNORECASE))
    results.append(check("06_has_mermaid", has_mermaid, "Has mermaid diagram"))

    results.append(check_word_count(content, 200, "06_word_count"))

    return results


def check_ex07() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    snapshot_path = OUTPUTS_DIR / "07-benchmark-snapshot.json"
    report_path = OUTPUTS_DIR / "07-benchmark-report.md"

    snapshot_data, snap_results = load_and_validate_json(snapshot_path, "07_snapshot")
    results.extend(snap_results)
    if snapshot_data is not None:
        if isinstance(snapshot_data, dict):
            entry_count = len(snapshot_data.get("models", snapshot_data))
        elif isinstance(snapshot_data, list):
            entry_count = len(snapshot_data)
        else:
            entry_count = 0
        results.append(check("07_snapshot_entries", entry_count >= 3, f"{entry_count} model entries (need >=3)"))
        snapshot_producer = snapshot_data.get("produced_by") if isinstance(snapshot_data, dict) else None
        results.append(check(
            "07_snapshot_provenance",
            snapshot_producer == "jg-benchmarker",
            f"produced_by: {snapshot_producer!r}" + ("" if snapshot_producer == "jg-benchmarker" else " (expected 'jg-benchmarker')"),
        ))

    results.append(check("07_report_exists", report_path.exists(), str(report_path)))
    if not report_path.exists():
        return results
    content = report_path.read_text()
    content_lower = content.lower()

    has_report_provenance = bool(re.search(r"produced\s+by[:\s*]*\s*jg-benchmarker", content, re.IGNORECASE))
    results.append(check("07_report_provenance", has_report_provenance, "Report has 'Produced by: jg-benchmarker' line"))

    has_eval_table = bool(re.search(r"\|.*agent.*\|.*model.*\|.*verdict.*\|", content, re.IGNORECASE))
    if not has_eval_table:
        has_eval_table = bool(re.search(r"\|.*\|.*\|.*\|", content)) and "verdict" in content_lower
    results.append(check("07_has_eval_table", has_eval_table, "Agent evaluation table with verdicts"))

    for section_pattern in [r"recommend", r"cost\s*impact"]:
        has_section = bool(re.search(rf"#+\s*.*{section_pattern}", content, re.IGNORECASE))
        results.append(check(f"07_section_{section_pattern.replace(chr(92), '').replace('s*', '_')}", has_section, f"Section matching '{section_pattern}'"))

    agent_names = ["planner", "worker", "tester", "reviewer", "debugger", "subplanner", "git", "benchmarker", "linter"]
    found_agents = sum(1 for a in agent_names if a in content_lower)
    results.append(check("07_agent_count", found_agents >= 5, f"{found_agents} agent names (need >=5)"))

    jg_refs = set(re.findall(r"jg-[\w-]+", content_lower))
    if jg_refs:
        agents_dirs = [
            EXPERT_DIR / "agents",
            REPO_ROOT / ".cursor-practitioner" / "agents",
            SANDBOX_DIR / ".cursor" / "agents",
        ]
        real_agents: set[str] = set()
        for d in agents_dirs:
            if d.is_dir():
                real_agents.update(p.stem for p in d.glob("*.md"))
        unrecognized = [a for a in jg_refs if a not in real_agents and a.replace("-fast", "").replace("-high", "") not in real_agents]
        results.append(check(
            "07_agent_names_valid",
            len(unrecognized) == 0,
            f"All {len(jg_refs)} jg-* names map to real agent files" if not unrecognized
            else f"Unrecognized agents (no .md file): {sorted(unrecognized)[:5]}",
        ))

    verdicts = ["excellent", "correct", "monitor", "tune", "upgrade"]
    found_verdicts = sum(1 for v in verdicts if v in content_lower)
    results.append(check("07_verdict_terms", found_verdicts >= 5, f"{found_verdicts}/5 verdict terms found"))

    results.append(check_word_count(content, 150, "07_report_length"))

    return results


def check_ex08() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    path = OUTPUTS_DIR / "08-evaluation-rubrics.md"
    results.append(check("08_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    results.extend(check_sections(
        content,
        ["Plan Quality Rubric", "Plan Evaluations", "Review Quality Rubric", "Improvement Recommendations"],
        "08_section",
    ))
    results.append(check_word_count(content, 200, "08_depth"))
    return results


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05, 6: check_ex06, 7: check_ex07, 8: check_ex08}

if __name__ == "__main__":
    verifier_main(CHECKERS, "Expert tutorial verifier")
