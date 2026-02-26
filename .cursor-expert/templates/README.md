# JG templates

Use these when adding new jg- agents, rules, or when generating pipeline artifacts.

| File | Use |
|------|-----|
| **agent.md** | New jg- agent. Copy to `agents/jg-<role>.md`, fill name/model/description and sections. Add to AGENTS.md and pipeline docs if the agent reads/writes artifacts. |
| **rule.mdc** | New jg- rule. Copy to `rules/jg-<name>.mdc`, set description and alwaysApply. |
| **plan.json.example** | Example plan artifact. Reference only; do not commit as real artifact. |
| **worker-result.json.example** | Example worker result. |
| **test-result.json.example** | Example test result. |
| **review-result.json.example** | Example review result. |
| **debug-diagnosis.json.example** | Example debugger diagnosis. |
| **git-result.json.example** | Example git result. |
| **state.yaml.example** | Example planner state for resume and long-running work. |
| **lessons.yaml.example** | Example cross-run lessons file (optional; planner reads at start). |

For new artifact types: add the shape to **pipeline/README.md** and add the filename and required keys to **pipeline/schema.py** REQUIRED dict.
