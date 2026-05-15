---
description: Run phase_04_cross_critique_round to detect contradictions and produce a conflict report.
---

# Phase 04: Cross Critique Round

## Goal
Detect and classify contradictions across revised plans.

## Required Inputs
- artifacts/revised-plans/*.yaml

## Required Output
- artifacts/conflicts/conflict-report.yaml using templates/artifacts/conflict-report.yaml

## Procedure
1. Compare revised plans pairwise on major decision dimensions.
2. Classify contradiction type and severity.
3. Propose explicit resolution options with tradeoffs.

## Hard-Fail Conditions
- Conflicts listed without severity.
- Conflicts not linked to impacted plans.
- No resolution option for critical contradictions.

## Completion Criteria
Conflict report is complete and ready for second critique.
