# Sandbox

Minimal Express/TypeScript app used as the target codebase for Practitioner and Expert tutorial exercises. Exercises add features (auth, notifications, WebSocket) via the multi-agent pipeline, then validate the results.

## Setup

```bash
npm install
```

## Commands

| Command | Description |
|---------|-------------|
| `npm test` | Run Jest test suites |
| `npm run typecheck` | Run TypeScript compiler checks |
| `npm start` | Start dev server on port 3000 |
| `npm run lint` | Run ESLint on `src/` |

## Reset

From the repo root:

```bash
make reset
```

This wipes all exercise-generated files and restores the sandbox to its base state (`src/app.ts`, `package.json`, clean `node_modules`).

## Exercise output

Directories like `src/auth/`, `src/notifications/`, and `docs/` are created during exercises and gitignored. They do not ship with the repo. Pipeline artifacts go to `.pipeline/` (also gitignored).
