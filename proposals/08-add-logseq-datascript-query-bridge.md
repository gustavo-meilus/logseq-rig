# Proposed OpenSpec Change: add-logseq-datascript-query-bridge

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-logseq-datascript-query-bridge`  
**Release target:** `0.2`  
**Depends on:** `add-vault-rig-retrieval-core`

## Intent

Add an optional live bridge from the `vault-rig` interface to Logseq OG's runtime DataScript/Datalog capabilities for structural graph queries and reusable named closure queries.

## Current / Problem

Filesystem search is excellent for exact retrieval but awkward for relational questions such as parent/child constraints, property joins, task conditions, and transitive graph relationships. Logseq OG already maintains a parsed DataScript view while running, so rebuilding another structural database would duplicate capability.

## Desired Behavior

When Logseq OG's supported local API is available, `vault-rig query` can execute verified structural queries and return normalized evidence; when Logseq is closed, core file/Git retrieval still works and live-only queries fail clearly.

## In Scope

- Detect live Logseq OG API availability without making it a core install prerequisite.
- Expose `vault-rig query <named-query> [args]`.
- Support a versioned query library stored with the Logseq Vault Rig/vault configuration.
- Allow experimental raw query execution only through an explicit advanced surface if retained by design.
- Normalize query results with page/block UUID/source evidence where available.
- Define a promotion procedure: draft query -> run/inspect -> verify on fixtures/real cases -> register as named query.

## Out of Scope

- Replace Logseq DataScript with SQLite.
- Make Logseq runtime mandatory for file search, history, or integrity checking.
- Generate new Datalog for every repeated query when a verified named query exists.
- Write graph changes through the bridge in this change unless separately specified.

## Acceptance Cases

- With Logseq running and API configured, a named structural query returns expected fixture results.
- With Logseq unavailable, live-query commands return an explicit capability error while other `vault-rig` commands continue working.
- A verified closure query can be parameterized by logical page/project identity without hardcoded fixture paths.
- Named queries are version-controlled and testable.
- Query output identifies the evidence needed for Codex/human review.

## Constraints / Preservation

- Markdown remains canonical; DataScript is a live structural view.
- Reuse the existing Logseq OG API/community CLI when sufficient before writing a bespoke protocol layer.
- Keep API credentials/local endpoint handling out of canonical notes and follow least authority.

## Migration / Rollout

- Feature can be enabled per vault after core Logseq Vault Rig install; no knowledge migration.

## Validation

- Fixture/live integration tests where a Logseq test runtime is available; named queries also get expected-result fixtures. Core test suite must still pass without Logseq running.

## Assumptions

- Native Logseq structural querying precedes creation of another graph database.

## Material Decisions

- Named verified queries are durable Logseq Vault Rig assets; Codex composes new Datalog mainly for novel exploration, then promotes repeated useful queries.

## Open Questions

- The exact local API/CLI bridge should be selected during design against the current Logseq OG environment and supported user setup.
