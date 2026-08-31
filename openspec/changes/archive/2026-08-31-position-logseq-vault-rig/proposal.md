## Why

The current README leads with managed-directory implementation details and says Git history is planned, although the CLI and retrieval contract already provide `history`. The public repository has no description or topics, so its existing file-first control and integrity boundary is difficult to discover.

## What Changes

- Present Logseq Vault Rig consistently as a stdlib-only local control layer for AI-assisted Logseq OG graphs where Markdown and Git remain authoritative.
- Update README and package descriptions to describe implemented Markdown/Git retrieval, bounded Codex setup, and deterministic integrity checks; remove stale roadmap language.
- State the public promise: "Agents can work here. Markdown stays in charge." Define graph drift once with supported concrete examples.
- Set GitHub repository metadata to the approved description and topics.
- Make the OG-only, local/file-first boundary and deferred semantic retrieval/MCP explicit.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is a documentation and repository-metadata change; it does not change product behavior.

## Impact

- Affected surfaces: `README.md`, `pyproject.toml`, any conflicting public documentation, and GitHub repository metadata.
- No code, CLI, managed-payload, graph-format, DataScript, dependency, repository-name, package-name, or command-name change.
