## ADDED Requirements

### Requirement: Controlled-property configuration survives managed namespace migration
When a clean legacy controlled-property configuration is the only recognized configuration, migration SHALL make the same rules available from the active managed namespace without deleting user-owned legacy configuration. Conflicting source and destination configurations MUST produce a no-write conflict.

#### Scenario: Clean legacy configuration is present
- **WHEN** a graph with a valid legacy controlled-property configuration is migrated and the active configuration is absent
- **THEN** subsequent integrity checks enforce the same controlled-property rules from the active namespace

#### Scenario: Configuration namespaces disagree
- **WHEN** valid legacy and active controlled-property configurations both exist with different contents
- **THEN** migration reports a conflict and does not overwrite either configuration

## MODIFIED Requirements

### Requirement: Deterministic local asset references resolve
Checks SHALL reject broken local asset references when the target path can be resolved unambiguously under supported graph conventions.

#### Scenario: Local asset is missing
- **WHEN** a checked note references an unambiguously resolved local asset that does not exist
- **THEN** the check fails and reports the note location and resolved missing path

### Requirement: Controlled properties are opt-in
Property-value validation SHALL apply only to properties and allowed values explicitly configured by the graph or user.

#### Scenario: Unconfigured property has a novel value
- **WHEN** a note uses a property that is not configured as controlled
- **THEN** the check does not fail because of that property's vocabulary
