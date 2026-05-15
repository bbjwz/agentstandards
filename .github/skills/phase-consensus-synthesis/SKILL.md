---
name: phase-consensus-synthesis
description: Merge strongest revised plan elements into a master plan and ADR log with explicit accepted, rejected, and unresolved decisions.
argument-hint: optional tie-break preference notes
user-invocable: true
disable-model-invocation: true
---

# Phase Consensus Synthesis Skill

## Inputs
- artifacts/revised-plans/*.yaml
- artifacts/critiques/round-2/*.yaml
- artifacts/conflicts/conflict-report.yaml

## Output Templates
- [master plan template](../../../templates/artifacts/master-plan.yaml)
- [adr log template](../../../templates/artifacts/adr-log.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-06-consensus-synthesis.prompt.md).
2. Merge strongest compatible decisions.
3. Record rejected alternatives and rationale.
4. Assign owners and next actions for unresolved tradeoffs.

## Gate
Fail if accepted, rejected, and unresolved decision sets are incomplete.
