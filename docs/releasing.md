# Maintainer release guide

Agentstandards publishes three Spec Kit archives plus a Python wheel and source distribution from a
single version tag.

## Prepare

1. Update `project.version` in `pyproject.toml`.
2. Update the matching versions and versioned URLs in the extension, preset, workflow, bundle,
   runtime, and catalogs.
3. Update catalog timestamps and `CHANGELOG.md`.
4. Run `python3 scripts/check_release_metadata.py`. Release construction fails when any declared
   version differs from `pyproject.toml`.
5. Run the complete offline verification:

   ```bash
   uv sync --extra test --locked
   uv run --extra test ruff check .
   uv run --extra test pytest
   SPEC_KIT_VERSION=1.0.8 bash scripts/verify_spec_kit_install.sh
   SPEC_KIT_VERSION=1.0.10 bash scripts/verify_spec_kit_install.sh
   uv build
   uv run python scripts/build_release.py --output dist
   ```

## Publish

Create and push an annotated `v<version>` tag from the verified `main` commit. The release workflow
repeats offline verification, builds all distributions, creates SHA-256 checksums, generates build
provenance attestations, and publishes the artifacts in a GitHub release.

Do not recreate or move an existing release tag. Publish a new patch version when a released
artifact needs correction.
