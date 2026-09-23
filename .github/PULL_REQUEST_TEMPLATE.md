## Summary

<!-- What changed and why? -->

## Verification

- [ ] `uv run --extra test ruff check .`
- [ ] `uv run --extra test pytest`
- [ ] Spec Kit clean-install verification, when distribution or integration files changed
- [ ] No paid provider calls were made by ordinary PR validation

## Safety and compatibility

- [ ] No credentials, private architecture material, or generated transcripts are included
- [ ] Provider and source-code trust boundaries are unchanged, or the change is explained below
- [ ] Required-provider quorum and the pre-task `READY` gate remain fail closed
- [ ] User-facing configuration or behavior changes are documented
