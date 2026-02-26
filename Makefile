# Multi-agents test suite — aligned to TESTING.md
# Run: make test-all

.PHONY: reset phase-0 phase-2 phase-3 phase-4 phase-5 test-all reset-and-test

# Reset procedure (optional; run before full rerun)
reset:
	rm -rf .pipeline/
	rm -rf .cursor-foundation/tutorials/outputs/
	rm -rf .cursor-practitioner/tutorials/outputs/
	rm -rf .cursor-expert/tutorials/outputs/
	rm -rf sandbox/.pipeline/
	@if [ -d sandbox ]; then rm -rf sandbox/node_modules/ sandbox/dist/; fi

# Phase 0: Gitignore — ensure generated artifacts are ignored
phase-0:
	@echo "Phase 0: Gitignore"
	@git check-ignore -v sandbox/node_modules/package 2>/dev/null && echo "PASS: node_modules ignored" || (echo "FAIL: node_modules not ignored"; exit 1)
	@git check-ignore -v .cursor-foundation/tutorials/outputs/foo 2>/dev/null && echo "PASS: tutorials/outputs ignored" || (echo "FAIL: tutorials/outputs not ignored"; exit 1)

# Phase 2: Sandbox — exists, installs, tests and typecheck pass
phase-2:
	@echo "Phase 2: Sandbox"
	@test -f sandbox/package.json || (echo "FAIL: sandbox/package.json missing"; exit 1)
	@test -f sandbox/src/app.ts || (echo "FAIL: sandbox/src/app.ts missing"; exit 1)
	@cd sandbox && npm install && npm test && npm run typecheck

# Phase 3: Foundation tutorials — verify.py --all
phase-3:
	@echo "Phase 3: Foundation tutorials"
	@python3 .cursor-foundation/tutorials/verify.py --all

# Phase 4: Practitioner tutorials — verify.py --all
phase-4:
	@echo "Phase 4: Practitioner tutorials"
	@python3 .cursor-practitioner/tutorials/verify.py --all

# Phase 5: Expert tutorials — verify.py --all
phase-5:
	@echo "Phase 5: Expert tutorials"
	@python3 .cursor-expert/tutorials/verify.py --all

# Full test sequence (Phases 0, 2, 3, 4, 5; Phase 1 is manual)
test-all: phase-0 phase-2 phase-3 phase-4 phase-5
	@echo ""
	@echo "=== All phases PASS ==="

# Reset then test (convenience for fresh runs)
reset-and-test: reset
	@cd sandbox && npm install --silent
	@$(MAKE) test-all
