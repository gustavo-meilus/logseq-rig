## Context

See proposal.md and specs/retrieval-core/spec.md. Canonical Markdown and Git already contain the required evidence. The core must preserve Logseq block structure without introducing a persistent index.

## Goals / Non-Goals

**Goals:**
- Provide one command dispatcher and consistent result envelopes.
- Reuse vault detection for paths and naming conventions.
- Parse only supported Logseq Markdown semantics needed by the command contract.

**Non-Goals:**
- A full Markdown renderer, persistent database, fuzzy ranking service, or mutation API.
- Semantic interpretation of relationships not represented in source.

## Decisions

1. **Scan canonical files on demand.** Python standard-library traversal and streaming reads are sufficient for initial personal-vault scale. A persistent index is deferred until measured latency requires it.
2. **Use one small block parser.** It records source lines, indentation, parent/child relationships, properties, page refs, block refs, and persisted id values. All retrieval and later integrity checks consume the same parsed representation.
3. **Separate logical identity from paths.** A resolver builds page and alias identities from detected conventions and parsed properties; namespaces remain logical names, not directories.
4. **Use stable JSON envelopes and NDJSON for streams.** Every result carries command, descriptor version, source path, line, logical page, and available block evidence. Errors use structured codes on stderr and non-zero status.
5. **Delegate history to the Git CLI.** Git is already the authoritative history mechanism; wrapping its machine-readable output is smaller and more reliable than reading repository internals.

## Risks / Trade-offs

- [On-demand scans become slow for large vaults] → Measure representative latency; add a disposable index only after a threshold is demonstrated.
- [Markdown edge cases exceed the parser] → Fail or warn on unsupported structures and add regression fixtures from real examples.
- [Aliases are ambiguous] → Return explicit ambiguity with candidates instead of guessing.

## Migration Plan

Add commands incrementally behind the stable dispatcher, starting with status and resolve. Existing vaults need no data migration. Rollback removes tooling only.
