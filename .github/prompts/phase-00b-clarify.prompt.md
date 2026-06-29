---
description: Run phase_00b_clarify to resolve open questions from spec ingestion before parallel planning begins. Optional but recommended when artifacts/spec.yaml contains open_questions.
---

# Phase 00b: Clarify (Optional)

## Goal
Resolve ambiguities captured as `open_questions` in `artifacts/spec.yaml` before planners receive the specification. Prevents divergent assumptions from propagating into parallel plans.

## When to Run
Run this phase when `artifacts/spec.yaml` contains one or more `open_questions` entries. Skip if the spec has no open questions.

## Required Inputs
- artifacts/spec.yaml (must contain at least one open_questions entry)
- spec/constitution.md (if available, use to constrain resolutions)

## Required Output
- artifacts/clarification-log.yaml using templates/artifacts/clarification-log.yaml

## Procedure
1. Read all `open_questions` from `artifacts/spec.yaml`.
2. For each question, determine its impact on requirements.
3. Classify the question as either:
   - **answerable** — resolve it using constitution.md constraints and available context.
   - **deferrable** — document why it cannot be resolved now and define the trigger that will force resolution later.
4. For answerable questions, produce a resolution and identify which requirement IDs are affected.
5. For requirements affected by a resolution, record spec amendments in `spec_amendments`.
6. Set `clarify_gate.all_critical_resolved: true` only if no priority-critical questions remain unresolved.
7. Set `clarify_gate.ready_for_planning: true` only when all critical open questions are resolved.
8. If blocking questions remain unresolved, hard-fail with a clear description of what information is needed.

## Hard-Fail Conditions
- Critical open question remains unresolved and no deferral reason is documented.
- A resolution contradicts a constraint in spec/constitution.md without a recorded exception.
- `clarify_gate.ready_for_planning` is false when no deferral justification exists.

## Completion Criteria
- All open questions from spec.yaml are accounted for (resolved or deferred with reason).
- `clarify_gate.ready_for_planning: true`.
- All spec amendments are recorded and traceable to question IDs.
- Output conforms to templates/artifacts/clarification-log.yaml schema.
