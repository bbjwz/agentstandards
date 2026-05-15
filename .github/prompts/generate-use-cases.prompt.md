---
description: Generate structured use-case catalog from validated architecture outputs.
---

# Phase 08: Use-Case Generation

## Goal
Generate structured use cases as a separate phase after architecture convergence.

## Required Inputs
- artifacts/spec.yaml
- artifacts/consensus/master-plan.yaml
- artifacts/validation/architecture-validation.yaml (READY)

## Required Output
- artifacts/use-cases/use-case-catalog.yaml using templates/artifacts/use-case-catalog.yaml

## Procedure
1. Generate actors and interaction contexts.
2. Generate happy paths and alternative paths.
3. Generate edge, failure, concurrency, misuse, and rollback scenarios.
4. Assign each use case to one or more requirements.

## Hard-Fail Conditions
- Missing scenario dimensions for critical use cases.
- Use cases not linked to REQ-* IDs.
- Architecture validation is not READY.

## Completion Criteria
Catalog covers full scenario spectrum and requirement linkage.
