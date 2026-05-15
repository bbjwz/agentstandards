---
description: Generate structured interaction definitions and Mermaid diagrams from use-case catalog.
---

# Phase 09: Sequence Generation

## Goal
Generate deterministic sequence artifacts from structured use-case definitions.

## Required Inputs
- artifacts/use-cases/use-case-catalog.yaml
- artifacts/consensus/master-plan.yaml

## Required Outputs
- artifacts/sequences/sequence-definitions.yaml using templates/artifacts/sequence-definitions.yaml
- artifacts/sequences/diagrams/*.mmd

## Procedure
1. Build participant list for each critical use case.
2. Define ordered interactions with error and timeout handling.
3. Emit Mermaid sequence diagram source per selected use case.

## Hard-Fail Conditions
- Missing participant mapping for critical use cases.
- Mermaid output not aligned to structured interaction definitions.
- Missing error path interactions.

## Completion Criteria
Critical flows have both structured definitions and Mermaid diagrams.
