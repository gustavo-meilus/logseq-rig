## Context

See proposal.md and specs/vault-detection/spec.md. Detection is a trust boundary for every later mutation. Logseq configuration is EDN, but only a small set of scalar path and naming values is required for the first release.

## Goals / Non-Goals

**Goals:**
- Return one versioned descriptor shared by all commands.
- Fail closed on material ambiguity while accepting default and explicitly configured layouts.
- Keep detection read-only and dependency-free.

**Non-Goals:**
- A general EDN implementation or full graph parser.
- Support for Logseq DB graphs or guessed historical filename modes.

## Decisions

1. **Implement a narrow EDN tokenizer for required configuration keys.** It accepts the supported strings, keywords, maps, comments, and whitespace needed for Logseq configuration and rejects unsupported reader forms that affect required values. Regex-only extraction was rejected because comments and nested forms make silent misreads unsafe; a third-party EDN package was rejected until the narrow grammar proves insufficient.
2. **Emit a versioned JSON descriptor.** It contains the vault root, resolved pages and journals directories, supported page filename mode, journal filename format, evidence, and warnings. Paths are normalized relative to the vault root before use.
3. **Separate evidence collection from validation.** Filesystem and configuration facts are gathered first, then one validator either produces the descriptor or structured diagnostics. Downstream commands consume the descriptor API rather than reparsing files.
4. **Default only documented absent values.** Malformed explicit values, path escape, unreadable config, and unsupported naming modes fail; missing optional values may use supported Logseq OG defaults.

## Risks / Trade-offs

- [Narrow EDN support rejects valid uncommon configuration] → Report the exact unsupported form and extend fixtures only when a real vault requires it.
- [Symlink or relative-path escape] → Resolve paths and require configured knowledge directories to remain beneath the selected vault root.
- [Logseq conventions evolve] → Version the descriptor and make unsupported modes explicit.

## Migration Plan

Add detection as a read-only command and test it against disposable fixtures before any lifecycle command depends on it. Rollback removes the detector without altering vaults.
