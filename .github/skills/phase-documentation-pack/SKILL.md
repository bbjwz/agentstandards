---
name: phase-documentation-pack
description: Produce final documentation pack with artifact index, decisions, and traceability summary.
argument-hint: optional audience and output style notes
user-invocable: true
disable-model-invocation: true
---

# Phase Documentation Pack Skill

## Inputs
- artifacts/consensus/master-plan.yaml
- artifacts/consensus/adr-log.yaml
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/sequences/sequence-definitions.yaml
- artifacts/tests/test-matrix.yaml
- artifacts/validation/traceability-matrix.yaml

## Output Template
- [documentation pack template](../../../templates/artifacts/documentation-pack.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-12-documentation-pack.prompt.md).
2. Summarize accepted, rejected, and unresolved decisions.
3. Include artifact links and version metadata.
4. Include traceability status and residual risks.

## Gate
Fail if any required artifact section is missing in the final pack.
