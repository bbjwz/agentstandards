# Agentstandards operational runbook

## 1. Install and configure

Before the first council run, establish the project constitution with Spec Kit. Its technology
constraints, engineering principles, quality standards, and compliance requirements become part of
the allowlisted architecture context.

Install the extension, task-gate preset, and workflow. Run `$speckit-agentstandards-init` once per
project. Pin exact models, declare the actual underlying vendor separately from any gateway, and
configure only environment-variable names for credentials.

Confirm configuration without provider calls:

```bash
uv run --script .specify/extensions/agentstandards/scripts/python/agentstandards.py status
```

## 2. Complete Spec Kit planning

The active feature must have `spec.md` and `plan.md`. Constitution, research, data model, quickstart,
and contracts are included when present. Source, diffs, task files, and implementation artifacts are
outside the external-provider boundary.

## 3. Run through the human gate

Run `$speckit-agentstandards-architect`. The runner executes independent and disclosed passes for the
six planners, five critics, and consensus synthesizer. It then writes a run-scoped decision manifest
and stops in `awaiting_human`.

Review the synthesis options and cited artifacts. Complete one selection for every conflict, include
rationale, set `status: approved`, and add `decided_by` plus an ISO-8601 `decided_at` timestamp.

## 4. Resume and validate

Run `$speckit-agentstandards-resume`. Codex compiles the selected decisions into the authoritative
master plan. Every participant then runs the architecture-validator persona in independent and
disclosed passes. Each pass is a new inference invocation with no inherited conversation history;
the disclosed pass sees earlier work only through the labeled artifacts included in its prompt.

The gate becomes `READY` only when both required participants—Codex and Anthropic—return `READY`.
Optional participant failures or blocking verdicts remain visible warnings but do not replace the
required quorum.

## 5. Resolve a blocked gate

Preferred path: remediate the architecture inputs and start a new council with `architect --new-run`.

Exception path: set the decision manifest status to `exception` and add an exception containing every
blocking required-validator artifact ID, reason, approver, and timestamp. Run resume again. The gate
records `exception_applied: true`; it never rewrites a blocking validator verdict.

## 6. Generate tasks

Invoke `$speckit-tasks`. Both the extension hook and wrapping preset run the offline gate command.
Missing, invalid, awaiting, or blocked reports stop task generation before `tasks.md` is touched.

## 7. Audit and recovery

- `$speckit-agentstandards-status` is read-only and makes no paid calls.
- Run `uv run --script .specify/extensions/agentstandards/scripts/python/agentstandards.py validate --all`
  to validate schemas, run IDs, provenance, transcript hashes, fresh-context isolation, and secret
  scanning offline.
- Audit `validator_isolation` in `gate-report.yaml` to confirm distinct independent and disclosed
  invocation IDs for each required participant.
- Re-running a partial phase reuses artifacts only when the full visible input hash matches.
- Changed Spec Kit inputs or participant configuration require a new run.
- Never edit provider artifacts or transcripts. Human authority belongs in the decision manifest.
- Treat visible transcripts as potentially confidential project material and review the complete
  architecture directory before committing or sharing it.
