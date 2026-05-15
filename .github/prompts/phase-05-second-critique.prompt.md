---
description: Run phase_05_second_critique using revised plans and conflict report as input.
---

# Phase 05: Second Critique

## Goal
Perform a second structured critique focused on residual risk and unresolved contradictions.

## Required Inputs
- artifacts/revised-plans/*.yaml
- artifacts/conflicts/conflict-report.yaml

## Required Outputs
- artifacts/critiques/round-2/*.yaml using templates/artifacts/critique-scorecard.yaml

## Procedure
1. Re-score revised plans against critique dimensions.
2. Validate whether prior weaknesses were effectively addressed.
3. Highlight unresolved blockers and new risks introduced by revisions.

## Hard-Fail Conditions
- Missing explicit residual-risk assessment.
- Contradictions ignored without a position.
- High-risk items without mitigation recommendations.

## Completion Criteria
Round-2 critique set is complete and ready for synthesis.
