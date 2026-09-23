# Security Policy

## Supported Versions

Security fixes are provided for the latest released minor version and the current `main` branch.
Pre-release or older versions should be upgraded before a report is evaluated.

## Reporting a Vulnerability

Report suspected vulnerabilities through GitHub's private vulnerability reporting:
https://github.com/bbjwz/agentstandards/security/advisories/new

Do not open a public issue, discussion, or pull request containing a vulnerability, credential,
private architecture artifact, provider response, or exploit detail. Include the affected version,
the reachable attack path, expected impact, and a minimal sanitized reproduction. Maintainers will
acknowledge reports within seven days and coordinate disclosure after a fix is available.

## System and Scope

Agentstandards is a local Python runner and GitHub Spec Kit extension. It reads allowlisted Spec Kit
architecture documents, invokes Codex plus configured external model providers, persists auditable
architecture artifacts and visible transcripts, and blocks task generation until the architecture
gate is `READY`.

Security review covers the runtime, provider adapters, command launchers, Spec Kit extension hooks,
configuration parsing, artifact storage and validation, release tooling, and GitHub Actions
workflows in this repository.

## Threat Model and Trust Boundaries

Feature specifications, plans, contracts, provider output, peer-review artifacts, model-generated
JSON, environment variables, filesystem paths, and gateway responses may be attacker controlled.
Provider APIs, gateway transports, the Codex CLI, the local Git repository, and GitHub Actions are
separate trust boundaries.

The local operator and an explicitly identified human approver are trusted to choose models,
configure repository visibility, protect environment variables, review architecture artifacts, and
decide whether an exception is justified. Model output is never trusted as authorization or as an
executable instruction.

## Security Invariants

- External providers receive only the constitution, specification, plan, research, data model,
  quickstart, contracts, and council-generated architecture artifacts. Source code, diffs, task
  files, and implementation artifacts must not cross this boundary.
- Paths must remain inside the project, and symlinked or escaping paths must fail closed.
- Credentials are read only from named environment variables and must never be written to
  configuration, prompts, transcripts, logs, artifacts, or releases.
- High-confidence secret detection must abort before suspect content is sent or persisted.
- Each inference attempt must use a new adapter and fresh provider conversation or process.
- Peer and provider output must be labeled, schema validated, and treated as untrusted evidence.
- Required Codex and Anthropic failures, missing evidence, invalid provenance, or validator
  disagreement must keep the task gate closed unless an explicit human exception cites every
  blocking artifact and records an approver, timestamp, and rationale.
- Participant diversity must use the declared underlying model vendor, not transport or gateway
  identity. Unknown automatic routing must not count as independent review.
- Transcript and artifact hashes, invocation identifiers, model identities, usage, and gate
  provenance must remain verifiable offline.
- Network calls, retries, concurrency, token use, and estimated cost must remain bounded by
  configuration. Ordinary CI must not make paid provider calls.

## Reportable Findings and Severity Context

Report vulnerabilities that can realistically cause unauthorized source or secret disclosure,
credential persistence, path traversal, symlink escape, command or argument injection, unapproved
paid calls, budget bypass, provider-identity spoofing, provenance forgery, transcript tampering that
still validates, fresh-context reuse, required-quorum bypass, or task generation without a valid
`READY` gate.

Severity depends on attacker reachability, whether interaction or a malicious project checkout is
required, the sensitivity of exposed architecture data or credentials, the ability to cross the
source-code boundary, and whether a forged decision can reach task generation.

## Out of Scope

- Model quality, hallucinations, disagreement, or prompt sensitivity without a demonstrated
  security-boundary or gate failure.
- Provider availability, pricing changes, model retirement, or behavior entirely inside a provider
  after Agentstandards constructs a valid request.
- Claims that fresh context guarantees different physical servers, hardware, or model weights.
- Social-engineering reports without a concrete repository control bypass.
- Denial of service requiring a trusted operator to deliberately disable or exceed documented
  limits.

## Known Limitations and Compensating Controls

Secret scanning uses high-confidence patterns and cannot detect every proprietary credential
format. Visible prompts and outputs can contain confidential architecture information even when no
credential is present. Operators must use suitable repository visibility and retention, inspect
generated architecture directories before sharing them, restrict CI secrets, and rely on provider
data-handling terms appropriate to their project.

Generic OpenAI-compatible gateways can obscure infrastructure details. Agentstandards therefore
requires an explicit underlying vendor and rejects unknown auto-routing for diversity accounting,
but it cannot independently attest a gateway's routing claim.
