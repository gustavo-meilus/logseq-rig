## Why

The project currently exposes Obsidian-style `vault` terminology through its repository identity, public commands, managed payload, and contracts even though it operates on Logseq graphs. Renaming the active product to Logseq Rig and using Graph terminology corrects that mismatch without weakening the lifecycle ownership guarantees for installed graphs.

## What Changes

- **BREAKING** Rename the distribution, repository, console command, Python package, managed namespace, installed Skill, environment variables, and active product copy from the `logseq-vrig`/`vault-rig` family to the `logseq-rig`/Graph family.
- **BREAKING** Rename public descriptor and diagnostic terminology from Vault to Graph while retaining serialized descriptor compatibility where its fields do not change.
- Migrate a clean, ownership-proven legacy managed installation when the new lifecycle update command runs; surface ambiguous, modified, or interrupted state as a no-write conflict or recoverable migration state.
- Preserve canonical graph content, user-owned configuration and instructions, and existing Logseq detection, retrieval, integrity, and DataScript behavior.
- Update active specifications, tests, fixtures, documentation, release guidance, and external repository naming. Preserve archived OpenSpec and stale proposal history as historical records.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `repository-foundation`: identify the renamed project boundaries and graph-owned content boundaries.
- `vault-detection`: expose detected Logseq locations using Graph terminology and diagnostics.
- `vault-lifecycle`: install, update, diagnose, migrate, recover, and uninstall the renamed managed payload without taking ownership of user files.
- `retrieval-core`: retain retrieval behavior while using the renamed descriptor and graph terminology.
- `integrity-checks`: preserve integrity behavior and controlled-property configuration across the managed namespace migration.
- `datascript-query-bridge`: retain read-only bridge behavior while using renamed configuration and graph wording.
- `codex-integration`: install the renamed Skill and hooks with the same bounded retrieval and integrity guarantees.
- `release-validation`: validate fresh installation and legacy migration using graph fixtures and the renamed public interface.

## Impact

- Affects the `vault_rig` package, packaging metadata, payload, fixtures, tests, current specifications, documentation, local clone/remote guidance, and release workflow.
- Existing `vault-rig` distribution users must install `logseq-rig` and run its update command before removing the old distribution.
- No runtime dependencies, Logseq protocol changes, canonical graph migrations, or Graph-write capabilities are introduced.
