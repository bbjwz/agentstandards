# Agentstandards

[![CI](https://github.com/bbjwz/agentstandards/actions/workflows/ci.yml/badge.svg)](https://github.com/bbjwz/agentstandards/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/bbjwz/agentstandards)](https://github.com/bbjwz/agentstandards/releases)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/bbjwz/agentstandards/blob/main/LICENSE)

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

The council provides structured adversarial review, deterministic phase progression, typed
artifacts, explicit human decisions, and a hard task-generation gate when required reviewers do not
approve the architecture.

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

Provider credentials are read only from environment variables. They are never written to project
configuration or transcripts.

## Installation

For development, install from a reviewed checkout:

```bash
specify extension add /path/to/agentstandards --dev
specify preset add --dev /path/to/agentstandards/presets/agentstandards-gate
specify workflow add /path/to/agentstandards/workflows/agentstandards-architecture --dev
```

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
  --codex-model YOUR_EXACT_CODEX_MODEL_ID \
  --anthropic-model YOUR_EXACT_ANTHROPIC_MODEL_ID
```

Optional participants are passed as repeated JSON objects. Transport identity and underlying-vendor
identity are separate:

```bash
uv run --script .specify/extensions/agentstandards/scripts/python/agentstandards.py init \
  --codex-model YOUR_EXACT_CODEX_MODEL_ID \
  --anthropic-model YOUR_EXACT_ANTHROPIC_MODEL_ID \
  --provider-json '{"id":"google-via-abacus","transport":"openai-compatible","underlying_vendor":"google","model":"YOUR_EXACT_GOOGLE_MODEL_ID","api_key_env":"ABACUS_API_KEY","base_url":"https://routellm.abacus.ai/v1"}'
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

> [!WARNING]
> Architecture transcripts can still contain confidential product, customer, or infrastructure
> information. Agentstandards persists visible prompts and outputs so the gate can be audited, but it
> does not decide who may see the surrounding Git repository. Review `specs/<feature>/architecture/`
> before committing or sharing it, and run the council only in a repository with an appropriate
> visibility and retention policy.

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

See [the council design](https://github.com/bbjwz/agentstandards/blob/main/docs/multi-vendor-council.md)
and [the operational runbook](https://github.com/bbjwz/agentstandards/blob/main/docs/pipeline-runbook.md)
for more detail.

## Community and security

Contributions are welcome. Read the [contribution guide](https://github.com/bbjwz/agentstandards/blob/main/CONTRIBUTING.md)
and [Code of Conduct](https://github.com/bbjwz/agentstandards/blob/main/CODE_OF_CONDUCT.md) before
opening a pull request. Use GitHub Discussions for support and design questions. Report
vulnerabilities privately by following the [security policy](https://github.com/bbjwz/agentstandards/blob/main/SECURITY.md),
never through a public issue.
