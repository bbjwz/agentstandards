# Agentstandards

Agentstandards is an MIT-licensed [GitHub Spec Kit](https://github.com/github/spec-kit)
extension, workflow, and preset that inserts a multi-vendor architecture council between
`$speckit-plan` and `$speckit-tasks`.

```text
constitution → specify → clarify → plan
    → Agentstandards architecture council
    → human decision gate
    → multi-vendor architecture validation
    → tasks → implementation
```

This template enforces:

- Structured adversarial review (not open-ended debate)
- Deterministic phase progression
- YAML-first intermediate artifacts
- Strict fail gates on unresolved blockers and traceability gaps
- Full artifact chain coverage: Requirement -> Use Case -> Sequence -> Test
- Closed-loop feedback via a post-implementation convergence phase

Codex is the only orchestrator and the mandatory OpenAI participant. Anthropic is the mandatory
external participant. Google and OpenAI-compatible transports such as Abacus RouteLLM and
OpenRouter are optional, but every enabled participant runs every architecture persona. External
participants receive architecture artifacts only—never source code, diffs, tasks, or implementation
artifacts.

## What it installs

- `$speckit-agentstandards-init` pins participant models, vendors, budgets, and transcript policy.
- `$speckit-agentstandards-architect` runs planning, critique, and synthesis, then pauses.
- `$speckit-agentstandards-resume` compiles human decisions and runs final validation.
- `$speckit-agentstandards-status` reports participants, progress, usage, failures, and gate state.
- A mandatory `before_tasks` hook and wrapping preset refuse task generation unless the saved gate is
  `READY`.
- The `agentstandards-architecture` workflow runs the Codex Spec Kit lifecycle through gated task
  generation.

The canonical registry contains 13 personas: six planners, five critics, a consensus synthesizer,
and an architecture validator. Every persona uses an independent pass followed by a disclosed pass.
Disclosed artifacts name the participant, underlying vendor, exact model, persona, and artifact ID so
reviewers know whose work they are challenging.

Every inference attempt is context-isolated. The runner constructs a new single-use provider adapter,
starts a new stateless API request or ephemeral Codex process, and supplies only the visible context
for that pass. Independent and disclosed validator passes therefore cannot inherit conversation
state from planning, critique, synthesis, compilation, or one another. Transcripts and the aggregate
gate report carry distinct invocation IDs, and offline validation rejects reused or missing isolation
evidence. This guarantees a fresh conversation context; hosted APIs cannot guarantee a physically
different model server or set of weights.

## Requirements

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Codex CLI authenticated for the selected Codex model
- Spec Kit 1.0.8 or newer, below 2.0
- An Anthropic API key exposed through the configured environment-variable name

### Migration-reference assets

The older Copilot-oriented workflow remains available for migration and comparison. It includes
phase-prefixed prompts and skills from ingestion through convergence, an optional clarification
phase, a post-implementation convergence phase, and YAML contracts for the constitution,
clarification log, and convergence report. These assets live under `.github/`, `templates/`,
`ai-logs.md`, and `ai-plan.md`; the Spec Kit extension remains the supported runtime.

Provider credentials are read only from environment variables. They are never written to project
configuration or transcripts.

## Installation

Until a tagged public release exists, install from a reviewed checkout:

```bash
specify extension add /path/to/agentstandards --dev
specify preset add --dev /path/to/agentstandards/presets/agentstandards-gate
specify workflow add /path/to/agentstandards/workflows/agentstandards-architecture --dev
```

### Legacy gate conditions

The deprecated Copilot workflow stops when any of the following occur:

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

Tagged releases publish Spec Kit archives and catalogs. A catalog-backed bundle install is:

```bash
specify extension catalog add https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.0/catalogs/extensions.json --name agentstandards --install-allowed
specify preset catalog add https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.0/catalogs/presets.json --name agentstandards --install-allowed
specify workflow catalog add https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.0/catalogs/workflows.json --name agentstandards
specify bundle catalog add https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.0/catalogs/bundles.json --id agentstandards --policy install-allowed
specify bundle install agentstandards
```

Only mark catalogs `install-allowed` after reviewing and trusting their contents.

## Configure a project

Invoke `$speckit-agentstandards-init` in Codex, or run the deterministic helper directly:

```bash
uv run --script .specify/extensions/agentstandards/scripts/python/agentstandards.py init \
  --codex-model gpt-5.6-sol \
  --anthropic-model claude-sonnet-4-5
```

Optional participants are passed as repeated JSON objects. Transport identity and underlying-vendor
identity are separate:

```bash
uv run --script .specify/extensions/agentstandards/scripts/python/agentstandards.py init \
  --codex-model gpt-5.6-sol \
  --anthropic-model claude-sonnet-4-5 \
  --provider-json '{"id":"google-via-abacus","transport":"openai-compatible","underlying_vendor":"google","model":"gemini-2.5-pro","api_key_env":"ABACUS_API_KEY","base_url":"https://routellm.abacus.ai/v1"}'
```

`auto`, `default`, `route-llm`, and other unknown-routing model IDs are rejected for diversity
accounting. Every enabled participant must declare a distinct underlying vendor.

## Run the council

After `$speckit-plan` has produced `spec.md` and `plan.md`:

1. Run `$speckit-agentstandards-architect`.
2. Review `specs/<feature>/architecture/decision-manifest.yaml` and its cited artifacts.
3. Select the decisions, provide rationale, and mark the manifest approved.
4. Run `$speckit-agentstandards-resume`.
5. Run `$speckit-tasks`; it proceeds only when the aggregate gate is `READY`.

If Codex or Anthropic blocks validation, the task gate stays closed. A human can remediate and run a
new council, or record an explicit exception that cites every blocking validator artifact, an
approver, a timestamp, and rationale.

## Artifacts and privacy boundary

Each feature stores versioned output under `specs/<feature>/architecture/`:

```text
architecture/
├── current-run.json
├── decision-manifest.yaml
├── master-plan.yaml
├── adr-log.yaml
├── gate-report.yaml
└── runs/<run-id>/
    ├── config-snapshot.yaml
    ├── context-manifest.json
    ├── state.json
    ├── artifacts/<stage>/<pass>/<persona>/<participant>.yaml
    └── transcripts/<stage>/<pass>/<persona>/
        ├── <participant>.json
        └── <participant>.attempt-NN.json
```

Transcripts contain visible prompts and outputs, timestamps, exact requested and resolved models,
usage, estimated cost, latency, request IDs, content hashes, and fresh-context isolation evidence.
They exclude API keys, headers,
hidden reasoning, and provider-internal state. High-confidence secret detection aborts before sending
or persisting content.

The external context allowlist is limited to the Spec Kit constitution, feature specification, plan,
research, data model, quickstart, contracts, and council-generated architecture artifacts. Symlinks,
source paths, diffs, and task files are rejected.

## Failure and CI behavior

Required Codex or Anthropic failures stop the phase. Optional-provider failures are recorded as
warnings and do not satisfy required quorum. Calls use bounded retries and concurrency, and runs are
resumable by stable artifact input hashes.

Ordinary CI never makes paid model calls. It runs formatting, tests, schema/provenance validation,
transcript secret scanning, decision-manifest checks, and gate verification. Live calls happen only
when a person explicitly invokes the council or manually dispatches the live workflow.

```bash
uv sync --extra test
uv run --extra test ruff check .
uv run --extra test pytest
```

## Migration note

The original `.github/agents`, `.github/prompts`, and `.github/skills` Copilot-oriented assets remain
as migration references. They are deprecated entrypoints. `runtime/agentstandards/personas.yml` is now
the authoritative persona registry, and the Spec Kit extension commands are the supported runtime.
The legacy skills remain portable for teams that need a staged migration, including constitution,
clarification, convergence, and requirement-to-test traceability assets. Context7 integration remains
deferred; see `ai-logs.md` for the original Spec Kit/OpenSpec analysis.

See [the council design](docs/multi-vendor-council.md) and
[the operational runbook](docs/pipeline-runbook.md) for more detail.
