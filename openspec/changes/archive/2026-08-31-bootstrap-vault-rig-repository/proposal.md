## Why

Logseq Vault Rig needs a repository foundation that separates its reusable managed payload from development assets and from every target vault's canonical Logseq Markdown. Establishing those ownership boundaries first prevents later lifecycle and tooling work from coupling to one personal vault.

## What Changes

- Define the repository areas for managed payload, development and test assets, documentation, version metadata, and stable entrypoints.
- Reserve a namespaced managed area inside target vaults while explicitly excluding vault-owned knowledge and configuration paths.
- Define locations for later Codex Skill, hook, and configuration payloads without implementing those features yet.
- Add a deterministic repository-layout check.

## Capabilities

### New Capabilities
- `repository-foundation`: Defines Logseq Vault Rig repository boundaries, target-vault ownership boundaries, and the stable bootstrap entrypoint.

### Modified Capabilities
- None.

## Impact

Creates the initial project layout and documentation contract. It does not modify a real vault, choose a distribution registry, or add retrieval, validation, DataScript, semantic, or MCP behavior.
