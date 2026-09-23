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
2. /phase-clarify (optional — only if spec.yaml contains open_questions)
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

## Hard Requirements
- Stop immediately on any gate failure.
- Do not skip phases.
- Do not invent missing upstream artifacts.
- Ensure Requirement -> Use Case -> Sequence -> Test links are complete before finalizing.
