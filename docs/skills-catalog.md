# Skills Catalog

This catalog maps each skill to its pipeline phase and artifact contracts.

## Orchestration
- Skill: pipeline-orchestrator
- Skill file: .github/skills/pipeline-orchestrator/SKILL.md
- Purpose: run end-to-end deterministic phase flow with strict gates.

## Phase Skills
1. phase-ingest-spec
   - Prompt: .github/prompts/phase-00-ingest-spec.prompt.md
   - Primary template: templates/artifacts/spec.yaml
2. phase-parallel-planning
   - Prompt: .github/prompts/phase-01-parallel-planning.prompt.md
   - Primary template: templates/artifacts/plan.yaml
3. phase-critique-round-1
   - Prompt: .github/prompts/phase-02-critique-round-1.prompt.md
   - Primary template: templates/artifacts/critique-scorecard.yaml
4. phase-plan-revision
   - Prompt: .github/prompts/phase-03-plan-revision.prompt.md
   - Primary template: templates/artifacts/revised-plan.yaml
5. phase-cross-critique
   - Prompt: .github/prompts/phase-04-cross-critique-round.prompt.md
   - Primary template: templates/artifacts/conflict-report.yaml
6. phase-second-critique
   - Prompt: .github/prompts/phase-05-second-critique.prompt.md
   - Primary template: templates/artifacts/critique-scorecard.yaml
7. phase-consensus-synthesis
   - Prompt: .github/prompts/phase-06-consensus-synthesis.prompt.md
   - Primary templates:
     - templates/artifacts/master-plan.yaml
     - templates/artifacts/adr-log.yaml
8. phase-architecture-validation
   - Prompt: .github/prompts/phase-07-architecture-validation.prompt.md
   - Primary template: templates/artifacts/validation-report.yaml
9. phase-use-case-generation
   - Prompt: .github/prompts/phase-08-use-case-generation.prompt.md
   - Primary template: templates/artifacts/use-case-catalog.yaml
10. phase-sequence-generation
    - Prompt: .github/prompts/phase-09-sequence-generation.prompt.md
    - Primary template: templates/artifacts/sequence-definitions.yaml
11. phase-test-generation
    - Prompt: .github/prompts/phase-10-test-scenario-generation.prompt.md
    - Primary template: templates/artifacts/test-matrix.yaml
12. phase-coverage-validation
    - Prompt: .github/prompts/phase-11-coverage-validation.prompt.md
    - Primary template: templates/artifacts/traceability-matrix.yaml
13. phase-documentation-pack
    - Prompt: .github/prompts/phase-12-documentation-pack.prompt.md
    - Primary template: templates/artifacts/documentation-pack.yaml

## Invocation
- Type / in chat to list available skills.
- Use /pipeline-orchestrator to drive the full flow.
- Use individual /phase-* skills for explicit, phase-by-phase control.

## Policy
- Skills are configured for manual deterministic invocation.
- Strict phase order and gate behavior are controlled by .github/agents/AGENTS.md.
