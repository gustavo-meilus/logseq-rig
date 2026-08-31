# release-validation Specification

## Purpose

Provides small public fixture vaults and stable checks that prove supported Logseq Vault Rig lifecycle, retrieval, integrity, and Codex integration behavior before release.

## Requirements

### Requirement: Fixtures cover supported behavior
The project SHALL provide minimal synthetic fixtures for default layout, configured directories and journal format, aliases and namespaces, nested blocks and properties, persisted block references, assets, and pre-existing managed-boundary configuration.

#### Scenario: Fixture corpus is inspected
- **WHEN** a contributor lists supported fixture scenarios
- **THEN** every supported behavior class maps to a small publishable synthetic fixture

### Requirement: Cheap and authoritative checks have stable entrypoints
The project SHALL expose one cheap targeted verification entrypoint and one authoritative full release-validation entrypoint.

#### Scenario: Contributor requests full validation
- **WHEN** the authoritative entrypoint runs
- **THEN** it exercises all supported fixture scenarios and returns a reliable pass or fail status

### Requirement: Lifecycle round trip is verified
Full validation SHALL exercise install twice, doctor, update behavior, retrieval commands, integrity checks, and uninstall against clean disposable fixture copies.

#### Scenario: Lifecycle round trip succeeds
- **WHEN** full validation runs on a supported fixture
- **THEN** installation is idempotent, supported commands pass, and uninstall removes only managed state

### Requirement: Canonical and user-owned content is protected
Validation SHALL compare content identities before and after lifecycle operations and SHALL fail if canonical fixture content or pre-existing user-owned configuration changes outside an explicit edit scenario.

#### Scenario: Installer changes canonical note
- **WHEN** lifecycle validation detects a canonical note hash changed unexpectedly
- **THEN** the authoritative check fails and identifies the modified file

### Requirement: Verification is independent and diagnostic
Release checks SHALL use deterministic expectations independent of Codex semantic judgment and SHALL identify the failing fixture and assertion.

#### Scenario: Retrieval regression occurs
- **WHEN** a supported retrieval result differs from its fixture expectation
- **THEN** validation exits non-zero and identifies the scenario and mismatch

### Requirement: Core validation is offline
The authoritative core validation SHALL run without private vault content or network access.

#### Scenario: Network is unavailable
- **WHEN** core release validation runs in a clean local environment
- **THEN** all non-live supported scenarios remain executable
