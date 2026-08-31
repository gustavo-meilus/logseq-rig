# Logseq Vault Rig Proposal Contracts for Logseq OG + Codex

This package contains a decomposed series of normalized OpenSpec change contracts for creating `logseq-vrig`, a reusable installable tooling and control layer for Logseq OG vault folders with Codex integration.

These are **not yet OpenSpec change artifacts**. The supplied `openspec-brainstorming` workflow requires explicit approval of each normalized contract before `openspec new change` is run. No initialized OpenSpec root/store was supplied and the OpenSpec CLI was not available in the current execution environment, so generating fake schema-specific artifacts would violate the workflow.

Start with [`00-roadmap.md`](00-roadmap.md).

## Files

- [`01-bootstrap-vault-rig-repository.md`](01-bootstrap-vault-rig-repository.md) - `bootstrap-vault-rig-repository` (0.1)
- [`02-detect-logseq-og-vault.md`](02-detect-logseq-og-vault.md) - `detect-logseq-og-vault` (0.1)
- [`03-add-vault-rig-lifecycle.md`](03-add-vault-rig-lifecycle.md) - `add-vault-rig-lifecycle` (0.1)
- [`04-add-vault-rig-retrieval-core.md`](04-add-vault-rig-retrieval-core.md) - `add-vault-rig-retrieval-core` (0.1)
- [`05-add-vault-rig-integrity-checks.md`](05-add-vault-rig-integrity-checks.md) - `add-vault-rig-integrity-checks` (0.1)
- [`06-add-codex-vault-rig-integration.md`](06-add-codex-vault-rig-integration.md) - `add-codex-vault-rig-integration` (0.1)
- [`07-add-vault-rig-fixtures-and-release-validation.md`](07-add-vault-rig-fixtures-and-release-validation.md) - `add-vault-rig-fixtures-and-release-validation` (0.1)
- [`08-add-logseq-datascript-query-bridge.md`](08-add-logseq-datascript-query-bridge.md) - `add-logseq-datascript-query-bridge` (0.2)
- [`09-add-derived-semantic-retrieval.md`](09-add-derived-semantic-retrieval.md) - `add-derived-semantic-retrieval` (optional)
- [`10-add-shared-mcp-adapter.md`](10-add-shared-mcp-adapter.md) - `add-shared-mcp-adapter` (optional)

## Recommended approval strategy

Approve the Release 0.1 contracts as a sequence, not as one giant scope. If a contract changes materially during review, update dependent contracts before creating their OpenSpec changes.

The optional semantic/MCP proposals should remain unapproved until a real retrieval/client requirement justifies them.
