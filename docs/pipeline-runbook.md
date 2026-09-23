# Pipeline Runbook

This runbook defines how to execute the deterministic multi-agent pipeline in every new project.

## 0. Bootstrap: Create Project Constitution (Recommended)
Before the first pipeline run, establish governing principles for the project.
1. Copy `templates/spec/constitution.md` to `spec/constitution.md` in the project.
2. Fill in technology constraints, engineering principles, quality standards, and compliance requirements.
3. The constitution is consumed by phase_00 (spec ingestion) and phase_00b (clarify) to anchor decisions.

## 1. Bootstrap
1. Copy this repository structure into the new project.
2. Create folders in the new project:
   - spec
   - artifacts/plans
   - artifacts/critiques/round-1
   - artifacts/critiques/round-2
   - artifacts/revised-plans
   - artifacts/conflicts
   - artifacts/consensus
   - artifacts/validation
   - artifacts/use-cases
   - artifacts/sequences/diagrams
   - artifacts/tests
3. Place your feature or system specification in spec/raw-spec.md.

## 2. Execute Phases
Use skills as slash commands in strict order:
1. /phase-ingest-spec
2. /phase-clarify  *(optional — run only if spec.yaml has open_questions entries)*
3. /phase-parallel-planning
4. /phase-critique-round-1
5. /phase-plan-revision
6. /phase-cross-critique
7. /phase-second-critique
8. /phase-consensus-synthesis
9. /phase-architecture-validation
10. /phase-use-case-generation
11. /phase-sequence-generation
12. /phase-test-generation
13. /phase-coverage-validation
14. /phase-documentation-pack
15. /phase-converge

Alternative:
- Run /pipeline-orchestrator to execute the same order with guided control.

Prompt compatibility:
- Prompt files in .github/prompts remain available and are aligned to the same phase contracts.

## 3. Strict Fail Conditions
- Missing required input artifact for the active phase.
- Artifact schema mismatch against templates/artifacts.
- Blocking unresolved ADRs during architecture validation.
- Requirement traceability gaps during coverage validation.
- Unresolved critical open questions during clarify gate (phase_00b).
- Critical requirement classified as not_implemented without a documented blocker during converge gate (phase_13).

## 4. Required Test Dimensions
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

## 5. Traceability Target
Coverage must always be complete:
- Requirement -> Use Case -> Sequence -> Test

## 6. Governance
- Keep all rejected alternatives documented.
- Keep unresolved tradeoffs explicit and owned.
- Do not bypass gates unless a documented exception policy exists.

## 7. Production Feedback Loop
When the pipeline terminates and the system is in production:
1. Incidents and recurring error patterns are documented as amendments in spec/raw-spec.md.
2. The convergence report (artifacts/validation/convergence-report.yaml) is reviewed each sprint.
3. If converge_gate.pipeline_rerun_required is true, rerun from /phase-ingest-spec with the convergence report attached as supplementary context.
4. New requirements discovered via production feedback are assigned new REQ-* IDs and processed through the full phase chain.
