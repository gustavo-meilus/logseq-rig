# Vault Rig

Vault Rig is a portable, Python 3.11+ tool for managing the `.vault-rig/`
area of a Logseq OG vault. Git is required for the planned history features.

## Repository layout

| Path | Owner | Purpose |
| --- | --- | --- |
| `vault_rig/` | Vault Rig | Python source and `python -m vault_rig` entrypoint |
| `payload/` | Vault Rig | Files that may later be copied into a vault's `.vault-rig/` area |
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
```
