---
description: Deterministic multi-agent orchestration registry for planning, critique, convergence, validation, and artifact generation.
---

# Deterministic Pipeline Registry

This file is the source of truth for phase ordering, role boundaries, and gate behavior.

## Operating Model
- Objective: Structured adversarial review with deterministic convergence.
- Loop policy: No unbounded debates. Maximum two critique loops.
- Stop policy: Hard-fail on missing required artifacts, schema violations, or unresolved blocking decisions.
- Format policy: YAML-first intermediate artifacts, markdown for final human-readable packs.
- Bootstrap prerequisite: spec/constitution.md should be created before first pipeline run using templates/spec/constitution.md. It is consumed by phase_00 and phase_00b.

## Canonical Phase Order
1. phase_00_spec_ingestion
2. phase_00b_clarify (OPTIONAL — run when spec.yaml contains open_questions)
3. phase_01_parallel_planning
4. phase_02_critique_round_1
5. phase_03_plan_revision
6. phase_04_cross_critique_round
7. phase_05_second_critique
8. phase_06_consensus_synthesis
9. phase_07_architecture_validation
10. phase_08_use_case_generation
11. phase_09_sequence_generation
12. phase_10_test_scenario_generation
13. phase_11_coverage_validation
14. phase_12_documentation_pack
15. phase_13_converge

## Skill Command Mapping
- /phase-ingest-spec -> phase_00_spec_ingestion
- /phase-clarify -> phase_00b_clarify (optional)
- /phase-parallel-planning -> phase_01_parallel_planning
- /phase-critique-round-1 -> phase_02_critique_round_1
- /phase-plan-revision -> phase_03_plan_revision
- /phase-cross-critique -> phase_04_cross_critique_round
- /phase-second-critique -> phase_05_second_critique
- /phase-consensus-synthesis -> phase_06_consensus_synthesis
- /phase-architecture-validation -> phase_07_architecture_validation
- /phase-use-case-generation -> phase_08_use_case_generation
- /phase-sequence-generation -> phase_09_sequence_generation
- /phase-test-generation -> phase_10_test_scenario_generation
- /phase-coverage-validation -> phase_11_coverage_validation
- /phase-documentation-pack -> phase_12_documentation_pack
- /phase-converge -> phase_13_converge
- /pipeline-orchestrator -> executes the full ordered mapping above

## Phase Contracts

### phase_00_spec_ingestion
- Required input:
  - spec/raw-spec.md
- Optional input:
  - spec/constitution.md (if present, apply its constraints during normalization)
- Required output:
  - artifacts/spec.yaml
- Gate:
  - Must include requirement IDs, constraints, non-goals, and acceptance criteria.

### phase_00b_clarify (OPTIONAL)
- Trigger condition:
  - artifacts/spec.yaml contains one or more open_questions entries
- Required input:
  - artifacts/spec.yaml
- Optional input:
  - spec/constitution.md
- Required output:
  - artifacts/clarification-log.yaml
- Gate:
  - All critical open questions must be resolved or deferred with documented reason.
  - clarify_gate.ready_for_planning must be true before proceeding to phase_01.

### phase_01_parallel_planning
- Required input:
  - artifacts/spec.yaml
- Required output:
  - artifacts/plans/plan-systems-architect.yaml
  - artifacts/plans/plan-staff-engineer.yaml
  - artifacts/plans/plan-security-architect.yaml
  - artifacts/plans/plan-scalability-specialist.yaml
  - artifacts/plans/plan-product-ux-reviewer.yaml
  - artifacts/plans/plan-reliability-engineer.yaml
- Gate:
  - All planner artifacts must conform to the plan schema and use identical requirement IDs from spec.

### phase_02_critique_round_1
- Required input:
  - artifacts/plans/*.yaml
- Required output:
  - artifacts/critiques/round-1/*.yaml
- Gate:
  - Each critique must use the scorecard schema and include dimensional scoring.

### phase_03_plan_revision
- Required input:
  - artifacts/plans/*.yaml
  - artifacts/critiques/round-1/*.yaml
- Required output:
  - artifacts/revised-plans/*.yaml
- Gate:
  - Every critique finding must be marked as incorporated, rejected_with_reason, or deferred.

### phase_04_cross_critique_round
- Required input:
  - artifacts/revised-plans/*.yaml
- Required output:
  - artifacts/conflicts/conflict-report.yaml
- Gate:
  - Contradictions must be classified and linked to impacted plans.

### phase_05_second_critique
- Required input:
  - artifacts/revised-plans/*.yaml
  - artifacts/conflicts/conflict-report.yaml
- Required output:
  - artifacts/critiques/round-2/*.yaml
- Gate:
  - Must explicitly evaluate unresolved risks and residual complexity.

### phase_06_consensus_synthesis
- Required input:
  - artifacts/revised-plans/*.yaml
  - artifacts/critiques/round-2/*.yaml
  - artifacts/conflicts/conflict-report.yaml
- Required output:
  - artifacts/consensus/master-plan.yaml
  - artifacts/consensus/adr-log.yaml
- Gate:
  - Consensus must include accepted decisions, rejected decisions, unresolved tradeoffs.

### phase_07_architecture_validation
- Required input:
  - artifacts/spec.yaml
  - artifacts/consensus/master-plan.yaml
  - artifacts/consensus/adr-log.yaml
- Required output:
  - artifacts/validation/architecture-validation.yaml
- Gate:
  - Must be READY before downstream generation. Missing coverage or blocking ADRs is fail.

### phase_08_use_case_generation
- Required input:
  - artifacts/spec.yaml
  - artifacts/consensus/master-plan.yaml
- Required output:
  - artifacts/use-cases/use-case-catalog.yaml
- Gate:
  - Must include happy, edge, failure, concurrency, misuse, and rollback scenarios.

### phase_09_sequence_generation
- Required input:
  - artifacts/use-cases/use-case-catalog.yaml
  - artifacts/consensus/master-plan.yaml
- Required output:
  - artifacts/sequences/sequence-definitions.yaml
  - artifacts/sequences/diagrams/*.mmd
- Gate:
  - Each critical use case must have a structured sequence definition and Mermaid output.

### phase_10_test_scenario_generation
- Required input:
  - artifacts/spec.yaml
  - artifacts/use-cases/use-case-catalog.yaml
  - artifacts/sequences/sequence-definitions.yaml
- Required output:
  - artifacts/tests/test-matrix.yaml
- Gate:
  - Must cover unit, integration, contract, e2e, chaos, performance, security, concurrency, recovery, migration.

### phase_11_coverage_validation
- Required input:
  - artifacts/spec.yaml
  - artifacts/use-cases/use-case-catalog.yaml
  - artifacts/sequences/sequence-definitions.yaml
  - artifacts/tests/test-matrix.yaml
- Required output:
  - artifacts/validation/traceability-matrix.yaml
- Gate:
  - Requirement -> Use Case -> Sequence -> Test links must be complete. Gaps are fail.

### phase_12_documentation_pack
- Required input:
  - artifacts/consensus/master-plan.yaml
  - artifacts/consensus/adr-log.yaml
  - artifacts/use-cases/use-case-catalog.yaml
  - artifacts/sequences/sequence-definitions.yaml
  - artifacts/tests/test-matrix.yaml
  - artifacts/validation/traceability-matrix.yaml
- Required output:
  - docs/final-documentation-pack.md
- Gate:
  - Must include version stamp and linked artifact index.

### phase_13_converge
- Required input:
  - artifacts/spec.yaml
  - artifacts/validation/traceability-matrix.yaml
  - artifacts/tests/test-matrix.yaml
  - docs/final-documentation-pack.md
- Optional input:
  - spec/constitution.md
- Required output:
  - artifacts/validation/convergence-report.yaml
- Gate:
  - All requirements must be accounted for (fully_implemented, partially_implemented, or not_implemented with documented blocker).
  - Critical requirements with not_implemented status and no blocker are a hard fail.
  - If converge_gate.pipeline_rerun_required is true, record the spec amendment path and halt.

## Role Registry

### Planning Agents
- systems-architect
- staff-engineer
- security-architect
- scalability-specialist
- product-ux-reviewer
- reliability-engineer

### Critique Agents
- failure-mode-reviewer
- cost-optimizer
- simplicity-enforcer
- enterprise-governance-reviewer
- qa-test-architect

### Convergence and Validation Agents
- consensus-synthesizer
- architecture-validator

## Hard Constraints
- Do not skip phases.
- Do not invent missing artifacts.
- Do not continue after a failed gate.
- Do not merge contradictory decisions without an ADR entry.
- Keep outputs concise, schema-bound, and auditable.
