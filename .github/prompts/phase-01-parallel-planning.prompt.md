---
description: Run phase_01_parallel_planning across six planning personas with identical input spec.
---

# Phase 01: Parallel Planning

## Goal
Generate six independent plan artifacts from the same normalized specification.

## Required Inputs
- artifacts/spec.yaml

## Required Outputs
- artifacts/plans/plan-systems-architect.yaml
- artifacts/plans/plan-staff-engineer.yaml
- artifacts/plans/plan-security-architect.yaml
- artifacts/plans/plan-scalability-specialist.yaml
- artifacts/plans/plan-product-ux-reviewer.yaml
- artifacts/plans/plan-reliability-engineer.yaml

## Procedure
1. Invoke each planner role once.
2. Enforce identical requirement ID set across all plans.
3. Ensure each plan follows templates/artifacts/plan.yaml.
4. Collect all outputs before critique starts.

## Hard-Fail Conditions
- Missing any planner artifact.
- Planner artifact deviates from required schema.
- Requirement IDs are inconsistent with artifacts/spec.yaml.

## Completion Criteria
All six plans exist and pass schema checks.
