---
name: phase-coverage-validation
description: Validate bidirectional traceability and produce strict pass or fail coverage status.
argument-hint: optional requirement IDs to inspect closely
user-invocable: true
disable-model-invocation: true
context: fork
---

# Phase Coverage Validation Skill

## Inputs
- artifacts/spec.yaml
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/sequences/sequence-definitions.yaml
- artifacts/tests/test-matrix.yaml

## Output Template
- [traceability matrix template](../../../templates/artifacts/traceability-matrix.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-11-coverage-validation.prompt.md).
2. Build forward mapping REQ -> UC -> SEQ -> TEST.
3. Build reverse mapping TEST -> SEQ -> UC -> REQ.
4. List gaps and remediation.

## Gate
Fail on any orphan requirement or broken artifact chain.
