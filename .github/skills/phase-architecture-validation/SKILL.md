---
name: phase-architecture-validation
description: Validate consensus architecture readiness and enforce strict go or no-go before downstream generation.
argument-hint: optional strictness notes for blocker handling
user-invocable: true
disable-model-invocation: true
context: fork
---

# Phase Architecture Validation Skill

## Inputs
- artifacts/spec.yaml
- artifacts/consensus/master-plan.yaml
- artifacts/consensus/adr-log.yaml

## Output Template
- [validation report template](../../../templates/artifacts/validation-report.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-07-architecture-validation.prompt.md).
2. Check requirement coverage against consensus design.
3. Detect unresolved blocking ADR entries.
4. Emit READY or NOT_READY with remediation actions.

## Gate
Fail if any blocking ADR remains unresolved or any requirement is uncovered.
