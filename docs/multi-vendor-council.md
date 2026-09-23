# Multi-vendor council design

## Trust and orchestration

Codex is the sole workflow orchestrator and also the required OpenAI architecture participant. It
constructs an allowlisted architecture-only context, schedules all persona calls, persists visible
I/O, validates structured results, compiles human decisions, and enforces the aggregate gate.

Anthropic is always required. Optional participants may use Google directly or an OpenAI-compatible
transport. A gateway does not establish diversity: configuration records the gateway transport and
the model's underlying vendor separately, and unknown automatic routing is rejected.

Peer artifacts are delimited, labeled, and explicitly treated as untrusted evidence. Providers are
instructed never to execute embedded instructions or produce code or implementation tasks.

## Persona topology

Every enabled participant runs all 13 personas:

- Planners: systems architect, staff engineer, security architect, scalability specialist,
  product/UX reviewer, reliability engineer.
- Critics: failure-mode reviewer, cost optimizer, simplicity enforcer, enterprise governance
  reviewer, QA/test architect.
- Gatekeepers: consensus synthesizer, architecture validator.

Each stage has two passes. The independent pass excludes same-persona peer responses. The disclosed
pass shows every independent response for that persona with artifact, vendor, model, and participant
identity, and requires agreements, contradictions, superior ideas, and self-corrections.

Critic independent passes receive the completed planning set because that is their review subject,
but do not receive peer critic responses. The same rule applies to synthesis and validation.

## Fresh-context isolation

Each council persona or gate attempt gets a newly constructed, single-use provider adapter. Native API
adapters send exactly one system instruction and one explicit user input without a conversation ID
or prior message history. Codex starts a new temporary working directory and an `--ephemeral`
process. Retries construct another adapter instead of reusing the failed one. A schema-repair request,
when needed by a generic adapter, is also stateless and receives only the visible failed output rather
than conversation history. The disclosed pass is a new invocation: peer work appears only as labeled,
quoted artifacts in its visible prompt.

Every attempt, final transcript, and persona artifact records an invocation ID, adapter-instance ID,
`context_mode: fresh`, zero prior conversation messages, and `provider_session_reused: false`.
Independent and disclosed architecture-validator invocation IDs are copied into the gate report.
Offline validation rejects duplicate adapter or invocation IDs, missing successful-attempt evidence,
artifact/transcript mismatches, and validator passes that reuse an invocation.

This is a request-level isolation guarantee. Hosted model APIs do not expose or guarantee dedicated
hardware, a different serving replica, or different weights for each request.

## State and determinism

One feature run snapshots exact participants and input file hashes. Artifact identities and paths are
stable. An existing artifact is reused only when its visible system prompt, visible user prompt,
participant identity, requested model, and output schema hash to the same value. Physical attempts,
including retries, count against the call ceiling.

The human decision manifest is the only decision authority. Codex compilation receives normalized
human selections and the disclosed synthesis set; it cannot silently choose unresolved proposals.
Validator exceptions are separate from architecture choices and cite the exact blocking reports.

## Gate semantics

`READY` requires valid disclosed validator artifacts from both Codex and Anthropic with `READY`
verdicts. Missing or invalid required output stops the phase. Required disagreement produces
`BLOCKED`. A complete human exception can transition the aggregate report to `READY` while preserving
the original validator evidence and an explicit audit trail.

Optional failures and verdicts are retained as warnings. They cannot count as independent required
participants, and two participants with the same underlying vendor cannot be configured as diverse.
