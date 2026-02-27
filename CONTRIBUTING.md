# Contributing

Thanks for your interest in improving the multi-agents training repo.

Before you start, read the [README](README.md) for prerequisites, repository structure, naming conventions, and maintenance policy.

## Development setup

```bash
cd sandbox && npm install

make reset
```

`make reset` wipes all generated outputs and restores the sandbox to its base state.

## Running tests

```bash
./test-all.sh              # all phases
./test-all.sh --phase 2    # Foundation only
./test-all.sh --phase 3    # Practitioner only
./test-all.sh --phase 4    # Expert only
```

Or via Make targets:

```bash
make test-all
make phase-2    # Foundation
make phase-3    # Practitioner
make phase-4    # Expert
```

## What not to commit

Runtime artifacts are excluded via [`.gitignore`](.gitignore). Never commit anything from `.pipeline/`, `tutorials/outputs/`, or `sandbox/node_modules/`.

## Pull request expectations

1. **Indicate affected tier(s)** — the PR template includes a checklist for this.
2. **Update root `.cursor/` first** if you changed any shared agents, rules, skills, or pipeline files.
3. **Run the grader** — `make test-all` should pass before opening the PR.
4. **Follow naming conventions** — see [README](README.md#naming-convention).
5. **Don't commit runtime artifacts** — nothing from `.pipeline/` or `tutorials/outputs/`.
6. **Keep PRs focused** — one logical change per PR when possible.
