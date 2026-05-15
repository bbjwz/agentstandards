# agentstandards

Reusable GitHub Copilot and VS Code components for a deterministic multi-agent architecture pipeline.

This template enforces:
- Structured adversarial review (not open-ended debate)
- Deterministic phase progression
- YAML-first intermediate artifacts
- Strict fail gates on unresolved blockers and traceability gaps
- Full artifact chain coverage: Requirement -> Use Case -> Sequence -> Test

## What Is Implemented

### Orchestration
- `.github/agents/AGENTS.md`
	- canonical phase order
	- required inputs and outputs per phase
	- strict gate conditions

### Reusable Agent Personas
- Planning personas (6):
	- systems architect
	- staff engineer
	- security architect
	- scalability specialist
	- product/ux reviewer
	- reliability engineer
- Critique personas (5):
	- failure-mode reviewer
	- cost optimizer
	- simplicity enforcer
	- enterprise governance reviewer
	- qa/test architect
- Convergence and gatekeeper personas:
	- consensus synthesizer
	- architecture validator

### Prompt Surface
- Full phase prompts from spec ingestion to final documentation pack under `.github/prompts/`
- Dedicated prompts for:
	- use-case generation
	- sequence generation
	- test generation
	- coverage validation

### Skills Surface
- Full phase skills under `.github/skills/` with standards-compliant `SKILL.md` files
- Skills are configured for deterministic manual invocation (`disable-model-invocation: true`)
- Orchestration entrypoint:
	- `pipeline-orchestrator`
- Phase skills:
	- `phase-ingest-spec`
	- `phase-parallel-planning`
	- `phase-critique-round-1`
	- `phase-plan-revision`
	- `phase-cross-critique`
	- `phase-second-critique`
	- `phase-consensus-synthesis`
	- `phase-architecture-validation`
	- `phase-use-case-generation`
	- `phase-sequence-generation`
	- `phase-test-generation`
	- `phase-coverage-validation`
	- `phase-documentation-pack`

### Artifact Contracts
- Canonical YAML templates in `templates/artifacts/`:
	- spec
	- plan
	- critique scorecard
	- revised plan
	- conflict report
	- adr log
	- master plan
	- validation report
	- use-case catalog
	- sequence definitions
	- test matrix
	- traceability matrix
	- documentation pack

### Operational Docs
- `docs/pipeline-runbook.md`
- `docs/adr-template.md`
- `docs/skills-catalog.md`

## Quick Start In A New Project

1. Copy this template structure into the new repository.
2. Create `spec/raw-spec.md`.
3. Open chat customizations and confirm skills are discoverable.
4. Execute either:
	- `/pipeline-orchestrator` for guided end-to-end execution
	- or run each phase skill in strict order:
		1. `/phase-ingest-spec`
		2. `/phase-parallel-planning`
		3. `/phase-critique-round-1`
		4. `/phase-plan-revision`
		5. `/phase-cross-critique`
		6. `/phase-second-critique`
		7. `/phase-consensus-synthesis`
		8. `/phase-architecture-validation`
		9. `/phase-use-case-generation`
		10. `/phase-sequence-generation`
		11. `/phase-test-generation`
		12. `/phase-coverage-validation`
		13. `/phase-documentation-pack`
5. Prompt files remain available as compatibility wrappers for the same phases.

## Strict Fail Policy

Pipeline progression stops when any of the following occur:
- missing required phase input artifacts
- schema mismatch against `templates/artifacts/*.yaml`
- unresolved blocking ADRs
- traceability gaps in Requirement -> Use Case -> Sequence -> Test

## Notes

- This implementation is Copilot and VS Code customization only, with no external orchestration runner.
- Skills are portable and can be reused across projects by copying `.github/skills/`.
- Context7 MCP integration is intentionally deferred to a follow-up increment.
- Each generated use case must map to a test plan and to the process flow represented by sequence definitions.