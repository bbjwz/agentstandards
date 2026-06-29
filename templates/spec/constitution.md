# Project Constitution

## Purpose
This document establishes the governing principles and development guidelines that apply to all phases of this project. It is consumed during spec ingestion (phase_00) and consulted throughout the pipeline to ensure consistency.

---

## 1. Project Identity
- **Project Name:** [project-name]
- **Version:** 1.0
- **Owner:** [team or person]
- **Reviewed At:** [YYYY-MM-DD]

---

## 2. Technology Constraints
List the technologies, cloud providers, languages, and frameworks that are mandated or prohibited.

### Mandated
- [e.g., TypeScript for all backend services]
- [e.g., PostgreSQL as the primary datastore]

### Prohibited
- [e.g., no use of MongoDB in production]
- [e.g., no client-side secrets]

---

## 3. Engineering Principles
Define non-negotiable principles the team upholds regardless of timeline or scope.

- [e.g., Every public API endpoint must be covered by a contract test.]
- [e.g., No component may have cyclomatic complexity > 10.]
- [e.g., All secrets are stored in environment variables, never in source files.]

---

## 4. Quality Standards
Define the minimum acceptable bar for code quality, test coverage, and performance.

- Minimum test coverage: [e.g., 80%]
- Required test dimensions: unit, integration, contract, e2e
- Performance budget: [e.g., p95 response time < 200ms for core APIs]
- Security posture: [e.g., OWASP Top 10 compliance]

---

## 5. Compliance and Regulatory Constraints
List any compliance frameworks or legal requirements that affect design decisions.

- [e.g., GDPR — user data must be erasable within 30 days of request]
- [e.g., SOC 2 Type II — access logs retained for 1 year]

---

## 6. Architecture Boundaries
Define the service topology and integration constraints.

- [e.g., Frontend communicates only through the API gateway; no direct DB access]
- [e.g., All inter-service communication uses gRPC over internal VPC]

---

## 7. Governance and Decision Policy
- Architectural decisions must be recorded as ADRs.
- Rejected alternatives must be documented with reasons.
- Unresolved tradeoffs must remain explicit; they cannot be silently deferred.

---

## 8. Production Feedback Loop
Describe how production incidents and metrics feed back into spec evolution.

- P0 incidents trigger an emergency spec amendment appended to `spec/raw-spec.md`.
- Recurring error patterns become new non-functional requirements in the next pipeline run.
- The convergence report (`artifacts/validation/convergence-report.yaml`) is reviewed at each sprint boundary.
