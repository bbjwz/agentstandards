---
name: phase-converge
description: Validate codebase alignment against the spec and documentation pack. Identify implementation gaps, test coverage gaps, documentation drift, and deferred work. Run after /phase-documentation-pack.
argument-hint: optional codebase snapshot path or branch name
user-invocable: true
disable-model-invocation: true
---

# Phase Converge Skill

This skill closes the feedback loop by comparing the actual codebase state against all pipeline artifacts. It is the final phase of the pipeline.

## Inputs
- artifacts/spec.yaml
- artifacts/validation/traceability-matrix.yaml
- artifacts/tests/test-matrix.yaml
- docs/final-documentation-pack.md
- Current codebase state

## Output
- [convergence-report template](../../../templates/artifacts/convergence-report.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-13-converge.prompt.md).
2. Assess implementation status of every requirement.
3. Check test matrix coverage against actual test files.
4. Document documentation drift.
5. Enumerate deferred items and production feedback inputs.
6. Set converge gate fields.

## Gate
Fail if any critical requirement is not implemented without a documented blocker and escalation path.

## Feedback Loop
If `converge_gate.pipeline_rerun_required: true`, amend `spec/raw-spec.md` with the critical gaps and rerun from `/phase-ingest-spec`, attaching the convergence report as context.
