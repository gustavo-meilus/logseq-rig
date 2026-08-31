## Why

Generic Codex behavior can flatten Logseq block structure, infer unsafe paths, and omit graph verification. A small repository-local operating contract can route work through deterministic Vault Rig commands without loading a Logseq manual into every session.

## What Changes

- Add a concise managed root operating contract for source of truth, retrieval routing, editing boundaries, and completion checks.
- Add one progressively disclosed `vault-rig` Skill rather than multiple speculative Skills.
- Add bounded SessionStart orientation and a Stop completion gate that runs changed-file integrity checks after canonical edits, with at most one repair continuation.
- Add a conservative workspace-scoped Codex configuration baseline and optional read-only review guidance for high-risk semantic restructuring.

## Capabilities

### New Capabilities
- `codex-integration`: Provides minimum repository-local Codex instructions, Skill routing, lifecycle hooks, and authority defaults for safe Vault Rig use.

### Modified Capabilities
- None.

## Impact

Depends on retrieval and integrity-check capabilities and is installed through the lifecycle ownership model. Exact Codex keys and hook interfaces will be verified against the installed release during implementation; semantic indexing, MCP, automatic Git operations, and mandatory subagents remain excluded.
