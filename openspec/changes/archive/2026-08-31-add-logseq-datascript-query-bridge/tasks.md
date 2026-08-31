## 1. Local API Client

- [x] 1.1 Implement the loopback-only HTTP client using environment-provided endpoint and token with redacted diagnostics, then verify missing, invalid, non-loopback, unauthorized, and unavailable configurations fail safely.
- [x] 1.2 Implement the DataScript capability probe and supported-version evidence, then verify bridge unavailability does not affect any offline core command.

## 2. Named Query Library

- [x] 2.1 Define the versioned named-query registry with argument and result schemas, then verify unknown names, missing arguments, and incompatible registry versions are rejected before HTTP execution.
- [x] 2.2 Add the initial parameterized structural and closure query fixtures plus the draft-inspect-verify-register procedure, then verify no query contains hardcoded fixture paths.

## 3. Query Execution

- [x] 3.1 Implement vault-rig query for registered read-only DataScript calls, then verify the client cannot select arbitrary API methods or graph-write operations.
- [x] 3.2 Normalize returned pages and blocks through existing resolvers, then verify source evidence is attached when resolvable and explicitly marked when not.

## 4. Verification and Rollout

- [x] 4.1 Add mock HTTP contract tests for success, API drift, auth failure, malformed results, and secret redaction, then verify the suite runs without Logseq or network access.
- [ ] 4.2 Run the named-query integration fixtures against a supported local Logseq OG instance when available, then record the tested version and verify expected results.
- [x] 4.3 Document opt-in environment setup and removal, then verify disabling the bridge leaves canonical Markdown and all core retrieval tests unchanged.
