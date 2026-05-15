---
description: Run phase_06_consensus_synthesis to produce master plan and ADR log from revised plans and critique outputs.
---

# Phase 06: Consensus Synthesis

## Goal
Converge on a single master plan while preserving decision auditability.

## Required Inputs
- artifacts/revised-plans/*.yaml
- artifacts/critiques/round-2/*.yaml
- artifacts/conflicts/conflict-report.yaml

## Required Outputs
- artifacts/consensus/master-plan.yaml
- artifacts/consensus/adr-log.yaml

## Procedure
1. Merge strongest compatible plan elements.
2. Resolve conflicts explicitly with rationale.
3. Track accepted, rejected, and unresolved decisions.
4. Record each decision in ADR format.

## Hard-Fail Conditions
- Missing rejected alternatives.
- Missing unresolved tradeoff ownership.
- Conflicts resolved without rationale.

## Completion Criteria
Master plan and ADR log are complete and internally consistent.
