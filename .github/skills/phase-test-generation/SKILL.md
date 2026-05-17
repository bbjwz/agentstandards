---
name: phase-test-generation
description: Generate complete multi-dimensional test scenarios linked to requirements, use cases, and sequences.
argument-hint: optional risk-based prioritization notes
user-invocable: true
disable-model-invocation: true
---

# Phase Test Generation Skill

## Inputs
- artifacts/spec.yaml
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/sequences/sequence-definitions.yaml

## Output Template
- [test matrix template](../../../templates/artifacts/test-matrix.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-10-test-scenario-generation.prompt.md).
2. Generate tests across required dimensions.
3. Include setup, steps, assertions, and expected outcomes.
4. Link each test to REQ, UC, and SEQ IDs.

## Gate
Fail if any required test dimension is missing or unlinked.
