---
name: phase-sequence-generation
description: Generate structured sequence definitions and Mermaid diagrams from the use-case catalog.
argument-hint: optional subset of use case IDs
user-invocable: true
disable-model-invocation: true
---

# Phase Sequence Generation Skill

## Inputs
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/consensus/master-plan.yaml

## Output Template
- [sequence template](../../../templates/artifacts/sequence-definitions.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/generate-sequences.prompt.md).
2. Define participants and ordered interactions.
3. Include timeout and error behavior.
4. Render Mermaid files per critical use case.

## Gate
Fail if critical use cases lack either structured sequence definition or Mermaid output.
