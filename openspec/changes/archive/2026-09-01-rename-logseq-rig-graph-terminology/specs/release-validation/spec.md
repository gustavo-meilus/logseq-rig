## ADDED Requirements

### Requirement: Renamed interface and migration are release-validated
The authoritative release check SHALL validate the installed `logseq-rig` interface, a fresh graph installation, and a clean legacy managed-payload migration without network access or private graph content.

#### Scenario: Renamed release candidate is checked
- **WHEN** authoritative release validation runs for the renamed release candidate
- **THEN** it verifies the installed public command and both fresh-install and clean-migration lifecycle paths

## MODIFIED Requirements

### Requirement: Fixtures cover supported behavior
The project SHALL provide minimal synthetic graph fixtures for default layout, configured directories and journal format, aliases and namespaces, nested blocks and properties, persisted block references, assets, pre-existing managed-boundary configuration, and legacy managed-payload migration.

#### Scenario: Fixture corpus is inspected
- **WHEN** a contributor lists supported fixture scenarios
- **THEN** every supported behavior class maps to a small publishable synthetic fixture

### Requirement: Lifecycle round trip is verified
Full validation SHALL exercise install twice, doctor, update behavior, retrieval commands, integrity checks, and uninstall against clean disposable graph fixture copies, and SHALL exercise the supported legacy migration path.

#### Scenario: Lifecycle round trip succeeds
- **WHEN** full validation runs on a supported fixture
- **THEN** installation is idempotent, supported commands pass, legacy migration preserves required behavior, and uninstall removes only managed state
