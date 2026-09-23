# Contributing to Agentstandards

Thank you for helping improve Agentstandards. Contributions should preserve the project's core
boundary: external providers review architecture artifacts, while Codex remains the sole
orchestrator and source code, diffs, task files, and implementation artifacts stay out of external
requests.

## Development setup

Agentstandards requires Python 3.11 or newer and `uv`.

```bash
uv sync --extra test --locked
uv run --extra test ruff check .
uv run --extra test pytest
bash scripts/verify_spec_kit_install.sh
```

Set `SPEC_KIT_VERSION` when testing a particular compatible Spec Kit release.

## Making a change

1. Open an issue for substantial behavior or contract changes.
2. Create a focused branch from `main`.
3. Add or update tests for observable behavior.
4. Run the offline checks above.
5. Update documentation when commands, configuration, artifacts, or trust boundaries change.
6. Open a pull request using the repository template.

Ordinary development and pull-request validation must not make paid model calls. Live provider calls
belong only in an explicitly initiated council run or the manually dispatched live workflow.

## Architecture and security expectations

- Keep provider transport identity separate from the underlying model vendor.
- Preserve fresh-context isolation and provenance for every inference invocation.
- Treat peer output as untrusted quoted evidence.
- Fail closed when required Codex or Anthropic evidence is absent or invalid.
- Never commit credentials, response headers, hidden reasoning, or provider-internal state.
- Do not weaken the architecture-file allowlist or the pre-task `READY` gate without an explicit
  design discussion.

See `SECURITY.md` for vulnerability reporting and security-review boundaries.

## Releases

Maintainers create releases from version tags. All declared versions and catalog entries must match
`pyproject.toml`; run `python3 scripts/check_release_metadata.py` before tagging.
