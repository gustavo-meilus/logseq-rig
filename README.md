# Logseq Rig

Logseq Rig is a small, local command-line tool for existing Logseq OG Markdown graphs. It helps an agent or contributor inspect a graph, install a bounded Codex payload, and check a few graph invariants without taking ownership of the graph itself.

Markdown and Git stay authoritative. Logseq Rig has no runtime dependencies and works with Python 3.11 or later. Its optional DataScript bridge is a local read view, not a graph-writing API.

## What it manages

The tool detects Logseq OG file graphs and reads their configured page and journal directories. It can:

- install, update, diagnose, and remove only its managed payload;
- retrieve pages, blocks, references, backlinks, history, and bounded context as JSON;
- check configured properties, asset references, and changed or complete graph content;
- install a repository-local Skill and Codex hooks without copying graph content into them.

It does not rewrite pages, journals, assets, or `logseq/config.edn`. It does not support Logseq DB graphs, semantic search, MCP, raw queries, or remote endpoints.

## Install

Install from a checkout:

```powershell
python -m pip install .
logseq-rig --version
```

For development, running the module from the checkout is equivalent:

```powershell
python -m logseq_rig --help
```

## Use with a graph

Start with read-only evidence:

```powershell
logseq-rig status C:\path\to\graph
logseq-rig doctor C:\path\to\graph
```

Install or update the managed payload only after reviewing that output:

```powershell
logseq-rig install C:\path\to\graph
logseq-rig update C:\path\to\graph
logseq-rig doctor C:\path\to\graph
```

Use `--dry-run` with lifecycle commands to see the planned changes first. `doctor` never changes the graph. `uninstall` removes only content whose recorded hashes still prove it is managed.

Older `.vault-rig` installations migrate when `update` can prove ownership. The migration writes `.logseq-rig` first, preserves user-owned configuration, and refuses malformed, modified, or conflicting state rather than guessing. Confirm a healthy doctor result and working hooks before removing the older distribution.

## Retrieve and check

All command results are JSON so they can be used from a shell, hook, or agent workflow.

```powershell
logseq-rig resolve C:\path\to\graph "Project Alpha"
logseq-rig find C:\path\to\graph "release notes"
logseq-rig context C:\path\to\graph "Project Alpha" --children 2
logseq-rig block C:\path\to\graph <block-id>
logseq-rig backlinks C:\path\to\graph "Project Alpha"
logseq-rig check C:\path\to\graph --changed
logseq-rig check C:\path\to\graph --all
```

Run `check --changed` after editing canonical Markdown in a Git-backed graph. Use `--all` for a complete integrity pass.

## Optional live queries

The DataScript bridge accepts only registered query names and loopback endpoints. Configure it outside the graph through `LOGSEQ_RIG_*` environment variables; never put endpoint tokens in notes, source, fixtures, or command output. Core detection, retrieval, lifecycle, and integrity commands do not require Logseq to be running.

## Develop and verify

The repository is stdlib-only and uses `unittest`.

```powershell
python -m unittest discover -s tests
python -m logseq_rig.release_validation fast
python -m logseq_rig.release_validation check
openspec validate --specs --strict --no-interactive
git diff --check
```

`release_validation check` exercises disposable synthetic graphs, a legacy-payload migration, the installed console command, lifecycle round trips, and graph-content hash preservation. It does not claim live Logseq or manual smoke testing.

The project layout is intentional: `logseq_rig/` contains the CLI and core behavior, `payload/codex/` contains installed files, `tests/fixtures/` contains synthetic graphs, and `openspec/` contains current contracts and delivery history. See [docs/](docs/README.md) for supporting notes.

## Release

Before a release, run the full verification commands above, ensure relevant OpenSpec work is complete, commit the intended version, and publish the matching Git tag. The current package version is available through `logseq-rig --version`.
