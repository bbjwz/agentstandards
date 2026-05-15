---
description: Run phase_02_critique_round_1 using structured scorecards for all planner outputs.
---

# Phase 02: Critique Round 1

## Goal
Perform structured adversarial critique of all planner artifacts.

## Required Inputs
- artifacts/plans/*.yaml

## Required Outputs
- artifacts/critiques/round-1/*.yaml using templates/artifacts/critique-scorecard.yaml

## Procedure
1. Evaluate each plan with critique personas.
2. Use scorecard dimensions and calibrated scoring.
3. Capture strengths, weaknesses, risks, hidden assumptions.
4. Capture recommended changes with effort and rationale.

## Hard-Fail Conditions
- Freeform critique without scorecard structure.
- Missing dimensional scores.
- Missing recommended changes for high-severity findings.

## Completion Criteria
All plans have at least one complete scorecard from each critique role.
