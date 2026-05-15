---
description: Run phase_03_plan_revision to produce revised plans from round-1 critique artifacts.
---

# Phase 03: Plan Revision

## Goal
Revise each original plan by consuming structured critique inputs.

## Required Inputs
- artifacts/plans/*.yaml
- artifacts/critiques/round-1/*.yaml

## Required Outputs
- artifacts/revised-plans/*.yaml using templates/artifacts/revised-plan.yaml

## Procedure
1. For each plan, apply or reject critique findings explicitly.
2. Record revision decisions and rationale.
3. Track dimensional score delta before and after revision.

## Hard-Fail Conditions
- Critique findings dropped without disposition.
- Missing revision rationale.
- Revised plans with broken requirement references.

## Completion Criteria
Revised plans include full finding disposition and score deltas.
