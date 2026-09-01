## MODIFIED Requirements

### Requirement: Live query availability is optional
The system SHALL detect whether a supported local Logseq OG query endpoint configured through the active Logseq Rig interface is available without making that endpoint a prerequisite for core commands.

#### Scenario: Logseq endpoint is unavailable
- **WHEN** a live query is requested while no supported endpoint is available
- **THEN** the query returns an explicit capability error and offline core commands remain usable

### Requirement: Endpoint authority is minimized
Endpoint credentials and local connection details MUST remain outside canonical notes and SHALL be exposed only through the active `LOGSEQ_RIG_*` query configuration to the query mechanism that requires them.

#### Scenario: Graph content is inspected
- **WHEN** canonical pages and journals are searched
- **THEN** they contain no bridge credentials introduced by Logseq Rig

#### Scenario: Vault content is inspected
- **WHEN** canonical pages and journals are searched
- **THEN** they contain no bridge credentials introduced by Logseq Rig
