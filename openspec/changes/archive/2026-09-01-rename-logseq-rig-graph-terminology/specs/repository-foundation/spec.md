## RENAMED Requirements

- FROM: `### Requirement: Repository remains independent of personal vaults`
- TO: `### Requirement: Repository remains independent of personal graphs`

## MODIFIED Requirements

### Requirement: Repository areas have explicit ownership
The repository SHALL identify the locations for Logseq Rig-managed payload, development and test assets, documentation, version metadata, and stable entrypoints, and SHALL distinguish them from content owned by target graphs.

#### Scenario: Contributor inspects a fresh clone
- **WHEN** a contributor reads the repository documentation and layout
- **THEN** each supported kind of payload, test, Skill, hook, and documentation has one identified location and ownership using the active Logseq Rig and Graph terminology

### Requirement: Managed payload does not own canonical knowledge
The managed payload SHALL use a namespaced target-graph boundary and MUST NOT claim ownership of configured pages, journals, assets, or Logseq configuration.

#### Scenario: Managed paths are compared with a target graph
- **WHEN** the payload layout is validated against canonical Logseq knowledge paths
- **THEN** no managed payload path overlaps or requires canonical knowledge content

#### Scenario: Managed paths are compared with a target vault
- **WHEN** the payload layout is validated against canonical Logseq knowledge paths
- **THEN** no managed payload path overlaps or requires canonical knowledge content

### Requirement: Repository remains independent of personal graphs
The repository SHALL support development and distribution without requiring personal graph content to be committed.

#### Scenario: Repository is prepared for development
- **WHEN** a fresh clone is validated
- **THEN** all required project assets are present without content from a personal graph

### Requirement: Layout is deterministically verifiable
The repository SHALL expose a deterministic check that fails when a required boundary is missing or forbidden canonical-graph content appears in a managed project area.

#### Scenario: Required boundary is missing
- **WHEN** the layout check runs without a required project boundary
- **THEN** it exits non-zero and identifies the missing boundary
