# AI Improvement Plan

## Initiative: spec-kit / OpenSpec Analysis Improvements
**Issue:** #3
**Status:** In Progress

---

## Plan

### Phase 1: Analysis Documentation
- [x] Read spec-kit repository and core SDD documentation
- [x] Read Hashrocket comparison article
- [x] Identify gaps in agentstandards vs. spec-kit capabilities
- [x] Document findings in ai-logs.md

### Phase 2: New Artifact Schemas
- [x] `templates/spec/constitution.md` — governing principles bootstrap template
- [x] `templates/artifacts/constitution.yaml` — constitution YAML schema
- [x] `templates/artifacts/clarification-log.yaml` — clarification log schema
- [x] `templates/artifacts/convergence-report.yaml` — convergence report schema

### Phase 3: New Prompt Files
- [x] `.github/prompts/phase-00b-clarify.prompt.md` — optional clarify phase prompt
- [x] `.github/prompts/phase-13-converge.prompt.md` — converge phase prompt

### Phase 4: New Skills
- [x] `.github/skills/phase-clarify/SKILL.md`
- [x] `.github/skills/phase-converge/SKILL.md`

### Phase 5: Registry and Orchestration Updates
- [x] Update `.github/agents/AGENTS.md`
- [x] Update `.github/skills/pipeline-orchestrator/SKILL.md`

### Phase 6: Documentation Updates
- [x] Update `docs/pipeline-runbook.md`
- [x] Update `docs/skills-catalog.md`
- [x] Update `README.md`

---

## Deferred Work

| Item | Reason |
|---|---|
| Feature-scoped `artifacts/[feature-id]/` layout | Breaking change; requires all artifact contract updates |
| `/speckit.analyze` equivalent (early cross-artifact validation) | Can be folded into clarify gate; low priority |
| Bidirectional feedback loop automation | Documented as re-entry pattern in runbook; full automation deferred |
| `specify` CLI integration | Python/uv dependency; out of scope |
| Context7 MCP integration | Already noted as deferred in README notes |
