# Agentstandards bundle

The Agentstandards bundle installs a Codex-orchestrated, multi-vendor architecture council, its hard
task gate, and the supporting Spec Kit workflow. It is intended for architecture-governance work
between `$speckit-plan` and `$speckit-tasks`.

## Installed components

- Extension: `agentstandards@0.1.1`
- Preset: `agentstandards-gate@0.1.1`
- Workflow: `agentstandards-architecture@0.1.1`

The bundle targets the `codex` integration and requires Spec Kit `>=1.0.8,<2.0.0`, `uv`, and the
Codex CLI. Installation into a project configured for another integration is rejected by Spec Kit.

## Install from the Agentstandards catalogs

The three components live in non-default catalogs. Register each component catalog as
install-allowed where applicable, then register and install the bundle:

```bash
specify extension catalog add \
  https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.1/catalogs/extensions.json \
  --name agentstandards --install-allowed

specify preset catalog add \
  https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.1/catalogs/presets.json \
  --name agentstandards --install-allowed

specify workflow catalog add \
  https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.1/catalogs/workflows.json \
  --name agentstandards

specify bundle catalog add \
  https://raw.githubusercontent.com/bbjwz/agentstandards/v0.1.1/catalogs/bundles.json \
  --id agentstandards --policy install-allowed

specify bundle install agentstandards --integration codex
```

Catalogs marked `install-allowed` can supply executable project content. Review and trust the
catalogs and referenced release artifacts before enabling that policy.

## Install the release artifact directly

Direct bundle installation still needs the three component catalogs above because a bundle
contains references, not copies of its extension, preset, and workflow. After registering those
catalogs, download and install the versioned bundle artifact:

```bash
curl --fail --location \
  https://github.com/bbjwz/agentstandards/releases/download/v0.1.1/agentstandards-bundle-0.1.1.zip \
  --output agentstandards-bundle-0.1.1.zip

specify bundle install ./agentstandards-bundle-0.1.1.zip --integration codex
```

## Start the architecture council

After installation, run `$speckit-agentstandards-init` to pin the mandatory Codex and Anthropic
models and any optional participants. Then run `$speckit-agentstandards-architect` after
`$speckit-plan`, complete the human decision manifest, and run `$speckit-agentstandards-resume`.
`$speckit-tasks` remains blocked until the aggregate architecture gate is `READY`.

No provider calls happen during bundle installation or the offline task-gate check.
