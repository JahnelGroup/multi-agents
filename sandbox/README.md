# Tutorial Sandbox

Minimal Express/TypeScript project used by Practitioner and Expert tier tutorial exercises.

## Setup

```bash
npm install
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm test` | Run tests (Jest) |
| `npm run typecheck` | TypeScript type checking |
| `npm start` | Start dev server on port 3000 |

## Usage

This project starts with a single `GET /` route. Tutorial exercises add routes, middleware, and tests to it.

To reset after completing exercises:

```bash
git checkout -- sandbox/
```
