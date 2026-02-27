# Sandbox

Minimal Express/TypeScript app used as the target codebase for Practitioner and Expert tutorial exercises. Exercises add features (auth, notifications, WebSocket) via the multi-agent pipeline, then validate the results.

## Setup and commands

All npm commands run from this directory (`sandbox/`):

```bash
npm install          # install dependencies
npm test             # run Jest test suites
npm run typecheck    # run TypeScript compiler checks
npm start            # start dev server on port 3000
npm run lint         # run ESLint on src/
```

## Reset

Run from the **repo root** (one level up):

```bash
cd ..
make reset
```

This wipes all exercise-generated files and restores the sandbox to its base state (`src/app.ts`, `package.json`, clean `node_modules`).

## Exercise output

Directories like `src/auth/`, `src/notifications/`, and `docs/` are created during exercises and gitignored. They do not ship with the repo. Pipeline artifacts go to `.pipeline/` (also gitignored).
