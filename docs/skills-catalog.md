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
2. phase-clarify *(optional — run when spec.yaml has open_questions)*
   - Prompt: .github/prompts/phase-00b-clarify.prompt.md
   - Primary template: templates/artifacts/clarification-log.yaml
3. phase-parallel-planning
   - Prompt: .github/prompts/phase-01-parallel-planning.prompt.md
   - Primary template: templates/artifacts/plan.yaml
4. phase-critique-round-1
   - Prompt: .github/prompts/phase-02-critique-round-1.prompt.md
   - Primary template: templates/artifacts/critique-scorecard.yaml
5. phase-plan-revision
   - Prompt: .github/prompts/phase-03-plan-revision.prompt.md
   - Primary template: templates/artifacts/revised-plan.yaml
6. phase-cross-critique
   - Prompt: .github/prompts/phase-04-cross-critique-round.prompt.md
   - Primary template: templates/artifacts/conflict-report.yaml
7. phase-second-critique
   - Prompt: .github/prompts/phase-05-second-critique.prompt.md
   - Primary template: templates/artifacts/critique-scorecard.yaml
8. phase-consensus-synthesis
   - Prompt: .github/prompts/phase-06-consensus-synthesis.prompt.md
   - Primary templates:
     - templates/artifacts/master-plan.yaml
     - templates/artifacts/adr-log.yaml
9. phase-architecture-validation
   - Prompt: .github/prompts/phase-07-architecture-validation.prompt.md
   - Primary template: templates/artifacts/validation-report.yaml
10. phase-use-case-generation
    - Prompt: .github/prompts/phase-08-use-case-generation.prompt.md
    - Primary template: templates/artifacts/use-case-catalog.yaml
11. phase-sequence-generation
    - Prompt: .github/prompts/phase-09-sequence-generation.prompt.md
    - Primary template: templates/artifacts/sequence-definitions.yaml
12. phase-test-generation
    - Prompt: .github/prompts/phase-10-test-scenario-generation.prompt.md
    - Primary template: templates/artifacts/test-matrix.yaml
13. phase-coverage-validation
    - Prompt: .github/prompts/phase-11-coverage-validation.prompt.md
    - Primary template: templates/artifacts/traceability-matrix.yaml
14. phase-documentation-pack
    - Prompt: .github/prompts/phase-12-documentation-pack.prompt.md
    - Primary template: templates/artifacts/documentation-pack.yaml
15. phase-converge
    - Prompt: .github/prompts/phase-13-converge.prompt.md
    - Primary template: templates/artifacts/convergence-report.yaml

## Invocation
- Type / in chat to list available skills.
- Use /pipeline-orchestrator to drive the full flow.
- Use individual /phase-* skills for explicit, phase-by-phase control.
- Use /phase-clarify after /phase-ingest-spec when open questions require resolution.
- Use /phase-converge after /phase-documentation-pack to close the feedback loop.

## Policy
- Skills are configured for manual deterministic invocation.
- Strict phase order and gate behavior are controlled by .github/agents/AGENTS.md.
- phase-clarify is optional; all other phases are mandatory.
