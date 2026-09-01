## MODIFIED Requirements

### Requirement: Root instructions remain a concise operating contract
The managed root contract SHALL identify canonical graph knowledge, stable Logseq invariants, retrieval routing, editing boundaries, and the authoritative verification command without embedding detailed procedures.

#### Scenario: New Codex session reads root instructions
- **WHEN** Codex starts in an installed graph
- **THEN** it can identify the source of truth, retrieval entrypoint, edit boundaries, and completion check from bounded root context

### Requirement: One Skill provides progressive procedures
The installation SHALL provide one repository-local Logseq Rig Skill that contains reusable retrieval and safe-edit procedures and delegates deterministic mechanics to Logseq Rig commands.

#### Scenario: Logseq-aware procedure is needed
- **WHEN** a task matches the Logseq Rig Skill
- **THEN** Codex can load the procedure without adding it to every session's root context

### Requirement: SessionStart reports bounded orientation
The SessionStart hook SHALL report detected graph state, Git state, available retrieval capabilities, and current integrity status without dumping graph content.

#### Scenario: Session starts in a healthy installed graph
- **WHEN** the SessionStart hook runs
- **THEN** it returns a bounded summary sufficient to choose supported retrieval and verification paths

#### Scenario: Session starts in a healthy installed vault
- **WHEN** the SessionStart hook runs
- **THEN** it returns a bounded summary sufficient to choose supported retrieval and verification paths

### Requirement: Optional review remains optional
Independent read-only review MAY be documented for high-risk semantic restructuring but SHALL NOT be required for routine Logseq Rig use.

#### Scenario: Routine deterministic edit completes
- **WHEN** a routine edit passes the required graph checks
- **THEN** completion does not require a subagent or multi-agent workflow
