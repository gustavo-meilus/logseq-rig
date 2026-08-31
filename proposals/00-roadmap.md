# Vault Rig: Logseq OG + Codex Proposal Series

This series decomposes the `vault-rig` project into focused OpenSpec change contracts. It follows the supplied OpenSpec Brainstorming workflow: one clear intent per change, explicit scope and preservation rules, proportional rigor, and an approval gate before creating actual OpenSpec change artifacts.

## Current evidence and boundaries

- The target system is `vault-rig`, a reusable tooling and control layer installed into existing Logseq OG vault folders without changing the vault's canonical knowledge model.
- Canonical knowledge remains the existing Logseq OG Markdown under the vault's configured pages/journals directories.
- Git remains history and rollback.
- Codex is the reasoning/operator layer; deterministic scripts validate structure and route retrieval.
- Vault Rig core must not require Logseq DB, a vector database, MCP, or a second authoritative data store.
- The actual target vault has not been inspected in this proposal package. Vault-specific conventions therefore remain runtime-discovered or explicit configuration, not hardcoded assumptions.
- The OpenSpec CLI was not available in the current execution environment and no initialized OpenSpec project/store was supplied. In accordance with the brainstorming workflow, this package contains normalized contracts ready for approval rather than fabricated OpenSpec change artifacts.

## Recommended delivery waves

### Release 0.1 - Portable core

1. `bootstrap-vault-rig-repository`
2. `detect-logseq-og-vault`
3. `add-vault-rig-lifecycle`
4. `add-vault-rig-retrieval-core`
5. `add-vault-rig-integrity-checks`
6. `add-codex-vault-rig-integration`
7. `add-vault-rig-fixtures-and-release-validation`

This release is sufficient to install Vault Rig into multiple vaults, search and inspect the graph safely, edit under Codex with repository-local guidance, and verify graph integrity.

### Release 0.2 - Native structural query integration

8. `add-logseq-datascript-query-bridge`

This adds live Logseq OG structural queries and a versioned named-query library without replacing Markdown as the source of truth.

### Optional extensions - only after demonstrated need

9. `add-derived-semantic-retrieval`
10. `add-shared-mcp-adapter`

Semantic indexing and MCP are intentionally separate optional changes so they do not become mandatory dependencies of every vault.

## Dependency graph

```text
bootstrap-vault-rig-repository
        |
        +--> detect-logseq-og-vault
                 |
                 +--> add-vault-rig-lifecycle
                 |
                 +--> add-vault-rig-retrieval-core
                           |
                           +--> add-vault-rig-integrity-checks
                           |        |
                           |        +--> add-codex-vault-rig-integration
                           |                    |
                           |                    +--> add-vault-rig-fixtures-and-release-validation
                           |
                           +--> add-logseq-datascript-query-bridge
                           |
                           +--> add-derived-semantic-retrieval   [optional]
                           |
                           +--> add-shared-mcp-adapter           [optional; may also use DataScript bridge]
```

## Approval and OpenSpec handoff

Approve each contract independently. After approval, create the corresponding OpenSpec change in the initialized `vault-rig` repository and let the active OpenSpec schema/instructions determine artifact structure.

Typical CLI flow after an OpenSpec root exists:

```bash
openspec context --json
openspec new change "<change-name>"
openspec status --change "<change-name>" --json
openspec instructions <artifact-id> --change "<change-name>" --json
openspec validate "<change-name>" --strict
```

Do not hardcode a universal `proposal.md -> specs -> design -> tasks` pipeline; follow the resolved schema and artifact dependency graph.
