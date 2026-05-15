---
description: Run phase_07_architecture_validation to enforce readiness gates before downstream generation.
---

# Phase 07: Architecture Validation

## Goal
Validate consensus outputs against specification coverage and blocker status.

## Required Inputs
- artifacts/spec.yaml
- artifacts/consensus/master-plan.yaml
- artifacts/consensus/adr-log.yaml

## Required Output
- artifacts/validation/architecture-validation.yaml using templates/artifacts/validation-report.yaml

## Procedure
1. Map requirements to consensus components.
2. Confirm no blocking unresolved ADRs.
3. Identify partial or missing coverage.
4. Produce explicit go or no-go status.

## Hard-Fail Conditions
- Blocking ADR unresolved.
- Requirement coverage incomplete.
- Validation report missing remediation steps.

## Completion Criteria
Status must be READY to proceed to use-case generation.
