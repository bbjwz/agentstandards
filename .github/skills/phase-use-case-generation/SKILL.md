---
name: phase-use-case-generation
description: Generate structured use-case catalog after architecture is validated, including happy, edge, failure, concurrency, misuse, and rollback scenarios.
argument-hint: optional domain emphasis for actors and scenarios
user-invocable: true
disable-model-invocation: true
---

# Phase Use Case Generation Skill

## Inputs
- artifacts/spec.yaml
- artifacts/consensus/master-plan.yaml
- artifacts/validation/architecture-validation.yaml

## Output Template
- [use case template](../../../templates/artifacts/use-case-catalog.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/generate-use-cases.prompt.md).
2. Generate actor-linked use cases tied to requirement IDs.
3. Include all required scenario classes.
4. Keep acceptance criteria explicit.

## Gate
Fail if critical requirements are not mapped to one or more use cases.
