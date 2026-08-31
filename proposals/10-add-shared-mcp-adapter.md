# Proposed OpenSpec Change: add-shared-mcp-adapter

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-shared-mcp-adapter`  
**Release target:** `optional`  
**Depends on:** `add-vault-rig-retrieval-core`

## Intent

Expose the already-controlled `vault-rig` capabilities through an optional MCP adapter when the same vault needs to be queried by clients beyond Codex CLI.

## Current / Problem

Codex can call local scripts directly, so an MCP server adds unnecessary tool/context/operational surface for Codex-only use. It becomes valuable only when ChatGPT, other agents, or remote-capable clients need the same structured vault interface.

## Desired Behavior

A vault may opt into an MCP server that delegates to the same `vault-rig` retrieval/validation primitives, exposes a deliberately small tool set, and applies narrower write authority than read authority.

## In Scope

- Expose selected read tools such as resolve/find/context/page/block/backlinks/query using existing `vault-rig` semantics.
- Keep write tools absent by default or scoped to explicit namespaces/operations with read-before-write safeguards if a later approved contract enables them.
- Reuse the same vault discovery, validation, and named-query implementations rather than creating a second knowledge model.
- Document client configuration and capability/approval boundaries.
- Provide health/version information so clients can detect mismatched Logseq Vault Rig versions.

## Out of Scope

- Make MCP mandatory for Codex CLI.
- Expose unrestricted filesystem or shell access through the server.
- Reimplement Logseq parsing/query semantics independently from `vault-rig`.
- Automatically expose private vaults over a network.

## Acceptance Cases

- The MCP adapter can answer a supported read query with the same canonical evidence as the equivalent `vault-rig` command.
- Stopping/removing MCP does not affect local Codex CLI use or canonical notes.
- Default MCP configuration cannot mutate the vault unless an explicit writable feature is separately enabled.
- Tool descriptions remain small and do not expose redundant overlapping capabilities.

## Constraints / Preservation

- Optional, least-authority extension.
- Local-only by default unless a separate security/network decision authorizes otherwise.
- No duplicate authoritative store or parser.

## Migration / Rollout

- Opt-in per vault/client after core Logseq Vault Rig is installed.

## Validation

- Contract tests compare MCP outputs with underlying `vault-rig` outputs; permission tests verify write operations are absent/denied by default; uninstall leaves core Logseq Vault Rig untouched.

## Assumptions

- CLI first, MCP later.

## Material Decisions

- Use MCP only to share an already-stable interface across clients, not as the internal architecture of Logseq Vault Rig.

## Open Questions

- Which external clients need MCP and whether any writes are required are intentionally unresolved until a concrete use case exists.
