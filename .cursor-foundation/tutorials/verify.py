#!/usr/bin/env python3
"""Foundation tutorial exercise verifier."""
from __future__ import annotations

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

_HELPERS_DIR = str(REPO_ROOT / "lib")
if _HELPERS_DIR not in sys.path:
    sys.path.insert(0, _HELPERS_DIR)

from verify_helpers import (  # noqa: E402
    check,
    check_json_has_keys,
    check_sections,
    check_word_count,
    load_and_validate_json,
    validate_schema_with,
    verifier_main,
)

GLOSSARY_DEFS = {
    "agent": "An AI that uses tools in a loop to accomplish a task",
    "subagent": "A specialized agent spawned by the main agent for a specific role",
    "rule": "A `.mdc` file that gives the AI persistent instructions",
    "skill": "A reusable instruction set for a specific task",
    "artifact": "A JSON file one agent writes and another reads",
    "pipeline": "A sequence of agents that pass work forward via artifacts",
    "frontmatter": "YAML metadata at the top of a rule or agent file (between `---` markers)",
    "acceptance criteria": "Conditions that define when a task is done",
    "state": "A checkpoint of pipeline progress that enables resuming interrupted work",
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


def check_ex01() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
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
        results.append(check_word_count(body, 10, f"01_{term_name.replace(' ', '_')}_length"))
        if term_name in GLOSSARY_DEFS:
            is_verbatim = GLOSSARY_DEFS[term_name].lower() in body.lower()
            results.append(check(f"01_{term_name.replace(' ', '_')}_original", not is_verbatim, "Not verbatim copy"))
    return results


def check_ex02() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
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
    results: list[tuple[str, bool, str]] = []
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
                results.append(check(f"03_{artifact_name}_{sub.replace(' ', '_')}", sub in section, f"Has '{sub}' subsection"))
            writer_match = any(w in section for w in expected_writers)
            results.append(check(f"03_{artifact_name}_writer_correct", writer_match, f"Writer is one of {expected_writers}"))
    return results


def check_ex04() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    pipeline_dir = REPO_ROOT / ".pipeline" / "HEALTH-01"
    artifacts = ["plan.json", "worker-result.json", "git-result.json"]
    schema_py = FOUNDATION_DIR / "pipeline" / "schema.py"
    for name in artifacts:
        path = pipeline_dir / name
        results.append(check(f"04_{name}_exists", path.exists(), str(path)))
        if path.exists():
            passed, msg = validate_schema_with(schema_py, path)
            results.append(check(f"04_{name}_valid", passed, msg))
    return results


def check_ex05() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
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
    why_sections = re.findall(
        r"(?:\*{0,2})why\s+multi[\s-]*agent(?:\*{0,2})\s*:?\s*(.+?)(?=\n##|\n\*\*[A-Z]|\Z)",
        content, re.IGNORECASE | re.DOTALL,
    )
    for i, section in enumerate(why_sections):
        results.append(check_word_count(section, 20, f"05_why_{i+1}_length"))
    return results


def check_ex06() -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    path = OUTPUTS_DIR / "06-configuration.md"
    results.append(check("06_file_exists", path.exists(), str(path)))
    if not path.exists():
        return results
    content = path.read_text()
    content_lower = content.lower()

    results.extend(check_sections(content, ["rules", "skills", "agents", "quiz answers"], "06_section"))

    rules_match = re.search(r"##\s*rules(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if rules_match:
        rules_text = rules_match.group(1).lower()
        for term in ["description", "alwaysapply", "globs", ".mdc"]:
            results.append(check(f"06_rules_mentions_{term}", term in rules_text, f"Rules mentions '{term}'"))

    skills_match = re.search(r"##\s*skills(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if skills_match:
        skills_text = skills_match.group(1).lower()
        for term in ["name", "skill.md", "description"]:
            results.append(check(f"06_skills_mentions_{term}", term in skills_text, f"Skills mentions '{term}'"))

    agents_match = re.search(r"##\s*agents(.*?)(?=##\s*quiz|\Z)", content, re.DOTALL | re.IGNORECASE)
    if agents_match:
        agents_text = agents_match.group(1).lower()
        for term in ["name", "model", "readonly"]:
            results.append(check(f"06_agents_mentions_{term}", term in agents_text, f"Agents mentions '{term}'"))

    quiz_match = re.search(r"##\s*quiz\s*answers(.*?)(?=^##[^#]|\Z)", content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if quiz_match:
        quiz_text = quiz_match.group(1)
        answers = re.split(r"\n\s*\d+[\.\)]\s+|\n\s*-\s+|\n\s*\*\*\d+[\.\)]\s*\*\*\s*|\n#{3,}\s+", quiz_text)
        answers = [a.strip() for a in answers if len(a.strip().split()) >= 5]
        results.append(check("06_quiz_count", len(answers) >= 4, f"{len(answers)} answers (need >=4)"))
        for i, answer in enumerate(answers[:4]):
            results.append(check_word_count(answer, 15, f"06_quiz_{i+1}_length"))
    else:
        results.append(check("06_quiz_section_found", False, "Quiz Answers section not found"))

    return results


CHECKERS = {1: check_ex01, 2: check_ex02, 3: check_ex03, 4: check_ex04, 5: check_ex05, 6: check_ex06}

if __name__ == "__main__":
    verifier_main(CHECKERS, "Foundation tutorial verifier", show_exercise_headers=False)
