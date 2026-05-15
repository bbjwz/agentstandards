# Copilot Instructions 

## Scope
These instructions apply to the full repository.

## Hard Rules
- Never remove logs
- Before major insert/update/delete database operations always ask for confirmation first and make a backup. 
- Limit the scope of your work to exactly the task at hand. When in doubt, ask for clarification before proceeding.
- Always aim for a modular design
- Aim for NASA 10 rules coding standards
- For architecture pipeline work, enforce deterministic phases and strict fail gates defined in .github/agents/AGENTS.md.
- Do not bypass schema contracts in templates/artifacts when generating phase outputs.

## Coding Standards
- Keep changes minimal and targeted; avoid unrelated refactors.

## Coding Standards TypeScript
- Maintain strict TypeScript compatibility; do not silence type errors with ts-ignore.

## UI and UX Expectations
- Prioritize clear states: loading, empty, error, and success.

## Testing and Validation
- After code changes, run relevant checks:
  - npm run lint
  - npm run typecheck
- For UX regression checks, use:
  - npm run test:ux:ai:local (local)
  - TEST_BASE_URL=<url> npm run test:ux:ai (deployed target)
  - npm run test:ux:ai:strict (CI hard-fail on error-level findings)

## AI UX Test Runner Conventions
- Keep production navigation robust:
  - non-local default wait strategy should avoid brittle network-idle assumptions.
- Always generate report artifacts under reports/<run-id>/.

## Deployment Workflow
- After requested changes are implemented and validated, commit changes.
- Push to main only when explicitly requested.

## Security and Secrets
- Never write raw secrets into source files, docs, logs, or commits.
- Use environment variables and platform secret stores (GitHub Secrets, Azure app settings).

## Documentation
- When adding significant functionality, append README with a concise "what was added" summary.
- Keep docs/ai-testing.md aligned with script behavior and environment variables.

## Pipeline Template Guardrails
- Keep structured adversarial review behavior intact: no open-ended debates.
- Preserve explicit accepted_decisions, rejected_decisions, unresolved_tradeoffs outputs in consensus artifacts.
- Preserve full Requirement -> Use Case -> Sequence -> Test traceability expectations.

