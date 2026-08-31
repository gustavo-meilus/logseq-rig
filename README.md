# Logseq Vault Rig

**Agents can work here. Markdown stays in charge.**

Logseq Vault Rig is a stdlib-only local control layer for Logseq OG graphs.
It discovers a graph's real file conventions, retrieves exact evidence from
Markdown and Git, installs a bounded Codex layer, and checks graph integrity
without introducing a second knowledge store.

Editing a Logseq graph safely is not the same as editing arbitrary Markdown.
Graph drift is a change that looks reasonable as Markdown but breaks something
Logseq depends on: a persisted block identity, block reference, asset path,
configured directory, filename convention, or another graph invariant.

Vault Rig is for local, file-first Logseq OG graphs. Core retrieval and
integrity checks work with Logseq closed. It is not a hosted knowledge service,
Logseq UI plugin, semantic retrieval engine, MCP server, or second knowledge
store. Its optional DataScript bridge remains local, named-query-only, and
read-only.

## Repository layout

| Path | Owner | Purpose |
| --- | --- | --- |
| `vault_rig/` | Logseq Vault Rig | Python source and `python -m vault_rig` entrypoint |
| `payload/` | Logseq Vault Rig | Files that may later be copied into a vault's `.vault-rig/` area |
| `tests/fixtures/` | Development | Synthetic test inputs only |
| `docs/` | Documentation | User and contributor documentation |
| `.agents/` | Codex integration | Repository-local skills, hooks, and configuration payloads |

Target-vault pages, journals, assets, and `logseq/config.edn` are always
vault-owned. This project does not contain personal vault content or
registry-specific configuration.

## Commands

```text
python -m vault_rig --help
python -m vault_rig --version
python -m vault_rig --check-layout
python -m vault_rig detect /path/to/vault
python -m vault_rig install /path/to/vault --dry-run
python -m vault_rig install /path/to/vault
python -m vault_rig update /path/to/vault --dry-run
python -m vault_rig doctor /path/to/vault
python -m vault_rig uninstall /path/to/vault
python -m vault_rig check /path/to/vault --all
python -m vault_rig check /path/to/vault --changed
python -m vault_rig status /path/to/vault
python -m vault_rig resolve /path/to/vault Plan
python -m vault_rig find /path/to/vault 'exact phrase'
python -m vault_rig context /path/to/vault 'exact phrase'
python -m vault_rig page /path/to/vault Plan
python -m vault_rig block /path/to/vault <block-id>
python -m vault_rig refs /path/to/vault Plan
python -m vault_rig backlinks /path/to/vault Plan
python -m vault_rig history /path/to/vault Plan
python -m vault_rig query /path/to/vault page-by-name Plan
```

## Optional live DataScript queries

The bridge is disabled unless both variables are set. It accepts only loopback
HTTP(S) endpoints and executes only the versioned named queries shown by the CLI.

```text
VAULT_RIG_LOGSEQ_ENDPOINT=http://127.0.0.1:1234/query
VAULT_RIG_LOGSEQ_TOKEN=local-token
python -m vault_rig query /path/to/vault page-by-name Plan
python -m vault_rig query /path/to/vault blocks-referencing-page Plan
```

Remove either variable to disable it; Markdown retrieval and all other commands
continue to work without Logseq or a network connection. To promote an exploratory
query: draft it against synthetic fixtures, inspect its result shape, verify it on a
supported local Logseq instance, then add its fixed name, argument schema, and
result shape to `vault_rig/datascript.py` with a contract test. Never add raw-query
CLI access or credentials to a vault note.

## Release validation

Run `python -m vault_rig.release_validation fast` while iterating. Run
`python -m vault_rig.release_validation check` as the offline release gate;
both commands need Python 3.11+ and Git, and work from a fresh checkout.
