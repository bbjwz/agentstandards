---
name: phase-parallel-planning
description: Run six planning personas in parallel from the normalized spec and generate plan artifacts with consistent requirement IDs.
argument-hint: optional focus area like security or scaling
user-invocable: true
disable-model-invocation: true
---

# Phase Parallel Planning Skill

## Inputs
- artifacts/spec.yaml

## Output Template
- [plan template](../../../templates/artifacts/plan.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-01-parallel-planning.prompt.md).
2. Use planning personas defined in [agents registry](../../agents/AGENTS.md).
3. Produce one plan artifact per planning persona.
4. Keep requirement IDs aligned with artifacts/spec.yaml.

## Gate
Fail if any required planning persona output is missing or non-conformant.
