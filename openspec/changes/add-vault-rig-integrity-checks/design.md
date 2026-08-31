## Context

See proposal.md and specs/integrity-checks/spec.md. Integrity checks can reuse the retrieval parser and resolver, but their output must remain a stronger deterministic oracle than the agent making edits.

## Goals / Non-Goals

**Goals:**
- Share parsing without sharing mutable state.
- Keep changed-mode feedback cheap while retaining graph-wide evidence where required.
- Emit stable diagnostics usable by humans, hooks, and CI.

**Non-Goals:**
- Automatic repair, prose linting, taxonomy enforcement, or semantic review.
- A persistent validation database.

## Decisions

1. **Build one in-memory graph evidence map per run.** It maps persisted UUIDs, references, controlled properties, and local assets to source locations. Initial complexity is linear in graph size and avoids stale cache invalidation.
2. **Use Git to select changed inputs.** Changed mode applies detailed checks to changed canonical files while consulting the global evidence map for uniqueness and reference targets. Full mode reports every supported failure.
3. **Represent findings with stable codes.** Each finding includes severity, invariant code, source location, related locations, and remediation context. Exit status is non-zero for errors.
4. **Keep controlled-property rules explicit.** A small vault-local configuration lists controlled keys and allowed values. Absence means no controlled-property checks.
5. **Treat declared mutation scope as optional input.** Mass-mutation warnings run only when a lifecycle or task supplies an expected scope; no intent is inferred from file counts alone.

## Risks / Trade-offs

- [Linear scans become expensive] → Measure first; add a disposable cache only when full-check latency is unacceptable.
- [False positives block valid Logseq behavior] → Add only high-confidence invariants and fixture every rule, including allowed counterexamples.
- [Git is unavailable or the vault is not a repository] → Full mode remains available; changed mode returns a clear capability error.

## Migration Plan

Ship check --all first for baseline assessment, then enable check --changed in hooks after fixtures pass. Existing failures are reported, never rewritten. Rollback disables hook enforcement and removes the checker.
