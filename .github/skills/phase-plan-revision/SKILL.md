---
name: phase-plan-revision
description: Revise each plan by consuming round-1 critiques and recording explicit finding dispositions.
argument-hint: optional focus on unresolved high-severity findings
user-invocable: true
disable-model-invocation: true
---

# Phase Plan Revision Skill

## Inputs
- artifacts/plans/*.yaml
- artifacts/critiques/round-1/*.yaml

## Output Template
- [revised plan template](../../../templates/artifacts/revised-plan.yaml)

## Procedure
1. Follow [phase prompt](../../prompts/phase-03-plan-revision.prompt.md).
2. Map each critique finding to a disposition: incorporated, rejected_with_reason, or deferred.
3. Update decisions and risks accordingly.
4. Record dimensional score deltas.

## Gate
Fail if any critique finding is dropped without disposition.
