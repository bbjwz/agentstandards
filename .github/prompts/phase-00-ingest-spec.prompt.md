---
description: Run phase_00_spec_ingestion to normalize raw requirements into artifacts/spec.yaml.
---

# Phase 00: Spec Ingestion

## Goal
Convert spec/raw-spec.md into a normalized YAML specification.

## Required Inputs
- spec/raw-spec.md

## Required Output
- artifacts/spec.yaml using templates/artifacts/spec.yaml

## Procedure
1. Parse raw requirements into bounded and testable statements.
2. Assign stable IDs REQ-001 onward.
3. Extract constraints, non-goals, and acceptance criteria.
4. Preserve unresolved ambiguities under open_questions.

## Hard-Fail Conditions
- Missing requirement IDs.
- Acceptance criteria missing for critical requirements.
- Constraints or non-goals omitted.

## Completion Criteria
Output conforms to schema and is ready for parallel planning.
