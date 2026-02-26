---
name: jg-<role>
model: gemini-3.1-pro
description: <one-line description for Cursor. Use when ...>
readonly: true
---

# JG-<ROLE>

## ROLE

<What this agent owns. One paragraph.>

## PRIMARY OBJECTIVE

<Single sentence.>

## CORE RESPONSIBILITIES

- <Responsibility 1>
- <Responsibility 2>
- If this agent reads/writes pipeline artifacts: paths are `.pipeline/<issue-id>/<artifact>.json`. Schema: **pipeline/README.md** in this bundle.
- <...>

## NON-GOALS

- Does not <...>
- Does not <...>

## OUTPUT / ARTIFACT (if applicable)

Write to `.pipeline/<issue-id>/<filename>.json`. Required fields: see **pipeline/README.md**. Add the new artifact to pipeline/README.md and pipeline/schema.py REQUIRED if you add a new artifact type.

## DECISION FRAMEWORK (optional)

<When in doubt, ...>
