## Project Purpose

`logseq-vrig` is a portable, stdlib-only control layer for existing Logseq OG Markdown vaults. Markdown and Git remain authoritative; optional DataScript is a local live read view. Release core is implemented; semantic retrieval and MCP remain deferred until a real need exists.

## Stack and Runtime

Python `3.11+`; no runtime dependencies. `Git` is required for history, changed-file integrity checks, and release fixtures. `openspec/` contains synced specifications and archived delivery records.

## Build, Test, Run

- CLI: `python -m vault_rig --help`
- Focused tests: `python -m unittest discover -s tests`
- Fast gate: `python -m vault_rig.release_validation fast`
- Release gate: `python -m vault_rig.release_validation check`
- Main-spec validation: `openspec validate --specs --strict --no-interactive`

## Architecture Map

- `vault_rig/`: CLI and deterministic vault detection, lifecycle, retrieval, integrity, release validation, and optional DataScript bridge.
- `payload/codex/`: files installed into a target vault; `lifecycle.py` owns their safe install/update/uninstall behavior.
- `tests/fixtures/`: synthetic vaults only; `tests/` uses `unittest`.
- `openspec/specs/`: current behavior contracts; `openspec/changes/archive/`: historical implementation records.
- `proposals/`: roadmap contracts; `09` semantic retrieval and `10` MCP are intentionally deferred.

Flow: detect a target vault → parse Markdown once for retrieval/integrity → return JSON evidence → mutate only managed payload through lifecycle operations.

## Domain Model

Target-vault Markdown, assets, and Logseq configuration are vault-owned. Preserve logical page names, block `id` values, block references, properties, asset paths, configured directories, and filename conventions. `VaultDescriptor` is the configuration source for downstream work. Live queries accept only registered names and a loopback endpoint; they never write graph data or expose credentials.

## Agent Guardrails

- Before editing a vault, use `vault-rig status <vault>` then evidence commands; after canonical Markdown edits run `vault-rig check <vault> --changed`.
- Treat `payload/codex/` as install-owned and change it with matching lifecycle tests; never hand-edit a target vault's managed manifest.
- Preserve user-owned instructions and canonical content during install/update/uninstall; do not use destructive Git operations or add personal-vault data.
- Keep live query credentials out of notes, source, test fixtures, output, and errors. Do not add raw-query or graph-write CLI access without an approved spec.

## Known Failure Modes

- Do not assume configured Markdown directories, filenames, aliases, or journal dates: use `detect()`/`VaultDescriptor`.
- Do not treat optional runtime features as core dependencies; core retrieval and integrity work with Logseq closed.
- Archived Codex manual smoke and live-DataScript integration checks are waived as unavailable, not executed evidence; do not claim either passed.
- Proposal files describe historic pre-OpenSpec planning and are stale on that point; synced specs and archived changes describe current delivery state.

## Verification Before Completion

Run affected tests, then `python -m unittest discover -s tests` and `python -m vault_rig.release_validation check` for behavior or payload changes. Run `git diff --check`. For spec changes, run `openspec validate --specs --strict --no-interactive`. Report unavailable live/manual validation as unavailable.

## Escalation - Ask the User When

Ask before changing canonical vault content, expanding managed payload ownership, changing DataScript API/protocol or security boundaries, enabling semantic/MCP features, modifying archive history, or treating waived live/manual validation as passed.
