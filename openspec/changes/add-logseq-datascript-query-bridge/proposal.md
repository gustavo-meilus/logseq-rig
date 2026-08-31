## Why

File search is sufficient for exact retrieval but inefficient for relational questions involving parents, children, properties, tasks, and transitive graph relationships. When Logseq OG is already running, its DataScript view can answer those questions without building another graph database.

## What Changes

- Add optional detection of a supported local Logseq OG query endpoint.
- Add `vault-rig query <named-query> [args]` backed by a versioned, testable named-query library.
- Normalize query results to stable page, block UUID, and source evidence where available.
- Define a draft, inspect, verify, and promote path for reusable queries.
- Fail live-only queries explicitly while preserving all offline core commands when Logseq is unavailable.

## Capabilities

### New Capabilities
- `datascript-query-bridge`: Provides optional read-only structural queries through Logseq OG's live DataScript view.

### Modified Capabilities
- None.

## Impact

Extends retrieval core without changing Markdown authority. The implementation will first evaluate an existing supported API or CLI; it will not add SQLite, require Logseq for core retrieval, expose credentials in notes, or write graph changes.
