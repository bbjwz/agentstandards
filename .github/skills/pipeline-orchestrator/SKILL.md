---
name: pipeline-orchestrator
description: Deprecated Copilot-era pipeline retained only as a migration reference; use the Spec Kit Agentstandards skills instead.
argument-hint: path to spec and optional scope notes
user-invocable: false
disable-model-invocation: true
---

# Pipeline Orchestrator Skill

> **Deprecated:** Do not use this as the runtime entrypoint. Install the Spec Kit bundle and invoke
> `$speckit-agentstandards-architect`. The canonical persona registry is
> `runtime/agentstandards/personas.yml`.

This skill documents the former bounded Copilot pipeline.

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
