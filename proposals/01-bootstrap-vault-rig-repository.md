# Proposed OpenSpec Change: bootstrap-vault-rig-repository

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `bootstrap-vault-rig-repository`  
**Release target:** `0.1`  
**Depends on:** None

## Intent

Create the repository foundation for `vault-rig`, whose managed payload can be applied to existing Logseq OG vault repositories without making the `vault-rig` repository itself a knowledge vault.

## Current / Problem

The Vault Rig architecture exists as a design, but there is no dedicated `vault-rig` repository defining which files are portable payload, which files are development-only, or what ownership boundaries an installer must respect.

## Desired Behavior

The repository exposes a clear Vault Rig managed payload, development/test area, version metadata, and stable entrypoints so later changes can add installer, retrieval, validation, and Codex behavior without coupling them to one personal vault.

## In Scope

- Define top-level repository boundaries for the Vault Rig managed payload, development/test assets, documentation, and release metadata.
- Reserve a namespaced managed directory inside target vaults (for example `.vault-rig/`) for implementation-owned files.
- Define locations for the repository-local Codex Skill and Codex hook/config payload that later installer changes can manage.
- Document that target vault `pages/`, `journals/`, `assets/`, and `logseq/config.edn` are user/vault-owned, not Vault Rig-owned.
- Expose a single documented bootstrap/entry command location for later lifecycle operations.

## Out of Scope

- Implement retrieval commands, validation logic, DataScript integration, semantic indexing, or MCP.
- Modify any real vault.
- Choose a package registry or hosted distribution mechanism.

## Acceptance Cases

- A fresh clone clearly identifies Vault Rig-managed files versus target-vault-owned files.
- No Vault Rig managed payload path collides with canonical Logseq knowledge directories.
- The repository can evolve without requiring personal vault content to be committed into the `vault-rig` repository.
- A contributor can identify where installer payload, tests, Skills, hooks, and docs belong from repository documentation alone.

## Constraints / Preservation

- Markdown in target Logseq OG vaults remains canonical knowledge.
- Vault Rig core must be usable without Logseq DB, semantic indexing, or MCP.
- Avoid speculative infrastructure; only reserve boundaries needed by the known roadmap.

## Migration / Rollout

- Initial change only establishes repository structure; it does not install into existing vaults.

## Validation

- Repository structure can be checked by a deterministic layout test that fails on missing required Vault Rig boundaries or forbidden canonical-vault content.

## Assumptions

- The `vault-rig` repository will be version-controlled independently from individual vault repositories.

## Material Decisions

- Use one reusable `vault-rig` repository rather than copying an unstructured collection of files manually between vaults.
- Keep vault-owned knowledge and Vault Rig-owned implementation separate.

## Open Questions

- Repository name is fixed as `vault-rig`; the license remains a repository-owner decision.
