# Routing Log — Notification System Walkthrough

Documentation of every routing decision across all 3 issues.

---

## NOTIF-001: Define notification API contract

### Classification

| Field | Value |
|-------|-------|
| **Issue ID** | NOTIF-001 |
| **Initial complexity** | Trivial |
| **Signals used** | File count: 2; domain: types/docs only; no cross-service integration; no tests beyond lint/typecheck |

### Tier selection

| Stage | Tier | Agent invoked |
|-------|------|---------------|
| Plan | Fast | (skip) |
| Implement | Fast | jg-worker-fast |
| Test | Fast | jg-tester-fast |
| Review | Fast | jg-reviewer-fast |
| Git | — | jg-git |

### Escalation events

None.

### Final outcome

- **Tier used**: Fast
- **Result**: PASS (all stages)
- **Branch**: `feature/notif-001-api-contract`
- **PR**: #101

---

## NOTIF-002: Implement notification service

### Classification

| Field | Value |
|-------|-------|
| **Issue ID** | NOTIF-002 |
| **Initial complexity** | Standard |
| **Signals used** | File count: 4; domain: service + repository + tests; cross-service integration (user service); unit + integration tests |

### Tier selection

| Stage | Tier | Agent invoked |
|-------|------|---------------|
| Plan | Standard | jg-subplanner |
| Implement | **Standard** (escalated from fast) | jg-worker |
| Test | Standard | jg-tester |
| Review | Standard | jg-reviewer |
| Git | — | jg-git |

### Escalation events

| From | To | Reason |
|------|-----|--------|
| Fast | Standard | Multi-file change with cross-service integration exceeds fast scope |

**Trigger**: jg-worker-fast invoked initially; worker determined scope (4 files, user service integration) exceeded fast tier capacity and requested escalation.

### Final outcome

- **Tier used**: Standard (after escalation at implement stage)
- **Result**: PASS (all stages)
- **Branch**: `feature/notif-002-service`
- **PR**: #102

---

## NOTIF-003: Add real-time WebSocket delivery with rate limiting

### Classification

| Field | Value |
|-------|-------|
| **Issue ID** | NOTIF-003 |
| **Initial complexity** | Complex |
| **Signals used** | File count: 6; domain: WebSocket, rate limiting, real-time; async/concurrency; load tests; reconnection edge cases |

### Tier selection

| Stage | Tier | Agent invoked |
|-------|------|---------------|
| Plan | High | jg-subplanner-high |
| Implement | High | jg-worker-high |
| Test | Standard | jg-tester |
| Review | High | jg-reviewer-high |
| Git | — | jg-git |

### Escalation events

None. Routed to high tier from the start based on complexity.

### Final outcome

- **Tier used**: High
- **Result**: PASS (all stages)
- **Branch**: `feature/notif-003-websocket-delivery`
- **PR**: #103

---

## Summary

| Issue | Initial complexity | Tier used | Escalation | Outcome |
|-------|--------------------|-----------|------------|---------|
| NOTIF-001 | Trivial | Fast | No | PASS |
| NOTIF-002 | Standard | Standard | Yes (fast → standard) | PASS |
| NOTIF-003 | Complex | High | No | PASS |
