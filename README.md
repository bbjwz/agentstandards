# agentstandards

Reusable GitHub Copilot and VS Code components for a deterministic multi-agent architecture pipeline.

This template enforces:
- Structured adversarial review (not open-ended debate)
- Deterministic phase progression
- YAML-first intermediate artifacts
- Strict fail gates on unresolved blockers and traceability gaps
- Full artifact chain coverage: Requirement -> Use Case -> Sequence -> Test
- Closed-loop feedback via a post-implementation convergence phase

## What Is Implemented

### Orchestration
- `.github/agents/AGENTS.md`
	- canonical phase order
	- required inputs and outputs per phase
	- strict gate conditions
	- bootstrap constitution prerequisite

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
- Full phase prompts from spec ingestion to convergence under `.github/prompts/`
- Prompt filenames are phase-prefixed for deterministic ordering (`phase-00` through `phase-13`)
- Dedicated prompts for:
	- ambiguity resolution (`phase-00b-clarify.prompt.md`) — optional
	- use-case generation (`phase-08-use-case-generation.prompt.md`)
	- sequence generation (`phase-09-sequence-generation.prompt.md`)
	- test generation (`phase-10-test-scenario-generation.prompt.md`)
	- coverage validation (`phase-11-coverage-validation.prompt.md`)
	- convergence (`phase-13-converge.prompt.md`)

### Skills Surface
- Full phase skills under `.github/skills/` with standards-compliant `SKILL.md` files
- Skills are configured for deterministic manual invocation (`disable-model-invocation: true`)
- Orchestration entrypoint:
	- `pipeline-orchestrator`
- Phase skills:
	- `phase-ingest-spec`
	- `phase-clarify` *(optional)*
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
	- `phase-converge`

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
	- clarification log *(new)*
	- convergence report *(new)*
	- constitution *(new)*
- Bootstrap templates in `templates/spec/`:
	- `constitution.md` — project governing principles template

### Operational Docs
- `docs/pipeline-runbook.md`
- `docs/adr-template.md`
- `docs/skills-catalog.md`
- `ai-logs.md` — analysis and learning log
- `ai-plan.md` — implementation plan and progress

## Quick Start In A New Project

1. Copy this template structure into the new repository.
2. Copy `templates/spec/constitution.md` to `spec/constitution.md` and fill in project principles.
3. Create `spec/raw-spec.md`.
4. Open chat customizations and confirm skills are discoverable.
5. Execute either:
	- `/pipeline-orchestrator` for guided end-to-end execution
	- or run each phase skill in strict order:
		1. `/phase-ingest-spec`
		2. `/phase-clarify` *(optional — only if spec.yaml has open_questions)*
		3. `/phase-parallel-planning`
		4. `/phase-critique-round-1`
		5. `/phase-plan-revision`
		6. `/phase-cross-critique`
		7. `/phase-second-critique`
		8. `/phase-consensus-synthesis`
		9. `/phase-architecture-validation`
		10. `/phase-use-case-generation`
		11. `/phase-sequence-generation`
		12. `/phase-test-generation`
		13. `/phase-coverage-validation`
		14. `/phase-documentation-pack`
		15. `/phase-converge`
6. Prompt files remain available as compatibility wrappers for the same phases.

## Strict Fail Policy

Pipeline progression stops when any of the following occur:
- missing required phase input artifacts
- schema mismatch against `templates/artifacts/*.yaml`
- unresolved blocking ADRs
- traceability gaps in Requirement -> Use Case -> Sequence -> Test
- unresolved critical open questions during clarify gate (phase_00b)
- critical requirement not implemented without documented blocker during converge gate (phase_13)

## Production Feedback Loop

When the system is in production, the pipeline supports a closed feedback loop:
1. Incidents and recurring error patterns are appended to `spec/raw-spec.md` as amendments.
2. The convergence report (`artifacts/validation/convergence-report.yaml`) is reviewed each sprint.
3. If `converge_gate.pipeline_rerun_required: true`, the pipeline reruns from `/phase-ingest-spec`.

## Notes

- This implementation is Copilot and VS Code customization only, with no external orchestration runner.
- Skills are portable and can be reused across projects by copying `.github/skills/`.
- Context7 MCP integration is intentionally deferred to a follow-up increment.
- Each generated use case must map to a test plan and to the process flow represented by sequence definitions.
- Improvements informed by analysis of [spec-kit](https://github.com/github/spec-kit) (Spec-Driven Development) — see `ai-logs.md` for details.