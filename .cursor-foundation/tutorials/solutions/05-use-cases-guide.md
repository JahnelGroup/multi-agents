# Document Use Cases -- Solution Guide

This exercise is open-ended (portfolio), so there is no single correct answer. The exemplar in `outputs/05-use-cases.md` shows one strong response. Here are the key points a good answer should demonstrate.

## What makes a strong use case document

### Task description
- 2-3 sentences that specify the change scope, not just "add feature X"
- Mentions file count and domains touched (signals for complexity classification)
- Identifies whether the task is trivial, standard, or complex

### Agent mapping
- Maps specific pipeline agents to the task, not generic roles
- Uses the correct agent names (`jg-subplanner`, `jg-worker`, etc.)
- For complex tasks, considers high-tier agents and explains why
- Includes all stages: planning through git

### Artifacts produced
- Lists all pipeline artifacts that would be created
- Includes conditional artifacts (e.g., `debug-diagnosis.json` "if tests fail")
- Uses correct artifact filenames from the pipeline schema

### Why multi-agent
- Explains the specific benefit for THIS task, not generic multi-agent advantages
- Common strong arguments: separation of concerns prevents scope drift, dedicated review catches domain-specific issues, traceable handoffs create audit trails
- Avoids circular reasoning ("multi-agent is better because we use multiple agents")

## Common mistakes
- Listing agents without explaining what each does for this specific task
- Omitting the debugger from complex scenarios
- Not distinguishing between standard and high-tier agents for security-critical tasks
- Writing "Why multi-agent" sections that are too generic and could apply to any task
