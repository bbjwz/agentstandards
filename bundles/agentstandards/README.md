# Agentstandards bundle

This bundle installs the Agentstandards extension, the wrapping `speckit.tasks` gate preset, and the
`agentstandards-architecture` Codex workflow.

The component references resolve from the Agentstandards extension, preset, and workflow catalogs.
Register the three component catalogs as documented in the repository root README before installing
the catalog bundle. For local development, install those components with their `--dev` options before
running offline bundle validation.

After installation, run `$speckit-agentstandards-init` to pin the mandatory Codex and Anthropic
models and any optional participants. No provider calls happen during bundle installation.
