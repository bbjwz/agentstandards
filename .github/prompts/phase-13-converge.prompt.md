---
description: Run phase_13_converge to assess codebase alignment against the spec and documentation pack, identify gaps, and produce a convergence report for iterative improvement.
---

# Phase 13: Converge

## Goal
Validate that the actual codebase and documentation reflect the specification, traceability matrix, and test matrix produced by the pipeline. Identify implementation gaps, documentation drift, and deferred work items. Enable a closed-loop feedback cycle.

## Required Inputs
- artifacts/spec.yaml
- artifacts/validation/traceability-matrix.yaml
- artifacts/tests/test-matrix.yaml
- docs/final-documentation-pack.md
- Current codebase state (working tree or specified snapshot)

## Optional Inputs
- spec/constitution.md (to check principle adherence)

## Required Output
- artifacts/validation/convergence-report.yaml using templates/artifacts/convergence-report.yaml

## Procedure
1. Load the traceability matrix and identify every requirement with its linked use cases, sequences, and tests.
2. For each requirement, determine its implementation status in the codebase:
   - **fully_implemented** — all acceptance criteria demonstrably satisfied.
   - **partially_implemented** — some criteria satisfied; document percentage and gaps.
   - **not_implemented** — no evidence in codebase; document blocker.
3. For each test in the test matrix, confirm whether a corresponding test file exists. Record missing tests as test coverage gaps.
4. Compare documentation-pack content against codebase reality. Note any sections that are outdated or inaccurate as documentation drift.
5. List all items that were explicitly deferred during the pipeline (from ADR log and critique deferred findings) and confirm their current status.
6. Record any production feedback inputs (incidents, metrics) that should inform the next spec revision.
7. Set `converge_gate.pipeline_rerun_required: true` if any critical requirements are not implemented or if unresolved blocking items exist.

## Hard-Fail Conditions
- Traceability matrix is missing or does not conform to schema.
- Final documentation pack does not exist.
- Any critical requirement (`priority: critical`) is classified as `not_implemented` without a documented blocker and escalation path.

## Completion Criteria
- All requirements accounted for (fully_implemented, partially_implemented, or not_implemented with blocker).
- All test-matrix items checked against codebase.
- Documentation drift documented.
- Deferred work items enumerated with priorities.
- `converge_gate` fields accurately reflect the pipeline state.
- Output conforms to templates/artifacts/convergence-report.yaml schema.

## Feedback Loop
If `converge_gate.pipeline_rerun_required: true`, create a new spec amendment in `spec/raw-spec.md` addressing the critical gaps and rerun the pipeline from phase_00_spec_ingestion, using the convergence report as supplementary context.
