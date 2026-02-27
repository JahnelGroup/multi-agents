# Rules & Skills Design -- Solution Guide

This is a portfolio exercise. The exemplar in `outputs/06-config-design.md` shows a strong response. Key evaluation criteria:

## Required sections (all 5 must be present)

### Rules Design (3 rules)
Each rule must specify:
- Filename, frontmatter (`description`, `alwaysApply`, `globs`)
- When to Apply, Rule Content, Exempt sections
- Strong answers explain WHY each frontmatter choice was made

### Skills Design (2 skills)
Each skill must specify:
- Directory name, SKILL.md frontmatter (`name`, `description`)
- When to Use, How to Execute, Output Format, Anti-patterns
- Strong answers make the `description` specific enough for accurate activation

### Agent Inventory
- Table with 10+ agents including tiered variants
- Must include `team-security-scanner` and `team-compliance-auditor`

### AGENTS.md Registry
- Pipeline execution order (numbered steps)
- Subagent type mapping table
- Tier routing table (trivial/standard/complex)

### Activation Flow
- Mermaid diagram showing rule/skill/agent interactions
- Must show when rules are checked (before dispatch, before commit)
- Must show when skills are loaded (on-demand)

## Common mistakes

- Setting `alwaysApply: true` on rules that only apply at specific pipeline stages
- Writing `description` fields too vague for accurate activation
- Missing the PCI-DSS override in the tier routing table
- Not including anti-patterns in skill definitions
