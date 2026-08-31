## Context

See proposal.md and specs/release-validation/spec.md. The implementation spans filesystem ownership, parsing, Git history, hooks, and preservation guarantees, so unit checks alone cannot prove the release contract.

## Goals / Non-Goals

**Goals:**
- Make every fixture small, synthetic, and attributable to one behavior class.
- Run lifecycle tests only on disposable copies.
- Keep one fast developer check and one authoritative release check.

**Non-Goals:**
- A private-vault corpus, model-quality benchmark, CI vendor configuration, or speculative OS matrix.
- A giant fixture containing every feature.

## Decisions

1. **Store source fixtures as immutable test inputs.** Each scenario has minimal canonical files plus expected machine-readable outcomes. Tests copy fixtures to a temporary directory before any mutation.
2. **Use Python's built-in unittest, tempfile, and hashing support.** No test framework is added until standard-library discovery or diagnostics becomes insufficient.
3. **Expose check-fast and check as stable scripts.** The fast path runs layout, unit, and affected fixture checks; the authoritative path runs the full fixture lifecycle from clean copies.
4. **Hash protected content before and after.** Expected lifecycle changes are enumerated; any other canonical or user-owned content difference fails validation.
5. **Keep CI integration provider-neutral.** A future CI file invokes the same authoritative local command rather than reimplementing the suite.

## Risks / Trade-offs

- [Fixtures drift to match broken output] → Keep expected behavior in specs and review fixture expectation changes as product changes.
- [Platform behavior differs] → Claim support only for environments exercised by the authoritative check; add matrix entries after real execution.
- [Full validation grows slow] → Preserve the cheap path and split fixtures by behavior without weakening the release command.

## Migration Plan

Add fixtures alongside the capabilities they validate, then make the full command the release gate. Rollback removes test assets and the gate without touching user vaults.
