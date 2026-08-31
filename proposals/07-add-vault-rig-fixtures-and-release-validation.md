# Proposed OpenSpec Change: add-vault-rig-fixtures-and-release-validation

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-vault-rig-fixtures-and-release-validation`  
**Release target:** `0.1`  
**Depends on:** `add-vault-rig-lifecycle`, `add-codex-vault-rig-integration`

## Intent

Make Vault Rig itself verifiable by adding representative disposable Logseq OG fixture vaults and an authoritative release check for install, retrieval, validation, update, and uninstall behavior.

## Current / Problem

Vault Rig can appear correct in one personal vault while failing on aliases, namespaces, custom directories, block references, or pre-existing user configuration. Without fixture vaults, installer and parser regressions are difficult to detect independently.

## Desired Behavior

Contributors can run one stable validation entrypoint that installs the current Vault Rig build into disposable fixture vaults, exercises supported behavior, and proves idempotence/non-destructive lifecycle guarantees before release.

## In Scope

- Create minimal fixture vaults for default layout, custom directories/journal format, aliases/namespaces, nested blocks/properties, block IDs/references, assets, and existing user `AGENTS.md`/Codex config where relevant.
- Provide a cheap targeted check and an authoritative full Vault Rig check.
- Verify install twice, doctor, update simulation, retrieval commands, graph checks, and uninstall against fixtures.
- Verify canonical fixture content hashes remain unchanged by install/uninstall except fixtures explicitly used to test Codex write behavior.
- Make release validation runnable locally and in CI when a CI provider is later configured.

## Out of Scope

- Benchmark model quality.
- Require production/private vault content in tests.
- Add cross-platform environments not actually supportable by the implementation toolchain without evidence.

## Acceptance Cases

- One command produces pass/fail evidence for the supported Vault Rig lifecycle.
- A regression in path resolution, alias/context parsing, UUID checks, lifecycle idempotence, or ownership cleanup is caught by a fixture test.
- Fixture data is synthetic and safe to publish.
- Tests do not pass by weakening or deleting failing fixture expectations during normal Vault Rig operation.

## Constraints / Preservation

- The verification oracle must be independent of Codex semantic judgment.
- Keep fixtures small and purpose-built; do not create a giant synthetic brain.
- Do not require network access for core validation.

## Migration / Rollout

- This becomes the gate for tagging/releasing Vault Rig versions; exact CI hosting is a later repository choice.

## Validation

- Authoritative check runs all supported fixture scenarios from a clean temporary location and returns non-zero on failure; artifacts/logs identify the failing scenario.

## Assumptions

- Verification is part of the product: a portable Vault Rig installation is not complete until install/update/uninstall and graph invariants are reproducibly tested.

## Material Decisions

- Use stable verification entrypoints rather than forcing Codex/contributors to know individual test commands.

## Open Questions

- The first supported OS/runtime matrix should match the actual implementation choice and user environments; do not invent a portability promise before testing it.
