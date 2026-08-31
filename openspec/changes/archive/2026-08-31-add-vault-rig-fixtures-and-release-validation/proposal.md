## Why

Behavior that works in one personal vault can still fail on custom directories, aliases, namespaces, UUID references, or pre-existing user configuration. Small public fixture vaults and one authoritative check are required to prove portability and non-destructive lifecycle behavior.

## What Changes

- Add minimal synthetic fixtures for each supported Logseq layout and graph invariant.
- Add a cheap targeted check and one authoritative release-validation entrypoint.
- Exercise install twice, doctor, update simulation, retrieval, integrity checking, and uninstall from clean disposable copies.
- Verify canonical fixture hashes and user-owned configuration remain unchanged outside explicit edit scenarios.
- Keep the check runnable locally and CI-ready without selecting a CI provider.

## Capabilities

### New Capabilities
- `release-validation`: Provides disposable fixtures and deterministic end-to-end evidence for supported Logseq Vault Rig behavior.

### Modified Capabilities
- None.

## Impact

Depends on lifecycle and Codex integration. It adds synthetic test data and stable validation entrypoints, not private vault content, model-quality benchmarks, network requirements, or untested portability promises.
