# Multi-agents training repo — Makefile
#
# Grader:  make test-all          (or ./test-all.sh)
# Reset:   make reset             (wipe outputs before re-running course)
# Phase:   make phase-2           (grade a single tier)
#
# See TESTING.md for full documentation.

.PHONY: reset phase-0 phase-1 phase-2 phase-3 phase-4 test-all

# Wipe all learner-generated outputs so the course can be re-run from scratch.
reset:
	rm -rf .pipeline/
	rm -rf .cursor-foundation/tutorials/outputs/
	rm -rf .cursor-practitioner/tutorials/outputs/
	rm -rf .cursor-expert/tutorials/outputs/
	rm -rf sandbox/.pipeline/
	@if [ -d sandbox ]; then rm -rf sandbox/node_modules/ sandbox/dist/; fi
	@echo "[DONE] Reset complete. Run 'cd sandbox && npm install' before grading."

# Phase 0: Gitignore — ensure generated artifacts are ignored
phase-0:
	@echo "Phase 0: Gitignore"
	@git check-ignore -v sandbox/node_modules/package 2>/dev/null && echo "PASS: node_modules ignored" || (echo "FAIL: node_modules not ignored"; exit 1)
	@git check-ignore -v .cursor-foundation/tutorials/outputs/foo 2>/dev/null && echo "PASS: tutorials/outputs ignored" || (echo "FAIL: tutorials/outputs not ignored"; exit 1)

# Phase 1: Sandbox — exists, installs, tests and typecheck pass
phase-1:
	@echo "Phase 1: Sandbox"
	@test -f sandbox/package.json || (echo "FAIL: sandbox/package.json missing"; exit 1)
	@test -f sandbox/src/app.ts || (echo "FAIL: sandbox/src/app.ts missing"; exit 1)
	@cd sandbox && npm install && npm test && npm run typecheck

# Phase 2: Foundation tutorials — verify.py --all
phase-2:
	@echo "Phase 2: Foundation tutorials"
	@python3 .cursor-foundation/tutorials/verify.py --all

# Phase 3: Practitioner tutorials — verify.py --all
phase-3:
	@echo "Phase 3: Practitioner tutorials"
	@python3 .cursor-practitioner/tutorials/verify.py --all

# Phase 4: Expert tutorials — verify.py --all
phase-4:
	@echo "Phase 4: Expert tutorials"
	@python3 .cursor-expert/tutorials/verify.py --all

# Grade all phases
test-all: phase-0 phase-1 phase-2 phase-3 phase-4
	@echo ""
	@echo "=== All phases PASS ==="
