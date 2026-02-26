# Exercise 03: Escalation Patterns

## Objective

Demonstrate the escalation flow by starting NOTIF-002 at the wrong tier (fast) and handling the escalation to standard.

## Required Reading

- [Expert README](../../README.md) -- "Routing and escalation" section
- [Expert walkthrough routing log](../../walkthrough/routing-log.md) -- NOTIF-002 escalation event

## Context

NOTIF-002 (notification service) was initially misclassified as trivial. The fast-tier worker recognizes it exceeds scope and requests escalation.

## Tasks

1. Create `sandbox/.pipeline/NOTIF-002-escalation/`

2. **Delegate to `jg-worker-fast`** with the NOTIF-002 scope (4 files, cross-service integration). The worker should recognize this exceeds fast tier and return `status: "escalate"` with `tier_used: "fast"`.

3. Read the escalation result. As the planner, decide to upgrade to standard tier.

4. **Delegate to `jg-subplanner`**: write `plan.json` for NOTIF-002.

5. **Delegate to `jg-worker`** (standard): implement the feature. Write `worker-result.json` with:
   ```json
   {
     "status": "completed",
     "tier_used": "standard",
     "escalation_history": [
       {
         "from_tier": "fast",
         "to_tier": "standard",
         "reason": "Multi-file change with cross-service integration exceeds fast scope"
       }
     ]
   }
   ```

## Validation

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 03
```

Checks: worker-result.json exists, has escalation_history, from_tier is "fast", to_tier is "standard".

## Reflection

- What signals told the fast-tier worker to escalate?
- How should the planner log escalation events for cost tracking?
- What's the cost of a misclassification vs the cost of always using the highest tier?
