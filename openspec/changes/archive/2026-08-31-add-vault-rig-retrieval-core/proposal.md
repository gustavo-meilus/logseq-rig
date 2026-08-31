## Why

Generic file search loses Logseq concepts such as logical page identity, aliases, block ancestry, and persisted block references. Codex and humans need one deterministic retrieval interface that preserves source evidence without requiring Logseq to run or introducing another authoritative store.

## What Changes

- Add stable `status`, `resolve`, `find`, `context`, `page`, `block`, `refs`, `backlinks`, and `history` command behavior where file and Git evidence is deterministic.
- Return JSON or NDJSON results with file, line, logical page, properties, and block UUID/context evidence when available.
- Resolve aliases and page identities through the shared vault descriptor rather than filename guesses.
- Keep exact and lexical retrieval ahead of later structural or semantic escalation.

## Capabilities

### New Capabilities
- `retrieval-core`: Provides deterministic Logseq-aware file and Git retrieval through the stable Logseq Vault Rig command interface.

### Modified Capabilities
- None.

## Impact

Depends on vault detection. It adds a small parser and command surface, but no persistent index, semantic search, live DataScript dependency, or graph mutation commands.
