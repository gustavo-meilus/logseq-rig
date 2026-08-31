# Proposed OpenSpec Change: add-vault-rig-lifecycle

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-vault-rig-lifecycle`  
**Release target:** `0.1`  
**Depends on:** `bootstrap-vault-rig-repository`, `detect-logseq-og-vault`

## Intent

Provide safe `install`, `update`, `doctor`, and `uninstall` lifecycle operations that apply the managed Logseq Vault Rig payload to any detected Logseq OG vault without overwriting user knowledge or unrelated repository configuration.

## Current / Problem

Manual copying is error-prone across multiple vaults. Reapplying Logseq Vault Rig can overwrite local customization, create drift, or make uninstall impossible unless file ownership and merge boundaries are explicit.

## Desired Behavior

A user can point one lifecycle entrypoint at a vault, install Logseq Vault Rig repeatedly without duplicate effects, update managed files safely, diagnose drift, and remove only Logseq Vault Rig-owned state.

## In Scope

- Install namespaced Logseq Vault Rig files into the detected vault.
- Track the installed Logseq Vault Rig version and the set/hash of files managed by the installer using a minimal manifest or equivalent deterministic ownership record.
- Create missing repository-local Codex/Skill integration only within explicitly managed paths.
- Handle root `AGENTS.md` conservatively: create it when absent or use a bounded managed section/other non-destructive strategy when user content already exists.
- Provide `doctor` to report incompatible/missing/locally-modified managed files without changing the vault.
- Provide uninstall that removes only files/sections proven to be installer-owned.
- Support dry-run/plan output before changes.

## Out of Scope

- Rewrite canonical notes.
- Normalize existing Logseq config.
- Automatically commit or push Git changes.
- Silently discard local modifications to managed files.
- Install optional semantic or MCP components by default.

## Acceptance Cases

- Installing into a clean supported vault creates the expected managed payload and leaves canonical knowledge unchanged.
- Running install twice is idempotent.
- Update changes only managed content and reports conflicts when managed files were locally modified.
- Dry-run lists intended changes without changing files.
- Doctor distinguishes healthy, missing, modified, and version-mismatched managed state.
- Uninstall removes installed Logseq Vault Rig state while preserving pre-existing files and user-owned edits outside managed regions.
- An interrupted install cannot leave canonical knowledge partially rewritten.

## Constraints / Preservation

- Minimum blast radius: never take ownership of `pages/`, `journals/`, `assets/`, or existing user configuration wholesale.
- Lifecycle operations must be deterministic and suitable for review with Git diff.
- No network requirement for applying an already-available `vault-rig` checkout/package to a vault.
- Do not require every vault to share identical personal conventions.

## Migration / Rollout

- Existing vaults adopt Logseq Vault Rig in place; no note migration is required. Updates must be forward-compatible or fail with explicit instructions.

## Validation

- Run lifecycle tests against disposable fixture vaults; compare before/after file trees and content hashes; verify second install produces no change; verify uninstall restores pre-install user-owned state.

## Assumptions

- A small managed manifest is justified because safe update/uninstall across many vaults requires explicit ownership evidence.

## Material Decisions

- Prefer copy/snapshot-style managed payload with explicit ownership over Git submodules or a second nested repository unless later evidence proves otherwise.
- No automatic Git commit/push.

## Open Questions

- The exact merge mechanism for an existing root `AGENTS.md` should be selected during design from currently supported Codex instruction behavior; it must be deterministic and reversible.
