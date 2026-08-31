# Proposed OpenSpec Change: add-derived-semantic-retrieval

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-derived-semantic-retrieval`  
**Release target:** `optional`  
**Depends on:** `add-vault-rig-retrieval-core`

## Intent

Add an optional disposable semantic retrieval layer for conceptually similar Logseq blocks only after deterministic retrieval proves insufficient for real user queries.

## Current / Problem

Exact search and DataScript cannot reliably find notes that discuss the same idea using different language. However, making embeddings/vector search part of the core Logseq Vault Rig would add state, dependencies, and retrieval ambiguity before evidence shows it is needed.

## Desired Behavior

A vault may opt into a rebuildable semantic index that returns candidate blocks with preserved Logseq context, while raw Markdown remains authoritative and exact/structural retrieval retains precedence.

## In Scope

- Index block-aware representations that include page identity, ancestor context, block text, selected properties/refs, and relevant children rather than isolated lines.
- Store all derived index state under a disposable/cache boundary excluded from canonical knowledge.
- Expose semantic search through the existing `vault-rig` interface as an explicit retrieval mode.
- Return source file/line/block UUID evidence for every candidate.
- Provide rebuild and delete-index operations.
- Measure whether semantic search improves known hard queries before enabling it by default in a vault.

## Out of Scope

- Make the semantic index authoritative.
- Write back inferred links automatically.
- Replace exact search or DataScript.
- Require cloud embeddings or a specific embedding provider without an explicit later decision.

## Acceptance Cases

- Deleting the entire semantic index does not lose knowledge and a rebuild restores capability.
- A semantic result always links back to canonical source evidence and block context.
- Exact identifiers/refs route to deterministic mechanisms rather than semantic search.
- A small evaluation set demonstrates material retrieval benefit before a vault enables the feature persistently.

## Constraints / Preservation

- Optional feature only.
- Derived data must be clearly separated from canonical Markdown.
- Privacy/network behavior must be explicit for whichever embedding implementation is later chosen.

## Migration / Rollout

- Opt-in per vault; can be disabled/uninstalled by deleting derived state and managed feature files.

## Validation

- Use a vault-specific retrieval evaluation set containing lexical-easy and semantic-hard questions; compare evidence quality and false positives; verify index rebuild determinism where applicable.

## Assumptions

- Semantic retrieval is an escalation layer, not the default route.

## Material Decisions

- Do not choose provider/model/storage implementation until there is measured need and an explicit privacy/operability decision.

## Open Questions

- What scale/query set proves semantic indexing is worth its maintenance cost must be determined from real vault usage.
