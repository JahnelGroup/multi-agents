# Foundation agents — index

This tier uses 3 agents for learning concepts only. For production use, copy `.cursor-practitioner/` into your project as `.cursor/`.

| Agent | Model | Role | Reads | Writes |
|-------|--------|------|--------|--------|
| **jg-planner** | gemini-3.1-pro | Orchestrates plan → implement → git | Issue | plan.json |
| **jg-worker** | gpt-5.3-codex | Implements code and tests per plan | plan.json | worker-result.json |
| **jg-git** | gemini-3-flash | Branch, commit, PR (no merge) | (git state) | git-result.json |
