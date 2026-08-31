## 1. Repository Boundaries

- [x] 1.1 Create the source, managed-payload, tests/fixtures, and documentation areas with ownership documentation, then verify the documented map matches the filesystem.
- [x] 1.2 Add release metadata and document Python 3.11+ plus Git as the initial prerequisites, then verify a fresh checkout contains no personal-vault content or registry-specific configuration.

## 2. Stable Entrypoint

- [x] 2.1 Add the minimal vault_rig package and python -m vault_rig entrypoint with version/help output, then verify both commands exit successfully using only the standard library.
- [x] 2.2 Reserve only the .vault-rig/ target namespace and approved repository-local Codex payload locations, then verify none overlap pages, journals, assets, or logseq/config.edn.

## 3. Layout Verification

- [x] 3.1 Implement the deterministic layout check for required boundaries and forbidden canonical-vault content, then verify one healthy and one intentionally invalid layout produce the expected exit statuses.
- [x] 3.2 Add the smallest unittest coverage for the entrypoint and layout contract, then verify python -m unittest passes from a fresh checkout.
