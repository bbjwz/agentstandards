# Pipeline Runbook

This runbook defines how to execute the deterministic multi-agent pipeline in every new project.

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
2. /phase-parallel-planning
3. /phase-critique-round-1
4. /phase-plan-revision
5. /phase-cross-critique
6. /phase-second-critique
7. /phase-consensus-synthesis
8. /phase-architecture-validation
9. /phase-use-case-generation
10. /phase-sequence-generation
11. /phase-test-generation
12. /phase-coverage-validation
13. /phase-documentation-pack

Alternative:
- Run /pipeline-orchestrator to execute the same order with guided control.

Prompt compatibility:
- Prompt files in .github/prompts remain available and are aligned to the same phase contracts.

## 3. Strict Fail Conditions
- Missing required input artifact for the active phase.
- Artifact schema mismatch against templates/artifacts.
- Blocking unresolved ADRs during architecture validation.
- Requirement traceability gaps during coverage validation.

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
