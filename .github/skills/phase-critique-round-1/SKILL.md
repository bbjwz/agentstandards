---
name: phase-critique-round-1
description: Perform first structured adversarial critique using scorecards across all planning artifacts.
argument-hint: optional emphasis such as reliability or governance
user-invocable: true
disable-model-invocation: true
---

# Phase Critique Round 1 Skill

## Inputs
- artifacts/plans/*.yaml

## Output Template
- [critique scorecard template](../../../templates/artifacts/critique-scorecard.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-02-critique-round-1.prompt.md).
2. Apply critique personas from [agents registry](../../agents/AGENTS.md).
3. Score each plan with strengths, weaknesses, and risks.
4. Include recommended changes with rationale and effort.

## Gate
Fail if scorecards are missing required sections or dimensional scores.
