## 1. Truthful public copy

- [x] 1.1 Audit `README.md`, `pyproject.toml`, and public documentation against CLI help and current OpenSpec specs; verify every retained capability claim has repository evidence.
- [x] 1.2 Rewrite the README opening and package description around the approved OG control-layer position, promise, graph-drift definition, and explicit product boundaries; verify the stale planned-history wording is absent and the opening is understandable without repository context.
- [x] 1.3 Update only public documentation that contradicts the approved position; verify relative documentation links resolve and no semantic-retrieval, MCP, hosted-service, UI-plugin, or second-store claim is introduced.

## 2. Repository discovery metadata

- [x] 2.1 Set the approved GitHub repository description and ten approved topics; verify the public repository page shows the exact description and topics.

## 3. Change verification

- [x] 3.1 Run `python -m vault_rig --help`, search public copy for stale roadmap/category claims, and manually review the README opening against the proposal's scope and non-goals.
- [x] 3.2 Run `git diff --check` and `openspec validate position-logseq-vault-rig --strict`; verify only approved public-copy, metadata, and planning changes are present.
