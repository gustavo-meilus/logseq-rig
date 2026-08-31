## Context

See proposal.md and specs/repository-foundation/spec.md. The repository currently contains planning material but no implementation runtime or layout. Python 3.11 and Git are available locally; the first release needs file, JSON, hashing, subprocess, and test support but no framework.

## Goals / Non-Goals

**Goals:**
- Establish the fewest durable project boundaries needed by the approved roadmap.
- Use a portable standard-library runtime and one stable command surface.
- Make target-vault ownership visually and mechanically distinct.

**Non-Goals:**
- Package-registry publication, CI-provider selection, or optional retrieval adapters.
- Pre-creating abstractions for features that do not yet exist.

## Decisions

1. **Use Python 3.11+ and the standard library for the portable core.** Source lives under a single vault_rig package, with python -m vault_rig as the canonical implementation entrypoint and thin platform launchers only if required. This is smaller than introducing Node packaging or compiled binaries and covers the known filesystem, JSON, hashing, subprocess, and test needs.
2. **Use four project-owned areas:** source, managed payload, tests/fixtures, and documentation. Keep release metadata at the root. Avoid deeper domain layering until multiple modules earn it.
3. **Reserve .vault-rig/ inside target vaults for managed state and payload.** Canonical pages, journals, assets, and logseq/config.edn remain vault-owned.
4. **Make layout validation data-driven but fixed.** A small check validates required paths and forbidden canonical content; no plugin architecture or general policy engine is added.

## Risks / Trade-offs

- [Python must exist on target machines] → Document Python 3.11+ as the initial runtime prerequisite; add packaging only after a real distribution need.
- [Reserved directories could outlive roadmap changes] → Reserve only .vault-rig/ and currently approved Codex payload locations.
- [Thin launchers can diverge] → Keep python -m vault_rig authoritative and test wrappers as delegation only.

## Migration Plan

Create the layout and validation check in an empty implementation tree. Rollback is deletion of the new project-owned files; no target vault is touched.
