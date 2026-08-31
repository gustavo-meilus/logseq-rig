# Proposed OpenSpec Change: add-vault-rig-integrity-checks

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-vault-rig-integrity-checks`  
**Release target:** `0.1`  
**Depends on:** `add-vault-rig-retrieval-core`

## Intent

Add deterministic `vault-rig check --changed` and `vault-rig check --all` verification so Codex edits cannot claim completion while known Logseq OG structural invariants are broken.

## Current / Problem

For this repository Markdown is the database. Generic linting is insufficient, while model self-review is too weak for invariants such as persisted UUID uniqueness and block-reference targets.

## Desired Behavior

Vault Rig can cheaply validate changed graph content during iteration and run an authoritative graph-wide check for high-risk operations, producing actionable machine-readable failures.

## In Scope

- Detect duplicate persisted `id::` UUIDs.
- Detect `((uuid))` block references whose persisted target cannot be found when the target is expected to be locally persisted.
- Detect malformed persisted block IDs supported by the selected OG conventions.
- Detect broken local asset references where deterministically resolvable.
- Detect accidental deletion of referenced blocks within the diff/graph evidence available.
- Support explicit controlled-property validation only for properties configured by a vault/user as controlled.
- Support a changed-files fast path and graph-wide full path.
- Report suspicious mass mutation relative to the requested/declared scope when the lifecycle/task supplies such scope.

## Out of Scope

- Police prose style, tag vocabulary, or every new page reference.
- Reject flexible Logseq behavior that is not an explicit invariant.
- Prove semantic correctness of note consolidation.
- Automatically repair failures without Codex/user review.

## Acceptance Cases

- A fixture with duplicate UUIDs fails with both locations identified.
- A fixture with a missing persisted block-ref target fails with the referring location.
- A healthy fixture passes both changed and full checks.
- Unknown/new page references do not fail merely because no page file exists.
- Controlled-property validation is opt-in and does not invent a global taxonomy.
- Exit status is reliable for hooks/CI.

## Constraints / Preservation

- Verification logic must be deterministic and independent of the model that made the edit.
- Checks should be strong enough to protect identity/integrity without making Logseq less flexible.
- The validator must never modify canonical graph files.

## Migration / Rollout

- Existing vaults can run the full check before enabling automatic Stop-hook enforcement. Pre-existing failures are reported rather than silently rewritten.

## Validation

- Unit/fixture tests for each supported invariant; full fixture-vault run; regression fixtures added whenever a real failure is found.

## Assumptions

- Knowledge Markdown changes are data changes, so the software-harness pattern of skipping "docs-only" verification does not apply to `pages/` or `journals/`.

## Material Decisions

- Use deterministic evidence before LLM review.
- Start with high-confidence invariants and add checks only when a real failure/risk earns them.

## Open Questions

- Whether target vaults use additional custom UUID/property conventions requires vault-specific discovery/configuration.
