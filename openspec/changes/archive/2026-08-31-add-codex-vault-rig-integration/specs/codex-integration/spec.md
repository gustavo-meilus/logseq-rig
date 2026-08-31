## Purpose

Provides the minimum repository-local Codex context and lifecycle controls needed to retrieve, edit, and verify Logseq OG knowledge safely.

## ADDED Requirements

### Requirement: Root instructions remain a concise operating contract
The managed root contract SHALL identify canonical knowledge, stable Logseq invariants, retrieval routing, editing boundaries, and the authoritative verification command without embedding detailed procedures.

#### Scenario: New Codex session reads root instructions
- **WHEN** Codex starts in an installed vault
- **THEN** it can identify the source of truth, retrieval entrypoint, edit boundaries, and completion check from bounded root context

### Requirement: One Skill provides progressive procedures
The installation SHALL provide one repository-local Logseq Vault Rig Skill that contains reusable retrieval and safe-edit procedures and delegates deterministic mechanics to Logseq Vault Rig commands.

#### Scenario: Logseq-aware procedure is needed
- **WHEN** a task matches the Logseq Vault Rig Skill
- **THEN** Codex can load the procedure without adding it to every session's root context

### Requirement: SessionStart reports bounded orientation
The SessionStart hook SHALL report detected vault state, Git state, available retrieval capabilities, and current integrity status without dumping graph content.

#### Scenario: Session starts in a healthy installed vault
- **WHEN** the SessionStart hook runs
- **THEN** it returns a bounded summary sufficient to choose supported retrieval and verification paths

### Requirement: Canonical edits trigger a bounded completion gate
The Stop hook SHALL run changed-content integrity verification when canonical graph files changed and MUST allow at most one repair continuation for the same failing completion attempt.

#### Scenario: Integrity check fails twice
- **WHEN** the Stop check fails after one repair continuation
- **THEN** the hook permits the turn to end while clearly reporting unresolved verification failure

### Requirement: Authority defaults are conservative
Managed Codex configuration SHALL scope writes to the workspace, preserve approval boundaries, and SHALL NOT select external web research for ordinary personal-knowledge queries unless explicitly requested.

#### Scenario: Task only reads vault knowledge
- **WHEN** Codex answers a local knowledge question
- **THEN** the configured workflow does not require mutation authority or external research

### Requirement: Optional review remains optional
Independent read-only review MAY be documented for high-risk semantic restructuring but SHALL NOT be required for routine Logseq Vault Rig use.

#### Scenario: Routine deterministic edit completes
- **WHEN** a routine edit passes the required graph checks
- **THEN** completion does not require a subagent or multi-agent workflow

### Requirement: Core operation does not depend on Logseq runtime
Codex integration SHALL remain usable with Logseq closed except for explicitly live-query capabilities.

#### Scenario: Logseq is closed
- **WHEN** Codex uses core retrieval or integrity commands
- **THEN** those operations remain available from canonical files and Git
