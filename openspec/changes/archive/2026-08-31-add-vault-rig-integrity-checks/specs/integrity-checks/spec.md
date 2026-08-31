## Purpose

Defines deterministic changed-file and graph-wide checks for high-confidence Logseq OG identity and reference invariants without restricting valid flexible graph behavior.

## ADDED Requirements

### Requirement: Changed and full verification modes are available
The system SHALL provide a changed-content fast path and an authoritative graph-wide path with reliable process exit status.

#### Scenario: Healthy graph is checked
- **WHEN** either supported check mode examines a healthy fixture
- **THEN** it exits successfully and reports no integrity failures

### Requirement: Persisted block IDs are valid and unique
Checks SHALL reject malformed supported persisted block IDs and duplicate UUIDs, reporting every known conflicting location.

#### Scenario: UUID appears twice
- **WHEN** the checked graph contains the same persisted UUID at two locations
- **THEN** the check exits non-zero and identifies both locations

### Requirement: Persisted block references resolve
Checks SHALL reject a block reference whose locally persisted target is expected but cannot be found.

#### Scenario: Block reference target is missing
- **WHEN** a checked file contains a supported block reference to an absent persisted target
- **THEN** the check exits non-zero and identifies the referring location and UUID

### Requirement: Referenced block deletion is detected when evidenced
Changed-content verification SHALL report deletion of a persisted block when available diff and graph evidence shows remaining references to that block.

#### Scenario: Referenced persisted block is deleted
- **WHEN** a change removes a persisted block that is still referenced in the graph
- **THEN** the changed-content check fails with deletion and reference evidence

### Requirement: Deterministic local asset references resolve
Checks SHALL reject broken local asset references when the target path can be resolved unambiguously under supported vault conventions.

#### Scenario: Local asset is missing
- **WHEN** a checked note references an unambiguously resolved local asset that does not exist
- **THEN** the check fails and reports the note location and resolved missing path

### Requirement: Controlled properties are opt-in
Property-value validation SHALL apply only to properties and allowed values explicitly configured by the vault or user.

#### Scenario: Unconfigured property has a novel value
- **WHEN** a note uses a property that is not configured as controlled
- **THEN** the check does not fail because of that property's vocabulary

### Requirement: Flexible page references remain valid
Checks MUST NOT fail merely because a page reference has no corresponding page file when Logseq OG permits that reference.

#### Scenario: New page reference has no file
- **WHEN** a checked note contains a syntactically supported page reference without a page file
- **THEN** the check does not report an integrity failure for absence alone

### Requirement: Verification never repairs graph files
All integrity checks SHALL be read-only and SHALL produce actionable machine-readable findings for callers, hooks, and CI.

#### Scenario: Integrity failure is found
- **WHEN** a check detects any supported failure
- **THEN** it reports evidence and exits non-zero without changing canonical graph files
