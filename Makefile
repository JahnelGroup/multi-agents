# Multi-agents training repo — Makefile
#
# Grader:  make test-all          (or ./test-all.sh)
# Reset:   make reset             (wipe outputs before re-running course)
# Phase:   make phase-2           (grade a single tier)
#
# See TESTING.md for full documentation.

.PHONY: reset phase-0 phase-1 phase-2 phase-3 phase-4 test-all docs-check

# Wipe all learner-generated outputs so the course can be re-run from scratch.
# Restores sandbox/src/app.ts to the clean base (no auth/notification imports).
reset:
	rm -rf .pipeline/
	rm -rf docs/foundation/tutorials/outputs/
	rm -rf docs/practitioner/tutorials/outputs/
	rm -rf docs/expert/tutorials/outputs/
	rm -rf sandbox/.pipeline/
	rm -rf sandbox/.cursor/
	rm -rf sandbox/.git/
	rm -rf sandbox/src/auth/
	rm -rf sandbox/src/notifications/
	rm -rf sandbox/docs/
	@if [ -d sandbox ]; then rm -rf sandbox/node_modules/ sandbox/dist/; fi
	@if [ -d sandbox/src ]; then printf 'import express from "express";\n\nconst app = express();\napp.use(express.json());\n\napp.get("/", (_req, res) => {\n  res.json({ status: "ok" });\n});\n\nif (require.main === module) {\n  app.listen(3000, () => {\n    console.log("Sandbox listening on port 3000");\n  });\n}\n\nexport { app };\n' > sandbox/src/app.ts; fi
	@if [ -f sandbox/package.json ]; then cd sandbox && npm install --silent 2>/dev/null; fi
	@echo "[DONE] Reset complete. Sandbox restored to base state."

# Phase 0: Gitignore — ensure generated artifacts are ignored
phase-0:
	@echo "Phase 0: Gitignore"
	@git check-ignore -v sandbox/node_modules/package 2>/dev/null && echo "PASS: node_modules ignored" || (echo "FAIL: node_modules not ignored"; exit 1)
	@git check-ignore -v docs/foundation/tutorials/outputs/foo 2>/dev/null && echo "PASS: tutorials/outputs ignored" || (echo "FAIL: tutorials/outputs not ignored"; exit 1)

# Phase 1: Sandbox — exists, installs, tests and typecheck pass
phase-1:
	@echo "Phase 1: Sandbox"
	@test -f sandbox/package.json || (echo "FAIL: sandbox/package.json missing"; exit 1)
	@test -f sandbox/src/app.ts || (echo "FAIL: sandbox/src/app.ts missing"; exit 1)
	@cd sandbox && npm install && npm test && npm run typecheck

# Phase 2: Foundation tutorials — verify.py --all
phase-2:
	@echo "Phase 2: Foundation tutorials"
	@python3 docs/foundation/tutorials/verify.py --all

# Phase 3: Practitioner tutorials — verify.py --all
phase-3:
	@echo "Phase 3: Practitioner tutorials"
	@python3 docs/practitioner/tutorials/verify.py --all

# Phase 4: Expert tutorials — verify.py --all
phase-4:
	@echo "Phase 4: Expert tutorials"
	@python3 docs/expert/tutorials/verify.py --all

# Grade all phases
test-all: phase-0 phase-1 phase-2 phase-3 phase-4
	@echo ""
	@echo "=== All phases PASS ==="

# Documentation integrity checks
docs-check:
	bash scripts/check-docs.sh

# Documentation site
docs-serve:
	pip install -r requirements-docs.txt
	mkdocs serve

docs-build:
	pip install -r requirements-docs.txt
	mkdocs build --strict
