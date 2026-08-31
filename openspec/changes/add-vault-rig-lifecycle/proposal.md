## Why

Manual payload copying cannot provide safe repeatable installation, updates, drift diagnosis, or uninstall across multiple vaults. Vault Rig needs explicit ownership evidence so it never overwrites canonical knowledge or unrelated user configuration.

## What Changes

- Add `install`, `update`, `doctor`, and `uninstall` lifecycle operations for detected vaults.
- Track the installed version and managed file hashes in a minimal ownership manifest.
- Provide deterministic dry-run output before mutations.
- Preserve locally modified managed files and pre-existing user content, including root instructions, by reporting conflicts instead of overwriting them.
- Make repeated installation idempotent and interrupted operations safe for canonical knowledge.

## Capabilities

### New Capabilities
- `vault-lifecycle`: Safely plans, installs, updates, diagnoses, and removes the Vault Rig managed payload.

### Modified Capabilities
- None.

## Impact

Depends on repository foundation and vault detection. It adds managed state under Vault Rig-owned paths but never takes ownership of pages, journals, assets, Logseq configuration, Git history, or optional semantic/MCP components.
