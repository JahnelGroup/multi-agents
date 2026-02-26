# Walkthrough: Add user authentication middleware

Step-by-step narration of the full pipeline run for issue #42.

---

## 1. Planner reads issue

**Agent:** Planner  
**Reads:** Issue #42 (scenario.md)  
**Action:** Classifies as standard complexity (3+ files, auth domain). Invokes subplanner.

---

## 2. Subplanner produces plan

**Agent:** Subplanner  
**Reads:** Issue #42  
**Writes:** plan.json  
**Actions:** Produces plan with 5 ordered steps across 4 files (login.ts, middleware.ts, login.test.ts, middleware.test.ts). Maps AC1→login.test.ts, AC2/AC3→middleware.test.ts. Self-assessment: high confidence.

---

## 3. Worker implements

**Agent:** Worker  
**Reads:** plan.json  
**Writes:** worker-result.json, src/auth/login.ts, src/auth/middleware.ts, src/auth/login.test.ts, src/auth/middleware.test.ts  
**Actions:** Implements all 4 files per plan. Status: completed.

---

## 4. Tester runs Phase 1 — FAIL

**Agent:** Tester  
**Reads:** worker-result.json, source files  
**Writes:** test-result-fail.json  
**Actions:** Runs lint (PASS), typecheck (PASS), unit_tests (FAIL). Expired token test fails: middleware returns 200 instead of 401. Verdict: FAIL.

---

## 5. Planner routes to debugger

**Agent:** Planner  
**Reads:** test-result-fail.json  
**Action:** Sees FAIL verdict, routes to debugger.

---

## 6. Debugger diagnoses

**Agent:** Debugger  
**Reads:** test-result-fail.json, src/auth/middleware.ts  
**Writes:** debug-diagnosis.json  
**Actions:** Parses test output, inspects middleware. Identifies off-by-one: expiry check uses `>` instead of correct logic. Root cause: line 15 in middleware.ts. Classification: fix_target. Provides fix instructions (change to `decoded.exp <= now` for rejection).

---

## 7. Planner re-dispatches worker

**Agent:** Planner  
**Reads:** debug-diagnosis.json  
**Action:** Re-dispatches worker with fix instructions.

---

## 8. Worker applies fix

**Agent:** Worker  
**Reads:** debug-diagnosis.json, src/auth/middleware.ts  
**Writes:** Updated worker-result.json, updated src/auth/middleware.ts  
**Actions:** Fixes expiry comparison on line 15.

---

## 9. Tester runs again — PASS

**Agent:** Tester  
**Reads:** Updated worker-result.json, source files  
**Writes:** test-result-pass.json  
**Actions:** Runs Phase 1. Lint PASS, typecheck PASS, unit_tests PASS. Verdict: PASS.

---

## 10. Reviewer reviews

**Agent:** Reviewer  
**Reads:** plan.json, diff of changed files  
**Writes:** review-result.json  
**Actions:** Reviews diff against plan. 0 blockers, 0 concerns, 2 nits (JWT_SECRET env config, unused import). Verdict: PASS.

---

## 11. Git creates branch and PR

**Agent:** Git  
**Reads:** review-result.json, changed files  
**Writes:** git-result.json  
**Actions:** Creates branch `feature/issue-42-auth-middleware`, commits with message `feat(auth): add login endpoint and JWT middleware\n\nCloses #42`, opens PR #87. CI status: pass.
