## Purpose

Provides deterministic Logseq-aware retrieval from canonical Markdown and Git while preserving enough source evidence for users and tools to verify every result.

## ADDED Requirements

### Requirement: Retrieval exposes a stable machine interface
Supported retrieval commands SHALL return JSON or NDJSON data, write diagnostics to standard error, and use non-zero exit status for failed requests.

#### Scenario: Requested page cannot be resolved
- **WHEN** resolve cannot identify one supported logical page
- **THEN** it returns a non-zero status and a machine-actionable diagnostic without emitting a false successful result

### Requirement: Logical pages resolve through vault conventions
Resolve SHALL map supported logical page names and reliably parsed aliases to canonical logical identity and actual source file using the detected vault descriptor.

#### Scenario: Logical name differs from filename
- **WHEN** a supported logical page name maps to an encoded or otherwise different filename
- **THEN** resolve returns the logical identity and actual source path

### Requirement: Exact graph evidence is searchable
Find SHALL locate supported literal text, page references, block references, persisted block UUIDs, properties, and task markers in configured knowledge files.

#### Scenario: Persisted block UUID is searched
- **WHEN** find receives a persisted UUID present in the vault
- **THEN** it returns the containing file, line, logical page, and block evidence

### Requirement: Matches can be expanded to block context
Context SHALL reconstruct supported Logseq block ancestry and requested children around a lexical match without returning only an isolated line.

#### Scenario: Nested block match is expanded
- **WHEN** context receives a match inside a nested block
- **THEN** the result includes the matching block and its ordered ancestors plus requested child depth

### Requirement: Pages and blocks can be inspected directly
Page and block retrieval SHALL return canonical source content and stable evidence for a resolvable logical page or persisted block UUID.

#### Scenario: Persisted block is requested
- **WHEN** block receives a unique persisted UUID
- **THEN** it returns that block's source location, content, properties, and supported context

### Requirement: Deterministic relationships are reported
Refs and backlinks SHALL report relationships derivable from canonical files and supported aliases without inventing links from semantic similarity.

#### Scenario: Page has explicit references
- **WHEN** backlinks is requested for a resolvable page
- **THEN** it returns explicit referring source locations with logical-page evidence

### Requirement: Git history is searchable
History SHALL use repository history to locate relevant introductions or changes for a supplied term, page, or source path.

#### Scenario: Term was introduced in prior history
- **WHEN** history receives a term present in an earlier commit
- **THEN** it returns the relevant commit and source evidence

### Requirement: Core retrieval works offline without a derived store
Core retrieval SHALL work with Logseq closed and MUST NOT require a persistent derived index, semantic service, MCP server, or live DataScript endpoint.

#### Scenario: Logseq is not running
- **WHEN** a supported file or Git retrieval command runs
- **THEN** it returns results from canonical Markdown or Git without a live Logseq dependency
