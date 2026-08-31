## 1. Configuration Reader

- [ ] 1.1 Implement the narrow EDN tokenizer for required Logseq path and naming values, then verify fixtures cover supported maps, strings, keywords, comments, malformed input, and rejected reader forms.
- [ ] 1.2 Define the versioned vault descriptor and structured diagnostics, then verify JSON serialization is stable and contains no absolute path outside the selected vault.

## 2. Detection

- [ ] 2.1 Collect Logseq OG filesystem and config evidence without writes, then verify before/after file-tree hashes match for default, custom, non-vault, and malformed fixtures.
- [ ] 2.2 Resolve configured pages and journals directories plus supported page and journal naming conventions, then verify default and custom-layout descriptors match expected JSON.
- [ ] 2.3 Reject path escapes, Logseq DB graphs, unsupported filename modes, and material ambiguity before downstream use, then verify each case returns a distinct non-zero diagnostic code.

## 3. Command Integration

- [ ] 3.1 Expose detection through the canonical command dispatcher and make downstream code consume the descriptor rather than reparse config, then verify CLI success and failure outputs in unittest.
