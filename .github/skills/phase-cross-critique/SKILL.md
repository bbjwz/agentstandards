---
name: phase-cross-critique
description: Detect and classify contradictions across revised plans and produce a structured conflict report.
argument-hint: optional contradiction dimension such as data model or scaling
user-invocable: true
disable-model-invocation: true
---

# Phase Cross Critique Skill

## Inputs
- artifacts/revised-plans/*.yaml

## Output Template
- [conflict report template](../../../templates/artifacts/conflict-report.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-04-cross-critique-round.prompt.md).
2. Compare revised plans pairwise across architecture dimensions.
3. Classify conflict type and severity.
4. Propose explicit resolution options with tradeoffs.

## Gate
Fail if critical contradictions are missing resolution options.
