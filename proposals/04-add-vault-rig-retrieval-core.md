# Proposed OpenSpec Change: add-vault-rig-retrieval-core

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-vault-rig-retrieval-core`  
**Release target:** `0.1`  
**Depends on:** `detect-logseq-og-vault`

## Intent

Add a small stable `vault-rig` command interface for deterministic Logseq-aware retrieval from raw Markdown and Git without requiring Logseq to be running.

## Current / Problem

Generic file search loses Logseq semantics: logical page identity can differ from filenames, aliases can represent the same page, and a matching block often needs parent/child context to be meaningful. Codex needs stable structured retrieval instead of repeatedly improvising shell searches.

## Desired Behavior

From any installed vault, Codex or a human can call stable machine-readable commands to inspect graph status, resolve pages, search exact text/refs/properties/tasks, recover block context, inspect backlinks/refs where deterministically derivable, and search Git history.

## In Scope

- Implement the initial command contract: `vault-rig status`, `vault-rig resolve`, `vault-rig find`, `vault-rig context`, `vault-rig page`, `vault-rig block`, `vault-rig refs`, `vault-rig backlinks`, and `vault-rig history` where support is deterministic from files/Git.
- Use the vault descriptor from `detect-logseq-og-vault`.
- Return JSON/NDJSON for machine-facing data and errors on stderr with non-zero exit codes.
- Preserve source evidence: logical page, file, line, block UUID when present, properties, ancestors/children when requested.
- Use cheap exact/lexical search before semantic inference.
- Treat page aliases as alternate identities when they can be reliably parsed from OG properties.

## Out of Scope

- Semantic/vector search.
- Live DataScript/Datalog queries.
- Editing/mutation commands beyond what is required for internal tests.
- A new authoritative index or database.

## Acceptance Cases

- `vault-rig resolve "<logical page>"` returns the canonical logical identity and actual file when resolvable.
- `vault-rig find` can locate exact page references, block references, persisted `id::` UUIDs, selected properties, tasks, and literal text.
- `vault-rig context` expands a lexical hit into its Logseq block ancestry and children rather than returning an isolated line.
- Results include enough stable evidence for a human or Codex to reopen the source.
- `vault-rig history` can use Git to locate when a term/page was introduced or changed.
- Commands work with Logseq closed.

## Constraints / Preservation

- Raw Markdown remains authoritative.
- Do not silently equate logical namespaces with filesystem directories.
- Do not build a derived persistent index in the core change.
- Favor standard OS/Git capabilities and a small parser over broad dependencies unless evidence requires more.

## Migration / Rollout

- No graph migration; commands operate against existing files.

## Validation

- Fixture tests cover aliases, namespaces, nested block context, properties, UUID refs, custom vault directories, and Git history. Golden JSON/NDJSON outputs are suitable where stable.

## Assumptions

- The first retrieval ladder is known location -> lexical/filesystem retrieval -> later structural DataScript -> Codex synthesis -> optional semantic retrieval.

## Material Decisions

- Expose a stable `vault-rig` interface so Codex does not need to know underlying `rg`, parser, or Git command details.

## Open Questions

- Exact supported task markers/property parsing variants should follow observed OG files/fixtures rather than be guessed beyond documented forms.
