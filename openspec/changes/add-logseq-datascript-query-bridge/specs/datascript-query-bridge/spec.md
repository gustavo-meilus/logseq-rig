## Purpose

Adds an optional read-only bridge to Logseq OG's live DataScript view for relational queries while retaining Markdown as canonical knowledge.

## ADDED Requirements

### Requirement: Live query availability is optional
The system SHALL detect whether a supported local Logseq OG query endpoint is available without making that endpoint a prerequisite for core Vault Rig commands.

#### Scenario: Logseq endpoint is unavailable
- **WHEN** a live query is requested while no supported endpoint is available
- **THEN** the query returns an explicit capability error and offline core commands remain usable

### Requirement: Named structural queries are executable
The query interface SHALL execute version-controlled named queries with supplied arguments and SHALL NOT require callers to generate new Datalog for repeated supported questions.

#### Scenario: Named closure query runs
- **WHEN** a caller invokes a verified named closure query with a logical project identity
- **THEN** the system returns the expected related graph entities without hardcoded fixture paths

### Requirement: Query results preserve evidence
Live query results SHALL be normalized with logical page, block UUID, and canonical source evidence when the endpoint provides enough information to resolve them.

#### Scenario: Query returns blocks
- **WHEN** a named query returns supported Logseq blocks
- **THEN** each normalized result includes stable evidence sufficient for human or Codex review

### Requirement: Named queries have a promotion path
The project SHALL define a draft, inspect, verify, and register procedure before an exploratory query becomes a durable named query.

#### Scenario: Experimental query is proposed for reuse
- **WHEN** a draft query repeatedly answers a supported question
- **THEN** it is added to the named library only after expected results are verified

### Requirement: Bridge is read-only
The DataScript bridge SHALL NOT mutate canonical graph data in this change.

#### Scenario: Caller attempts a write operation
- **WHEN** a request would change graph state through the bridge
- **THEN** the operation is unavailable or rejected

### Requirement: Endpoint authority is minimized
Endpoint credentials and local connection details MUST remain outside canonical notes and SHALL be exposed only to the query mechanism that requires them.

#### Scenario: Vault content is inspected
- **WHEN** canonical pages and journals are searched
- **THEN** they contain no bridge credentials introduced by Vault Rig

### Requirement: Core behavior survives bridge removal
Disabling or uninstalling the bridge SHALL leave canonical Markdown and all core file and Git retrieval behavior intact.

#### Scenario: Bridge is removed
- **WHEN** the optional bridge is disabled or uninstalled
- **THEN** core retrieval continues to operate and no knowledge migration is required
