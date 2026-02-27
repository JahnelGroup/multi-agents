# Claude Code

Pipeline concepts from this training are IDE-agnostic. If you use Claude Code instead of Cursor, you can adapt the setup. This page consolidates all Claude Code references from across the repo.

## Concept mapping table

| Cursor | Claude Code |
|--------|-------------|
| `.cursor/rules/*.mdc` | `CLAUDE.md` at repo root |
| `.cursor/agents/*.md` | Instructions referenced in `CLAUDE.md` |
| `.cursor/skills/*/SKILL.md` | `.claude/commands/*.md` |
| `subagent_type` dispatch | Sequential prompting through stages |

## What transfers directly

Artifacts, pipeline concepts, agent roles, and stage gates are IDE-agnostic. The same `plan.json`, `worker-result.json`, `test-result.json`, `review-result.json`, `debug-diagnosis.json`, and `git-result.json` work in both environments. Walkthrough content and pipeline artifacts are portable.

## What differs

| Aspect | Cursor | Claude Code |
|--------|--------|-------------|
| **Wiring mechanism** | `subagent_type` dispatch — Task tool invokes specialized subagents | Sequential prompting — you prompt through stages in order |
| **Rule activation** | Frontmatter + `description`; Cursor decides when to include rules | `CLAUDE.md` directives; you structure instructions in one file |
| **Skill discovery** | `.cursor/skills/*/SKILL.md`; Cursor surfaces skills to agents | `.claude/commands/*.md`; you reference commands explicitly |
| **Tiered routing** | `jg-tier-routing.mdc` + subagent dispatch with tier suffixes | Routing logic in `CLAUDE.md`; model selection per prompt |

## Migration path

To adapt the `.cursor/` setup for Claude Code:

1. **Convert rules to `CLAUDE.md` sections** — Extract the body of each `.mdc` rule and add it as a section in `CLAUDE.md`. Include the jg-planner-first gate, tier routing logic, and any team rules.

2. **Convert skills to `.claude/commands/`** — Each `SKILL.md` becomes a command file. The jg-pipeline-artifact-io skill (artifact layout, read/write conventions) maps to a command that agents invoke when reading or writing pipeline artifacts.

3. **Use sequential prompting instead of subagent dispatch** — Instead of `Task(subagent_type="jg-subplanner", ...)`, prompt: "You are the subplanner. Read the issue and produce plan.json at .pipeline/<issue-id>/plan.json." Then: "You are the worker. Read plan.json and implement..." and so on. Model selection per stage replaces tier-based subagent selection.

4. **Preserve artifact schemas** — The `pipeline/schema.py` and artifact shapes in `pipeline/README.md` apply unchanged. Validation and stage-gate checks work the same.
