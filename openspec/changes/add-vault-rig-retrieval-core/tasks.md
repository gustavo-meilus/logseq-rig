## 1. Source Model

- [ ] 1.1 Implement the shared streaming Logseq block parser for indentation, properties, page refs, block refs, persisted IDs, and source locations, then verify focused fixtures cover nested and malformed supported cases.
- [ ] 1.2 Implement logical page and alias resolution from the vault descriptor and parsed properties, then verify encoded filenames, namespaces, aliases, and ambiguity return expected evidence.

## 2. Command Contract

- [ ] 2.1 Add common JSON/NDJSON result and error envelopes to the command dispatcher, then verify stdout, stderr, and exit status remain machine-readable for success, absence, and ambiguity.
- [ ] 2.2 Implement status and resolve, then verify they work with Logseq closed on default and custom-layout fixtures.

## 3. File Retrieval

- [ ] 3.1 Implement find for literal text, page refs, block refs, persisted UUIDs, properties, and supported task markers, then verify results include file, line, logical page, and block evidence.
- [ ] 3.2 Implement context, page, and block inspection using the shared source model, then verify nested ancestry and requested child depth are preserved.
- [ ] 3.3 Implement refs and backlinks from explicit source relationships and aliases, then verify no semantic-only relationship is emitted.

## 4. History and Integration

- [ ] 4.1 Implement history by wrapping machine-readable Git commands, then verify a temporary repository reports the commit that introduced and changed a fixture term.
- [ ] 4.2 Run the retrieval acceptance fixtures through the public CLI, then verify every command works without a persistent index, live Logseq endpoint, semantic service, or MCP server.
