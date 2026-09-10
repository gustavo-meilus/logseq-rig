## ADDED Requirements

### Requirement: Configured unique properties reject duplicate values
Property-value uniqueness validation SHALL apply only to properties explicitly configured as unique, and SHALL reject the same value occurring more than once across the graph, reporting every known conflicting location.

#### Scenario: Configured property value repeats
- **WHEN** a checked graph assigns the same value to a property configured as unique at two locations
- **THEN** the check exits non-zero and identifies both locations

#### Scenario: Unconfigured property repeats a value
- **WHEN** a note reuses a value for a property that is not configured as unique
- **THEN** the check does not fail because of that repetition

### Requirement: Unique-property collisions are scoped like other changed-mode duplicates
Changed-content verification SHALL report a graph-wide unique-property collision when at least one conflicting occurrence is in a changed canonical Markdown file, including unchanged conflicting locations as related evidence, and SHALL NOT surface a collision confined entirely to unchanged files.

#### Scenario: Collision is confined to unchanged files
- **WHEN** every location of a duplicated configured-property value is outside the changed-file selection
- **THEN** `check --changed` does not report that collision

#### Scenario: Collision has at least one changed occurrence
- **WHEN** at least one location of a duplicated configured-property value is a changed canonical Markdown file
- **THEN** `check --changed` reports the collision and lists every known location, including unchanged ones, as related evidence
