## Context

See [proposal.md](proposal.md) for motivation and the delta specifications for behavior. The current package and installed payload use one name family in packaging, command invocation, Python imports, payload paths, manifest markers, integrity configuration, fixtures, and user-facing copy. Lifecycle ownership records are content-hash based, and the existing incomplete-state marker detects but does not resume interrupted operations.

The change is a public breaking rename, but installed graphs may contain managed state from the existing release. The migration must preserve canonical Markdown, user instructions, assets, Logseq configuration, and user-owned configuration.

## Goals / Non-Goals

**Goals:**

- Make `logseq-rig`, `logseq_rig`, `.logseq-rig`, Graph terminology, and `LOGSEQ_RIG_*` the sole active public contract.
- Migrate a clean legacy managed payload safely and make every unsafe legacy state a diagnostic no-write outcome.
- Retain existing offline, read-only retrieval/integrity/DataScript security behavior.
- Provide deterministic validation for the installed command and migration lifecycle.

**Non-Goals:**

- Preserve a public legacy executable, Python-package alias, or environment-variable alias.
- Modify canonical graph content, enable graph writes through DataScript, add dependencies, or alter parsing/retrieval semantics.
- Rewrite archived OpenSpec or stale proposal history.

## Decisions

### One public name family with a major-release boundary

The distribution and repository use `logseq-rig`; Python imports use `logseq_rig`; the console executable and installed Skill use `logseq-rig`; managed state uses `.logseq-rig`; and user-facing product terminology uses Graph. Public descriptor and diagnostics use Graph terminology. The descriptor's serialized field schema remains unchanged unless a field itself must change.

No runtime alias for the old executable, package, or environment variables is provided. An alias would retain the terminology this change removes and would obscure whether an installed payload has been migrated. The release documentation instead requires installing the new distribution, running its update command, verifying doctor, then optionally removing the old distribution.

### Migration is ownership-proven, preflighted, and idempotent

`update` is the migration entrypoint. Before any write it validates exactly one recognized legacy manifest, every legacy managed file/region hash, marker structure, destination ownership state, and relevant user configuration. It rejects duplicate markers, both namespaces with conflicting state, missing/unproven legacy records, destination collisions, and modified managed content without writing either namespace.

For a successful migration, it writes the active payload and manifest before retiring proven legacy payload paths. A durable destination migration record captures the migration phase and allows `doctor` to report incomplete state. A later `update` either completes cleanup deterministically or reports a conflict; it never guesses ownership. This extends the existing incomplete-operation approach rather than adding a separate migration subsystem.

### User-owned integrity configuration is copied, never silently deleted

The controlled-property configuration is not manifest-owned. When only a valid legacy configuration exists, migration copies its rules into the active namespace and preserves the original. If active and legacy configurations differ, migration stops before writes. This preserves integrity behavior without claiming ownership of user configuration.

### Current specifications move to Graph terminology; historical records stay immutable

The active main-spec capability directories and headings that expose the old term are renamed during implementation and their references updated. Delta specs retain existing capability paths only because OpenSpec requires them to target the current contracts. Archived changes and stale proposals remain historical evidence and are excluded from terminology-completeness checks.

### Validation uses the packaged interface and synthetic graphs

Repository tests retain fast unit coverage. Release validation gains a disposable legacy fixture/migration path and installs the built distribution into a temporary environment to exercise the `logseq-rig` console executable. No private graph, network endpoint, or live Logseq process is needed.

## Risks / Trade-offs

- [An interrupted migration leaves both name families present] → Persist a destination migration phase before altering legacy files; make doctor diagnostic and update resumable or conflict-only.
- [A user has independently created a destination payload/configuration path] → Treat it as a conflict rather than overwrite or absorb it.
- [Legacy hooks stop working after the old distribution is removed too early] → State the upgrade order prominently and verify the new installed hooks before advising removal.
- [Historical files retain old terms] → Scope terminology checks to active product files and document the intentional historical exception.
- [A renamed package is installed alongside the old distribution] → Treat coexistence as expected during migration; do not rely on package-manager upgrade semantics to remove the old distribution.

## Migration Plan

1. Release the renamed distribution with the migration-capable lifecycle and updated payload.
2. Users install `logseq-rig`, run `logseq-rig doctor <graph>`, then run `logseq-rig update <graph>` when migration is required.
3. Users verify healthy doctor output and the installed hooks before optionally uninstalling the old distribution.
4. Rename the GitHub repository and update remotes, external action references, package links, and release documentation only after repository validation passes.

Rollback is operational: before legacy cleanup completes, the migration record supports deterministic completion or a no-write conflict. A failed migration does not alter canonical graph content or overwrite user-owned files; manual intervention is required for ambiguous ownership rather than an automatic rollback that could destroy data.
