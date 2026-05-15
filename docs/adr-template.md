# ADR Template

Use this lightweight template for every decision produced during consensus synthesis.

```yaml
adr_id: ADR-001
title: Choose Event-Driven Payment Orchestration
status: accepted
context: |
  Competing plans proposed direct synchronous calls vs event-driven orchestration.
options:
  - option_id: OPT-A
    name: Synchronous orchestration
    pros:
      - Lower initial implementation complexity
    cons:
      - Tighter coupling under peak load
    source_plan_ids:
      - PLAN-STAFF-001
  - option_id: OPT-B
    name: Event-driven orchestration
    pros:
      - Better resilience and throughput control
    cons:
      - Requires stronger observability and replay controls
    source_plan_ids:
      - PLAN-SCALE-001
      - PLAN-REL-001
decision: OPT-B
accepted_decision: Use event-driven orchestration with idempotent consumers.
rejected_decisions:
  - option_id: OPT-A
    reason: Coupling risk and degraded failure isolation under burst traffic.
unresolved_tradeoffs:
  - message ordering guarantees across regions
consequences:
  - Introduces queue management and replay tooling requirements.
revisit_trigger: Reassess if p95 latency exceeds 300ms at target load.
owner: consensus-synthesizer
related_requirements:
  - REQ-003
  - REQ-017
related_use_cases:
  - UC-004
  - UC-012
related_tests:
  - TEST-UC-004-PERF-001
```
