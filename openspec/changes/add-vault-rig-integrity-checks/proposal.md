## Why

In a Logseq OG vault, Markdown is the database: duplicate persisted UUIDs and broken block or asset references are data-integrity failures that generic linting and model self-review cannot reliably prevent.

## What Changes

- Add `vault-rig check --changed` for iteration and `vault-rig check --all` for authoritative graph-wide verification.
- Detect duplicate or malformed persisted block IDs, missing locally persisted block-reference targets, deterministically broken local assets, and evidenced deletion of referenced blocks.
- Support explicitly configured controlled-property validation without imposing a global taxonomy.
- Produce actionable machine-readable failures and reliable exit statuses without modifying graph files.

## Capabilities

### New Capabilities
- `integrity-checks`: Deterministically verifies supported Logseq identity, reference, asset, and configured-property invariants.

### Modified Capabilities
- None.

## Impact

Builds on retrieval primitives and supplies the completion oracle for hooks and release validation. It intentionally does not police prose, flexible page references, or semantic correctness.
