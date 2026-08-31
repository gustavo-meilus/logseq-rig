## Why

Logseq Vault Rig cannot safely operate on a folder until it knows that the folder is a Logseq OG vault and has resolved its actual pages, journals, filename, and journal-date conventions. Guessing these values risks incorrect reads or destructive writes.

## What Changes

- Add read-only detection of Logseq OG/file vaults from configuration and filesystem evidence.
- Return a normalized machine-readable vault descriptor for all downstream commands.
- Resolve configured knowledge directories and supported filename conventions rather than assuming defaults.
- Reject non-vaults, malformed configuration, and unsupported material conventions with actionable diagnostics and no mutation.

## Capabilities

### New Capabilities
- `vault-detection`: Detects supported Logseq OG vaults and exposes their normalized on-disk conventions.

### Modified Capabilities
- None.

## Impact

Depends on the repository foundation and becomes the shared discovery primitive for lifecycle, retrieval, and validation. Logseq DB graphs and full graph parsing remain outside scope.
