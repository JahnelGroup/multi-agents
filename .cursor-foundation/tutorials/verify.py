#!/usr/bin/env python3
"""Foundation tutorial exercise verifier."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TUTORIALS_DIR = Path(__file__).resolve().parent
FOUNDATION_DIR = TUTORIALS_DIR.parent
REPO_ROOT = FOUNDATION_DIR.parent
OUTPUTS_DIR = TUTORIALS_DIR / "outputs"
ANSWERS_DIR = TUTORIALS_DIR / "answers"

GLOSSARY_DEFS = {
    "agent": "An AI that uses tools in a loop to accomplish a task",
    "subagent": "A specialized agent spawned by the main agent for a specific role",
    "rule": "A `.mdc` file that gives the AI persistent instructions",
    "skill": "A reusable instruction set for a specific task",
    "artifact": "A JSON file one agent writes and another reads",
    "pipeline": "A sequence of agents that pass work forward via artifacts",
    "frontmatter": "YAML metadata at the top of a rule or agent file (between `---` markers)",
    "acceptance criteria": "Conditions that define when a task is done",
}

PATTERN_ANSWERS = {
    1: {"agents": ["planner", "jg-planner"], "artifact": "plan.json"},
    2: {"agents": ["worker", "jg-worker"], "artifact": "worker-result.json"},
    3: {"agents": ["git", "jg-git"], "artifact": "git-result.json"},
    4: {"agents": ["debugger", "jg-debugger"], "artifact": "debug-diagnosis.json"},
}

ANATOMY_WRITERS = {
    "plan.json": ["subplanner", "jg-subplanner"],
    "worker-result.json": ["worker", "jg-worker"],
    "debug-diagnosis.json": ["debugger", "jg-debugger"],
}


def check(name: str, passed: bool, msg: str) -> tuple[str, bool, str]:
    return (name, passed, msg)


def check_ex01() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "01-vocabulary.md"
    results.append(check("01_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    terms = list(GLOSSARY_DEFS.keys())
    for term in terms:
        pattern = rf"^##\s+{re.escape(term)}"
        has_heading = bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))
        results.append(check(f"01_has_{term.replace(' ', '_')}", has_heading, f"Heading for '{term}'"))
    sections = re.split(r"^##\s+", content, flags=re.MULTILINE)[1:]
    for section in sections:
        lines = section.strip().split("\n", 1)
        term_name = lines[0].strip().lower()
        body = lines[1].strip() if len(lines) > 1 else ""
        word_count = len(body.split())
        results.append(check(f"01_{term_name.replace(' ', '_')}_length", word_count >= 10, f"{word_count} words (need >=10)"))
        if term_name in GLOSSARY_DEFS:
            is_verbatim = GLOSSARY_DEFS[term_name].lower() in body.lower()
            results.append(check(f"01_{term_name.replace(' ', '_')}_original", not is_verbatim, "Not verbatim copy"))
    return results


def check_ex02() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "02-patterns.md"
    results.append(check("02_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text().lower()
    for num, expected in PATTERN_ANSWERS.items():
        section_match = re.search(rf"##\s*scenario\s*{num}(.*?)(?=##\s*scenario|\Z)", content, re.DOTALL)
        if not section_match:
            results.append(check(f"02_scenario_{num}_exists", False, f"Scenario {num} section"))
            continue
        results.append(check(f"02_scenario_{num}_exists", True, f"Scenario {num} section"))
        section = section_match.group(1)
        agent_match = any(a in section for a in expected["agents"])
        results.append(check(f"02_scenario_{num}_agent", agent_match, f"Expected one of {expected['agents']}"))
        artifact_match = expected["artifact"] in section
        results.append(check(f"02_scenario_{num}_artifact", artifact_match, f"Expected {expected['artifact']}"))
    return results


def check_ex03() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "03-annotations.md"
    results.append(check("03_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    for artifact_name, expected_writers in ANATOMY_WRITERS.items():
        has_section = bool(re.search(rf"##\s*{re.escape(artifact_name)}", content, re.IGNORECASE))
        results.append(check(f"03_{artifact_name}_section", has_section, f"Section for {artifact_name}"))
        section_match = re.search(rf"##\s*{re.escape(artifact_name)}(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
        if section_match:
            section = section_match.group(1).lower()
            for sub in ["writer", "required fields", "consumer"]:
                has_sub = sub in section
                results.append(check(f"03_{artifact_name}_{sub.replace(' ', '_')}", has_sub, f"Has '{sub}' subsection"))
            writer_match = any(w in section for w in expected_writers)
            results.append(check(f"03_{artifact_name}_writer_correct", writer_match, f"Writer is one of {expected_writers}"))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results = []
    pipeline_dir = REPO_ROOT / ".pipeline" / "HEALTH-01"
    artifacts = ["plan.json", "worker-result.json", "git-result.json"]
    for name in artifacts:
        path = pipeline_dir / name
        results.append(check(f"04_{name}_exists", path.exists(), str(path)))
        if path.exists():
            schema_py = FOUNDATION_DIR / "pipeline" / "schema.py"
            if schema_py.exists():
                proc = subprocess.run(
                    [sys.executable, str(schema_py), "--validate", str(path)],
                    capture_output=True, text=True,
                )
                passed = proc.returncode == 0
                results.append(check(f"04_{name}_valid", passed, proc.stdout.strip() or proc.stderr.strip()))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results = []
    path = OUTPUTS_DIR / "05-use-cases.md"
    results.append(check("05_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    for i in range(1, 4):
        has_case = bool(re.search(rf"##\s*use\s*case\s*{i}", content, re.IGNORECASE))
        results.append(check(f"05_use_case_{i}_exists", has_case, f"Use Case {i}"))
    for sub in ["task description", "agent mapping", "artifacts produced", "why multi-agent"]:
        count = len(re.findall(rf"\*?\*?{re.escape(sub)}\*?\*?", content, re.IGNORECASE))
        results.append(check(f"05_has_{sub.replace(' ', '_')}", count >= 3, f"Found {count} instances (need >=3)"))
    why_sections = re.findall(r"(?:why multi-agent).*?\n(.*?)(?=\n##|\n\*\*|\Z)", content, re.IGNORECASE | re.DOTALL)
    for i, section in enumerate(why_sections):
        word_count = len(section.split())
        results.append(check(f"05_why_{i+1}_length", word_count >= 20, f"{word_count} words (need >=20)"))
    return results


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05}


def main() -> None:
    parser = argparse.ArgumentParser(description="Foundation tutorial verifier")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--exercise", type=int, choices=range(1, 6), help="Exercise number (1-5)")
    group.add_argument("--all", action="store_true", help="Run all exercises")
    args = parser.parse_args()

    exercises = list(CHECKERS.keys()) if args.all else [args.exercise]
    all_results: list[tuple[str, bool, str]] = []

    for ex in exercises:
        results = CHECKERS[ex]()
        all_results.extend(results)
        for name, passed, msg in results:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {name}: {msg}")

    passed = sum(1 for _, p, _ in all_results if p)
    total = len(all_results)
    print(f"\n{passed}/{total} checks passed", end="")
    if passed == total:
        print(" -- PASS")
        sys.exit(0)
    else:
        print(" -- FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
