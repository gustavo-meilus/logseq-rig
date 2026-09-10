## Why

Some graphs rely on a property acting as a stable, human-assigned identifier (for example a `slug` or `ref` key) even though Logseq itself does not enforce uniqueness for arbitrary properties. Today the checker can only validate a property's allowed vocabulary (`controlled_properties`); it has no opt-in way to reject the same value being assigned twice.

## What Changes

- Extend `.logseq-rig/integrity.json` with an optional `unique_properties` list of property names.
- For each configured property, reject duplicate values across the graph with the machine-readable finding code `duplicate_property_value`, reporting every known conflicting location.
- In `check --changed`, surface a graph-wide collision when at least one conflicting occurrence is in a changed canonical Markdown file, including unchanged conflicting locations as related evidence; duplicates confined entirely to unchanged files are not surfaced.
- Leave properties not listed in `unique_properties` unrestricted, and validate malformed configuration the same way `controlled_properties` is validated today.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `integrity-checks`: adds opt-in duplicate-value detection for configured properties alongside the existing controlled-property and persisted-ID checks.

## Impact

Extends `logseq_rig/integrity.py` and its configuration loader only; no CLI surface, managed payload, or DataScript behavior changes. Unconfigured graphs see no behavior change.
