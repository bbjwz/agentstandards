---
name: phase-second-critique
description: Run second critique cycle focused on residual risk, unresolved conflicts, and remaining complexity.
argument-hint: optional priority area to challenge
user-invocable: true
disable-model-invocation: true
---

# Phase Second Critique Skill

## Inputs
- artifacts/revised-plans/*.yaml
- artifacts/conflicts/conflict-report.yaml

## Output Template
- [critique scorecard template](../../../templates/artifacts/critique-scorecard.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-05-second-critique.prompt.md).
2. Re-assess risk posture after revisions.
3. Validate that prior high-severity findings were addressed.
4. Flag residual blockers explicitly.

## Gate
Fail if residual high-severity risks have no mitigation recommendations.
