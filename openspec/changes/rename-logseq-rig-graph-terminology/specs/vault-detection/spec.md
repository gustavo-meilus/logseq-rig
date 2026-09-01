## MODIFIED Requirements

### Requirement: Detection is read-only
The system SHALL inspect a target folder for Logseq OG configuration and filesystem evidence without modifying that folder.

#### Scenario: Non-vault folder is inspected
- **WHEN** detection receives a folder that lacks sufficient Logseq OG evidence
- **THEN** it returns a non-zero result with a Graph-terminology actionable diagnostic and leaves the folder unchanged

### Requirement: Configured knowledge directories are resolved
The system SHALL report the actual configured pages and journals directories rather than assuming default names.

#### Scenario: Vault uses custom directories
- **WHEN** a supported graph configures non-default pages or journals directories
- **THEN** the graph descriptor contains those resolved directories

### Requirement: Relevant naming conventions are described
The graph descriptor SHALL include the supported page filename mode and journal filename format when they can affect downstream path resolution.

#### Scenario: Vault declares a custom journal format
- **WHEN** detection reads a supported custom journal filename format
- **THEN** the normalized graph descriptor exposes that format for downstream consumers

### Requirement: Descriptor is machine-readable and reusable
Successful detection SHALL return one normalized machine-readable graph descriptor sufficient for downstream lifecycle, retrieval, and validation commands.

#### Scenario: Downstream command consumes detection output
- **WHEN** a downstream command receives a successful graph descriptor
- **THEN** it can locate configured knowledge directories without reparsing graph configuration

### Requirement: Material ambiguity fails explicitly
Malformed, unreadable, or unsupported configuration that could affect data integrity MUST produce an actionable error rather than silently falling back to guessed values.

#### Scenario: Filename mode is unsupported
- **WHEN** the graph uses a filename mode the release does not support
- **THEN** detection fails before any downstream mutation and identifies the unsupported convention

### Requirement: Only Logseq OG file graphs are accepted
The detector SHALL reject Logseq DB graphs and other folder types that do not satisfy the supported Logseq OG file-graph contract.

#### Scenario: Target is a Logseq DB graph
- **WHEN** detection identifies a non-file Logseq DB graph
- **THEN** it reports the graph type as unsupported without mutation
