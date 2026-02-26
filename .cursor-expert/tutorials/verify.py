#!/usr/bin/env python3
"""Expert tutorial exercise verifier."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TUTORIALS_DIR = Path(__file__).resolve().parent
EXPERT_DIR = TUTORIALS_DIR.parent
REPO_ROOT = EXPERT_DIR.parent
SANDBOX_DIR = REPO_ROOT / "sandbox"
OUTPUTS_DIR = TUTORIALS_DIR / "outputs"
SCHEMA_PY = EXPERT_DIR / "pipeline" / "schema.py"


def check(name: str, passed: bool, msg: str) -> tuple[str, bool, str]:
    return (name, passed, msg)


def validate_schema(artifact_path: Path) -> tuple[bool, str]:
    if not SCHEMA_PY.exists():
        return False, f"schema.py not found at {SCHEMA_PY}"
    if not artifact_path.exists():
        return False, f"Artifact not found: {artifact_path}"
    proc = subprocess.run(
        [sys.executable, str(SCHEMA_PY), "--validate", str(artifact_path)],
        capture_output=True, text=True,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


EXPECTED_TIERS = {1: "trivial", 3: "complex", 5: "complex"}


def check_ex01() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "01-classifications.json"
    results.append(check("01_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        results.append(check("01_valid_json", False, str(e)))
        return results
    results.append(check("01_valid_json", True, "Valid JSON"))
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


TIER_MAP = {
    "NOTIF-001": {"worker": "fast", "tester": "fast", "reviewer": "fast", "has_plan": False},
    "NOTIF-002": {"worker": "standard", "tester": "standard", "reviewer": "standard", "has_plan": True},
    "NOTIF-003": {"worker": "high", "reviewer": "high", "has_plan": True},
}


def check_ex02() -> list[tuple[str, bool, str]]:
    results = []
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
            results.append(check(f"02_{issue}_no_plan", not plan.exists(), f"Trivial task should skip plan"))
        for artifact in ["worker-result.json", "test-result.json", "review-result.json", "git-result.json"]:
            path = issue_dir / artifact
            results.append(check(f"02_{issue}_{artifact}", path.exists(), str(path)))
            if path.exists():
                passed, msg = validate_schema(path)
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
    return results


def check_ex03() -> list[tuple[str, bool, str]]:
    results = []
    esc_dir = SANDBOX_DIR / ".pipeline" / "NOTIF-002-escalation"
    results.append(check("03_dir_exists", esc_dir.is_dir(), str(esc_dir)))
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
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            results.append(check("03_parse", False, str(e)))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "04-cost-analysis.json"
    results.append(check("04_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        results.append(check("04_valid_json", False, str(e)))
        return results
    results.append(check("04_valid_json", True, "Valid JSON"))
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
    results.append(check("04_recommendation_length", len(rec.split()) >= 20, f"{len(rec.split())} words (need >=20)"))
    results.append(check("04_has_breakeven", "breakeven_analysis" in data, "Has breakeven_analysis"))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "05-architecture.md"
    results.append(check("05_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    sections = [
        "Agent Inventory", "Pipeline Flow", "Tier Routing Rules",
        "Cost Projections", "Monitoring Strategy", "Escalation Policy", "Rollback Plan",
    ]
    for section in sections:
        has_section = bool(re.search(rf"#+\s*{re.escape(section)}", content, re.IGNORECASE))
        results.append(check(f"05_section_{section.lower().replace(' ', '_')}", has_section, f"Section: {section}"))
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


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05}


def main() -> None:
    parser = argparse.ArgumentParser(description="Expert tutorial verifier")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--exercise", type=int, choices=range(1, 6), help="Exercise number (1-5)")
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
