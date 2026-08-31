# Proposed OpenSpec Change: detect-logseq-og-vault

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `detect-logseq-og-vault`  
**Release target:** `0.1`  
**Depends on:** `bootstrap-vault-rig-repository`

## Intent

Add deterministic discovery of a target Logseq OG vault and its relevant on-disk conventions before any install, search, or mutation operation.

## Current / Problem

Logseq Vault Rig cannot safely assume `pages/`, `journals/`, page filename encoding, or journal filename format. Logseq OG configuration can change these conventions, and logical page names do not always equal filesystem paths.

## Desired Behavior

Given a target folder, Logseq Vault Rig either returns a normalized vault descriptor derived from Logseq configuration and filesystem evidence or fails clearly without modifying the folder.

## In Scope

- Detect whether a folder is plausibly a Logseq OG vault using repository evidence such as `logseq/config.edn` and configured knowledge directories.
- Resolve configured pages and journals directories instead of assuming defaults.
- Capture filename/page-name mode and journal filename format when available.
- Return a machine-readable descriptor for downstream commands.
- Expose diagnostics explaining missing or ambiguous vault prerequisites.

## Out of Scope

- Parse the entire Logseq graph into a second database.
- Infer aliases, backlinks, or block context.
- Modify `logseq/config.edn` automatically.
- Support Logseq DB graphs.

## Acceptance Cases

- Default-layout OG vaults are detected and normalized.
- Vaults with custom page/journal directories are reported with those actual directories.
- A non-Logseq folder is rejected without filesystem mutation.
- Malformed or unreadable relevant configuration produces an actionable diagnostic rather than silent fallback.
- Downstream tooling can consume the descriptor without reparsing configuration independently.

## Constraints / Preservation

- Vault detection must be read-only.
- Do not derive a page path from a logical page name without the vault descriptor/resolver layer.
- Unknown configuration must be surfaced rather than guessed when guessing can affect data integrity.

## Migration / Rollout

- Existing vaults require no migration; discovery reads their current layout.

## Validation

- Fixture vaults cover default layout, custom directories, custom journal format, non-vault folder, and malformed configuration.

## Assumptions

- The target is Logseq OG/file graphs, not the new DB graph format.

## Material Decisions

- Make configuration discovery a shared deterministic primitive used by installer, retrieval, and validator.

## Open Questions

- Whether all historical Logseq filename modes need first-release support should be decided from real target-vault inventory; unsupported modes must fail explicitly rather than corrupt paths.
