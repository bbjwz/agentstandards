---
name: phase-clarify
description: Resolve open questions from spec ingestion before parallel planning. Recommended when artifacts/spec.yaml contains open_questions entries. Produces clarification-log.yaml.
argument-hint: path to spec.yaml with open questions
user-invocable: true
disable-model-invocation: true
---

# Phase Clarify Skill (Optional)

This skill is an optional pre-planning step. Run it when `artifacts/spec.yaml` contains open questions that could cause planners to make divergent assumptions.

## When to Use
- After `/phase-ingest-spec` and before `/phase-parallel-planning`
- Only when `artifacts/spec.yaml` contains one or more `open_questions` entries
- Skip if the spec has no open questions

## Inputs
- artifacts/spec.yaml (required — must contain open_questions)
- spec/constitution.md (optional — used to constrain resolutions)

## Output
- [clarification-log template](../../../templates/artifacts/clarification-log.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-00b-clarify.prompt.md).
2. Classify each open question as answerable or deferrable.
3. Record resolutions and spec amendments.
4. Confirm planning readiness gate.

## Gate
Fail if any critical open question is unresolved without a documented deferral reason.
