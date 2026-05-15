---
description: Use when producing YAML artifacts for pipeline phases, critique scorecards, ADR logs, and traceability matrices.
applyTo: "**/*.{md,yaml,yml}"
---

# Schema and Format Standards

## Canonical Format
- YAML-first for intermediate artifacts.
- Markdown for final documentation pack.
- Use ASCII only.

## ID Conventions
- Requirement IDs: REQ-001, REQ-002, ...
- Use case IDs: UC-001, UC-002, ...
- Sequence IDs: SEQ-001, SEQ-002, ...
- Test IDs: TEST-UC-001-E2E-001, TEST-REQ-010-SEC-001, ...
- ADR IDs: ADR-001, ADR-002, ...

## Required Metadata
Each generated YAML artifact must include:
- schema_version
- generated_at
- source_phase
- owners or personas

## Validation Rules
- Keep keys stable across phases.
- Do not rename IDs between phases.
- Every reference must point to an existing upstream artifact ID.
- Include explicit null or empty arrays instead of omitting required keys.

## Critique Scorecard Rules
- Must include: strengths, weaknesses, risks, hidden_assumptions, scalability_concerns, security_concerns, implementation_complexity, recommended_changes.
- implementation_complexity range: 1 to 10.
- Recommended changes must include rationale and estimated effort.

## Traceability Rules
- Each requirement must map to one or more use cases.
- Each mapped use case must map to one or more sequences.
- Each mapped sequence must map to one or more test cases.
- Any broken link is a hard-fail condition in coverage validation.
