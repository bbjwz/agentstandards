---
description: Use for architecture planning, adversarial review, consensus synthesis, and deterministic artifact generation.
applyTo: "**/*.md"
---

# Pipeline Core Rules

## Purpose
Enforce a deterministic multi-agent orchestration process with strict phase boundaries.

## Mandatory Behavior
- Use the exact phase order defined in .github/agents/AGENTS.md.
- Require required input artifacts before starting a phase.
- Produce only the required output artifacts for the active phase.
- Fail fast on missing inputs, schema violations, or unresolved blocking decisions.
- Keep debates bounded to configured rounds; never run open-ended loops.
- Prefer phase skills in .github/skills as the operator command surface.
- Keep skill execution deterministic and phase-scoped.

## Iteration Limits
- Planning rounds: 1
- Critique rounds: 2
- Revision rounds: 1
- Consensus rounds: 1

## Scoring and Critique
- Critiques must use the shared scorecard schema.
- Include strengths, weaknesses, risks, hidden assumptions, and recommended changes.
- Include dimensional scoring for scalability, security, simplicity, testability, cost, reliability.

## Consensus Requirements
- Explicitly list accepted decisions.
- Explicitly list rejected decisions and reasons.
- Explicitly list unresolved tradeoffs and required follow-up.
- Record all conflict resolutions in ADR format.

## Downstream Artifact Requirements
- Use-case generation is separate from planning.
- Sequence diagrams must be generated from structured interaction definitions.
- Test generation must span all required dimensions.
- Coverage validation must produce a traceability matrix.

## Gate Policy
- Strict fail: unresolved blocking ADRs or requirement traceability gaps stop progression.
- No manual bypass unless user explicitly requests an exception policy.
