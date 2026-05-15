---
description: Validate end-to-end Requirement to Use Case to Sequence to Test coverage and generate traceability matrix.
---

# Phase 11: Coverage Validation

## Goal
Create a strict traceability matrix and fail on any artifact-chain gap.

## Required Inputs
- artifacts/spec.yaml
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/sequences/sequence-definitions.yaml
- artifacts/tests/test-matrix.yaml

## Required Output
- artifacts/validation/traceability-matrix.yaml using templates/artifacts/traceability-matrix.yaml

## Procedure
1. Build forward mapping: REQ -> UC -> SEQ -> TEST.
2. Build reverse mapping: TEST -> SEQ -> UC -> REQ.
3. Mark coverage status and list gaps.
4. Return pass only when no orphan requirement exists.

## Hard-Fail Conditions
- Any requirement missing use-case linkage.
- Any linked use case missing sequence linkage.
- Any linked sequence missing test linkage.

## Completion Criteria
Matrix has zero critical gaps and explicit status per requirement.
