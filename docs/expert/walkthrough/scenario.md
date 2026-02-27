# Build a Notification System

## Overview

Build a notification system with API contract, service implementation, and real-time delivery.

## Issues (ordered)

| Order | Issue ID | Title | Complexity | Tier | Depends on |
|-------|----------|-------|------------|------|------------|
| 1 | NOTIF-001 | Define notification API contract | Trivial | Fast | -- |
| 2 | NOTIF-002 | Implement notification service | Standard | Standard (with escalation from fast) | NOTIF-001 |
| 3 | NOTIF-003 | Add real-time WebSocket delivery with rate limiting | Complex | High | NOTIF-002 |

## Acceptance Criteria

### NOTIF-001: Define notification API contract

- TypeScript interfaces defined
- API doc created

### NOTIF-002: Implement notification service

- Service creates/reads notifications
- Unit tests pass
- Integration with existing user service

### NOTIF-003: Add real-time WebSocket delivery with rate limiting

- WebSocket pushes notifications in real-time
- Rate limiter caps at 100/min per user
- Tests cover normal flow, rate limit, and reconnection
