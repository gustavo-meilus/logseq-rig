# Contributing

## Workflow

1. Fork the repository and create a focused branch from `main`.
2. Make the smallest change that solves the issue. Do not add personal-graph data.
3. Add or update tests and documentation for behavior changes.
4. Run the checks below, review `git diff`, and open a pull request from the fork.

Questions and early ideas belong in GitHub Discussions. Use an issue for a reproducible bug or a concrete feature request.

## Development checks

The project uses Python 3.11+ and has no runtime dependencies:

```powershell
python -m pip install .
python -m unittest discover -s tests
python -m logseq_rig.release_validation fast
python -m logseq_rig.release_validation check
openspec validate --specs --strict --no-interactive
git diff --check
```

The full release validation command is the canonical local verifier. It does not claim live Logseq or manual smoke testing.

## OpenSpec

Behavior changes require an OpenSpec change under `openspec/changes/`, with the relevant proposal, specification, design, and tasks. Keep `openspec/specs/` synchronized when the change is complete; do not modify archived history.

## Graph ownership

Markdown, assets, Logseq configuration, and Git history in a target graph remain graph-owned and authoritative. Use `logseq-rig status <graph>` and evidence commands before editing a graph, then run `logseq-rig check <graph> --changed` after canonical Markdown edits. The managed payload is limited to `payload/codex/`; preserve user-owned instructions and configuration. Never add credentials, personal notes, or raw graph content to this repository.
