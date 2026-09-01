## ADDED Requirements

### Requirement: Legacy managed payloads migrate only with proven ownership
The update operation SHALL migrate a legacy managed payload to the active namespace only when its manifest, managed regions, and installer-owned files are valid and unchanged. It MUST report a no-write conflict for malformed, modified, ambiguous, or unowned legacy state.

#### Scenario: Clean legacy installation is updated
- **WHEN** update runs against a graph with one valid unchanged legacy ownership record
- **THEN** the active managed payload and ownership record replace the legacy managed payload without changing canonical graph content or user-owned files

#### Scenario: Legacy state has drifted
- **WHEN** update finds a legacy managed file, region, marker, or ownership record that cannot be proven unchanged
- **THEN** it reports the conflicting evidence and does not write either managed namespace

### Requirement: Interrupted migration is recoverable
An interrupted namespace migration SHALL leave durable migration diagnostics and MUST permit deterministic recovery or conflict reporting without rewriting canonical graph content.

#### Scenario: Migration is interrupted after destination state begins
- **WHEN** a filesystem failure interrupts a legacy migration after destination managed state is created
- **THEN** doctor identifies recoverable incomplete state and a subsequent update can complete or report a no-write conflict deterministically

## MODIFIED Requirements

### Requirement: Lifecycle changes are previewable
Every mutating lifecycle operation SHALL provide a deterministic dry-run that reports intended additions, updates, migrations, conflicts, and removals without changing the target.

#### Scenario: Install dry-run
- **WHEN** a user requests an install dry-run for a supported graph
- **THEN** the system reports the planned filesystem changes and leaves all files unchanged

### Requirement: Installation respects ownership boundaries
Installation SHALL write only declared Logseq Rig-managed files or bounded managed regions and MUST NOT rewrite canonical pages, journals, assets, or Logseq configuration.

#### Scenario: Install into an existing vault
- **WHEN** installation runs against a detected supported graph
- **THEN** the expected managed payload is installed while graph-owned knowledge and unrelated configuration remain byte-for-byte unchanged

### Requirement: Managed ownership is recorded
The system SHALL record the installed version and sufficient deterministic identity for every managed file or region to support drift detection, safe update, safe migration, and safe uninstall.

#### Scenario: Installation completes
- **WHEN** all planned managed files are installed successfully
- **THEN** an ownership record describes the installed version and managed content identities

### Requirement: Doctor reports lifecycle state without mutation
Doctor SHALL distinguish healthy, missing, locally modified, version-mismatched, legacy-migration-required, and incomplete managed state and SHALL NOT change the graph.

#### Scenario: Managed file is missing
- **WHEN** doctor finds a file listed in the ownership record is absent
- **THEN** it reports that file as missing and performs no repair

#### Scenario: Legacy managed state is detected
- **WHEN** doctor finds one valid legacy ownership record and no active ownership record
- **THEN** it reports that migration is required and performs no repair

### Requirement: Uninstall removes only proven managed state
Uninstall SHALL remove only files or bounded regions proven to be installer-owned and SHALL preserve pre-existing files and user-owned edits outside those boundaries.

#### Scenario: Vault has pre-existing root instructions
- **WHEN** uninstall removes a Logseq Rig-managed root-instruction region
- **THEN** all pre-existing instruction content remains intact

### Requirement: Failed lifecycle operations protect canonical knowledge
A failed or interrupted lifecycle operation MUST NOT leave canonical knowledge partially rewritten and SHALL leave sufficient diagnostics for recovery.

#### Scenario: Installation is interrupted
- **WHEN** an error occurs while applying managed payload files
- **THEN** canonical knowledge remains unchanged and the operation reports its incomplete managed state
