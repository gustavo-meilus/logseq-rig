## Context

See proposal.md and specs/vault-lifecycle/spec.md. Lifecycle operations cross an ownership boundary between the reusable payload and existing user repositories, so planning, conflict detection, and recoverability must precede writes.

## Goals / Non-Goals

**Goals:**
- Derive dry-run and execution from the same deterministic change plan.
- Prove ownership before update or removal.
- Preserve canonical knowledge and unrelated configuration under interruption.

**Non-Goals:**
- General-purpose file synchronization, three-way merging, backups, or Git automation.
- Ownership of complete user configuration files when a bounded region suffices.

## Decisions

1. **Use a plan-first engine.** Install, update, and uninstall build a list of add, replace, bounded-region edit, conflict, and remove actions. Dry-run serializes that plan; execution applies the same object.
2. **Store one JSON manifest under .vault-rig/.** It records schema version, Vault Rig version, relative managed paths, ownership mode, and SHA-256 identities. JSON and SHA-256 use the Python standard library; no state database is introduced.
3. **Use explicit markers for shared text files.** Existing AGENTS.md content is preserved around one Vault Rig-managed region. A file created wholly by Vault Rig is recorded as whole-file-owned. Missing, duplicated, or locally changed markers become conflicts.
4. **Stage managed writes before replacement.** New content is written under the managed namespace, flushed, then atomically replaced where the platform supports it. Canonical directories are never part of a write plan.
5. **Fail closed on drift.** Update and uninstall compare current identities with the manifest. They do not overwrite or remove mismatched content; doctor reports the same state without mutation.

## Risks / Trade-offs

- [Atomic replacement differs by filesystem] → Keep staging on the target filesystem and retain clear incomplete-state diagnostics.
- [Managed-region markers collide with user text] → Use unique versioned markers and reject duplicates.
- [Manifest loss prevents proof of ownership] → Doctor reports unmanaged residue; uninstall does not guess.

## Migration Plan

Introduce dry-run and doctor before enabling writes. Validate install-twice and uninstall on fixtures. Rollback uses uninstall while the manifest is healthy; conflicts require user review rather than forced cleanup.
