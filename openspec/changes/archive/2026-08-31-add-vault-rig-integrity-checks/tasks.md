## 1. Evidence Collection

- [x] 1.1 Build the per-run in-memory map of persisted UUIDs, references, properties, and local assets from the shared parser, then verify source and related locations are retained.
- [x] 1.2 Define stable finding codes and machine-readable output, then verify a caller can distinguish pass, warning, capability error, and integrity failure by output and exit status.

## 2. Invariant Checks

- [x] 2.1 Implement persisted UUID format and uniqueness checks, then verify malformed and duplicate fixtures report every relevant location.
- [x] 2.2 Implement missing persisted block-target and evidenced referenced-block deletion checks, then verify failures identify both reference and target/deletion evidence.
- [x] 2.3 Implement deterministic local-asset checks and opt-in controlled-property rules, then verify unconfigured properties and valid fileless page refs remain accepted.

## 3. Check Modes

- [x] 3.1 Implement check --all over the detected graph, then verify healthy and failing fixtures produce reliable statuses without changing files.
- [x] 3.2 Implement Git-selected check --changed with optional declared mutation scope, then verify changed-only diagnostics, unsupported non-Git behavior, and mass-mutation warnings.

## 4. Regression Verification

- [x] 4.1 Run both check modes against all invariant fixtures and compare pre/post hashes, then verify the checker is deterministic and read-only.
