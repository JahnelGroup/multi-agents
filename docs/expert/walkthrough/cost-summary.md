# Cost Summary — Notification System Walkthrough

Per-issue cost breakdown using illustrative token counts and costs.

---

## Per-issue breakdown

| Issue | Agents invoked | Total tokens | Est. cost |
|-------|----------------|-------------|-----------|
| NOTIF-001 (trivial/fast) | 4 fast agents | ~8K tokens | ~$0.01 |
| NOTIF-002 (standard, with escalation) | 1 fast + 5 standard agents | ~45K tokens | ~$0.15 |
| NOTIF-003 (complex/high) | 6 agents (3 high, 1 standard, 2 other) | ~120K tokens | ~$0.80 |

---

## Comparison

**If all 3 issues used standard tier (no rework)**: ~$0.45 total.

- NOTIF-001: ~$0.15 (standard instead of fast)
- NOTIF-002: ~$0.15 (unchanged)
- NOTIF-003: ~$0.15 (standard instead of high)

**Standard tier with rework (under-tiering NOTIF-003)**: ~$0.67–0.75 total.

- NOTIF-001: ~$0.15
- NOTIF-002: ~$0.15
- NOTIF-003 on standard: initial run ~$0.15; complex scope often triggers 1–2 retry cycles (debugger + worker re-dispatch, or plan_defect and re-plan). Assume 1.5x–2x extra: ~$0.22–0.30. Total for NOTIF-003: ~$0.37–0.45. **Total for all three**: ~$0.67–0.75, with more cycles and latency than a single high-tier pass.

**With tiered routing**: ~$0.96 total.

- NOTIF-001: ~$0.01 (fast tier)
- NOTIF-002: ~$0.15 (standard, after escalation)
- NOTIF-003: ~$0.80 (high tier)

---

## Analysis

- **NOTIF-003 premium** ($0.80 high vs ~$0.37–0.45 standard with rework): High-tier agents reduce rework cycles and produce more robust designs in one pass. The "standard only" $0.15 figure understates the real cost when a complex task is under-tiered.
- **NOTIF-001 savings** ($0.01 vs $0.15): Demonstrate the fast tier's value for trivial tasks (2 files, types + docs only). No need for heavier models.
- **NOTIF-002 escalation**: Initial fast-tier attempt escalated to standard; the extra cost (~$0.15) reflects appropriate tiering once scope was understood.

*Note: Actual costs depend on model pricing and task complexity. These figures are illustrative.*
