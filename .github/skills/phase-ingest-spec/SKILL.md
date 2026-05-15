---
name: phase-ingest-spec
description: Normalize raw requirements into artifacts/spec.yaml with stable requirement IDs and acceptance criteria. Use at the start of every pipeline run.
argument-hint: path to raw spec markdown
user-invocable: true
disable-model-invocation: true
---

# Phase Ingest Spec Skill

## Inputs
- Source document such as spec/raw-spec.md

## Output
- [spec template](../../../templates/artifacts/spec.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-00-ingest-spec.prompt.md).
2. Extract requirements and assign REQ identifiers.
3. Capture constraints, non-goals, and acceptance criteria.
4. Record open questions explicitly.

## Gate
Fail if critical requirements are missing IDs or acceptance criteria.
