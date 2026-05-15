---
name: pipeline-orchestrator
description: Run the full deterministic multi-agent architecture pipeline from spec ingestion to documentation pack. Use when starting or reviewing a project with strict phase gates.
argument-hint: path to spec and optional scope notes
user-invocable: true
disable-model-invocation: true
---

# Pipeline Orchestrator Skill

Use this skill to execute the complete pipeline with bounded rounds and strict fail gates.

## Required References
- Phase registry: [AGENTS](../../agents/AGENTS.md)
- Runbook: [Pipeline Runbook](../../../docs/pipeline-runbook.md)
- Core behavior rules: [Pipeline Core Rules](../../instructions/pipeline-core.instructions.md)
- Schema rules: [Schema Standards](../../instructions/schema-standards.instructions.md)

## Execution Order
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

## Hard Requirements
- Stop immediately on any gate failure.
- Do not skip phases.
- Do not invent missing upstream artifacts.
- Ensure Requirement -> Use Case -> Sequence -> Test links are complete before finalizing.
