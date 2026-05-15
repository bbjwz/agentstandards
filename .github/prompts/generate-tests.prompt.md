---
description: Generate multi-dimensional test scenarios with traceable linkage to requirements, use cases, and sequences.
---

# Phase 10: Test Scenario Generation

## Goal
Generate a comprehensive test matrix across all required dimensions.

## Required Inputs
- artifacts/spec.yaml
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/sequences/sequence-definitions.yaml

## Required Output
- artifacts/tests/test-matrix.yaml using templates/artifacts/test-matrix.yaml

## Procedure
1. Generate tests for each dimension:
   - unit
   - integration
   - contract
   - e2e
   - chaos
   - performance
   - security
   - concurrency
   - recovery
   - migration
2. Link each test to REQ-* and UC-* and SEQ-* IDs.
3. Include setup, steps, assertions, and expected outcome.

## Hard-Fail Conditions
- Missing required test dimensions.
- Tests without traceability links.
- Missing negative and failure-path coverage.

## Completion Criteria
Test matrix is complete and traceable.
