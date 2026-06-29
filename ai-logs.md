# AI Analysis Log

## Session: spec-kit and OpenSpec Analysis
**Date:** 2026-06-29
**Issue:** #3 — Analyze openspec and spec kit for improvement on our agentstandards

---

## Sources Analyzed

### 1. spec-kit (github/spec-kit)
- URL: https://github.com/github/spec-kit
- Approach: **Spec-Driven Development (SDD)** — specifications become executable artifacts
- Tooling: Python CLI (`specify`), prompt/skill injection into AI coding agents

### 2. OpenSpec / Hashrocket Article
- URL: https://hashrocket.com/blog/posts/openspec-vs-spec-kit-choosing-the-right-ai-driven-development-workflow-for-your-team
- Approach: Requirements-first with formal specification language; more structured than ad-hoc AI prompting

---

## Key Learnings from spec-kit

### 1. Constitution Phase (Governance First)
spec-kit introduces `/speckit.constitution` as a **pre-pipeline step** that establishes governing principles, coding standards, and team conventions before any specification work begins. This prevents spec drift and ensures all downstream phases inherit consistent constraints.

**Gap in agentstandards:** Pipeline starts immediately at spec ingestion without establishing organizational or technical principles. Decisions are left implicit and may conflict across planners.

**Improvement:** Add a `spec/constitution.md` bootstrap document and reference it as a mandatory prerequisite in the pipeline. This aligns with the hard-constraint model already in AGENTS.md.

### 2. Clarify Phase (Explicit Ambiguity Resolution)
spec-kit introduces `/speckit.clarify` as an **optional but recommended step** between spec definition and technical planning. It surfaces underspecified requirements and forces resolution before expensive planning work begins.

**Gap in agentstandards:** Phase 00 (spec ingestion) captures `open_questions` in the YAML artifact but there is no explicit phase dedicated to resolving them. Planners receive ambiguous specs and must individually guess resolutions, leading to divergent plans.

**Improvement:** Add an optional `phase-clarify` step between phase_00 and phase_01. It ingests `artifacts/spec.yaml` (specifically the `open_questions` field), resolves ambiguities through structured dialogue, and emits a `clarification-log.yaml`. Phase_01 gates on this log if open_questions were present.

### 3. Converge Phase (Codebase Alignment Check)
spec-kit introduces `/speckit.converge` as a **post-implementation terminal phase** that assesses the actual codebase against the spec, plan, and tasks, then appends remaining gaps as new tracked work.

**Gap in agentstandards:** Pipeline terminates at documentation pack. There is no mechanism to validate that the generated documentation reflects actual implementation, or to capture what was deferred or is still pending.

**Improvement:** Add `phase_13_converge` as the terminal phase after documentation pack. It compares the traceability matrix and test matrix against current codebase state, identifies drift, and emits a `convergence-report.yaml`.

### 4. Cross-Artifact Consistency Analysis
spec-kit's `/speckit.analyze` runs cross-artifact validation before implementation — checking that spec, plan, and tasks are mutually consistent and complete. This is similar to our coverage validation (phase_11) but runs earlier.

**Gap in agentstandards:** Cross-artifact consistency is checked only after sequences and tests are generated. Earlier detection of spec-plan mismatches would reduce rework.

**Note:** This could be folded into the clarify phase gate or added as an enhancement to architecture validation (phase_07). Not implemented in this increment; deferred.

### 5. Feature-Scoped Directory Structure
spec-kit organizes artifacts per feature: `specs/[feature-id]/` with all related documents co-located. This scales better for multi-feature projects.

**Gap in agentstandards:** All artifacts live under flat `artifacts/` directories. For multi-feature work, this becomes ambiguous.

**Note:** This is an infrastructure-level change that affects the entire artifact contract. Deferred to a follow-up increment. The current flat structure is acceptable for single-feature pipeline runs.

### 6. Bidirectional Feedback Loop
SDD emphasizes that production metrics and incidents should feed back into spec evolution. Specifications are living documents.

**Gap in agentstandards:** Pipeline is one-directional (spec → plan → critique → … → docs). There is no documented mechanism for production feedback to trigger spec updates.

**Improvement:** Document a re-entry pattern in the runbook: production incidents create a new `spec/raw-spec.md` amendment, which restarts the pipeline from phase_00 with the converge report as supplementary context.

---

## What We Are NOT Adopting

| spec-kit Capability | Reason for Deferral |
|---|---|
| `specify` CLI tooling | Python/uv dependency; agentstandards is Copilot-native, no external runners |
| Preset/extension system | Adds infrastructure complexity; agentstandards uses instruction files instead |
| Feature-scoped `specs/[id]/` layout | Breaking change to artifact contracts; deferred |
| Auto branch creation on specify | Out of scope for prompt/skill surface |

---

## Summary of Implemented Improvements

1. `spec/constitution.md` — bootstrap template (in `templates/spec/`)
2. `templates/artifacts/constitution.yaml` — constitution YAML schema
3. `templates/artifacts/clarification-log.yaml` — clarify phase artifact schema
4. `templates/artifacts/convergence-report.yaml` — converge phase artifact schema
5. `.github/prompts/phase-00b-clarify.prompt.md` — optional clarify prompt
6. `.github/prompts/phase-13-converge.prompt.md` — converge prompt
7. `.github/skills/phase-clarify/SKILL.md` — clarify skill
8. `.github/skills/phase-converge/SKILL.md` — converge skill
9. Updated `AGENTS.md` — added clarify (optional) and converge (phase_13)
10. Updated `pipeline-orchestrator` skill
11. Updated `docs/pipeline-runbook.md`
12. Updated `docs/skills-catalog.md`
13. Updated `README.md`
