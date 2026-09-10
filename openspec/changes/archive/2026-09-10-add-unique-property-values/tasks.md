## 1. Configuration

- [x] 1.1 Add an `_unique_properties` loader for `.logseq-rig/integrity.json` that defaults to no restriction and validates malformed input the same way `controlled_properties` is validated, then verify a malformed list is rejected as a capability error.

## 2. Duplicate detection

- [x] 2.1 Group existing per-run property occurrences by `(key, value)` for configured property names, then verify a duplicate value across two files is reported once with every conflicting location.
- [x] 2.2 Reuse the `duplicate_persisted_id` changed-mode scoping rule for the new `duplicate_property_value` finding, then verify a collision confined entirely to unchanged files is not surfaced in `check --changed`, while a collision with at least one changed-file occurrence is surfaced with unchanged locations as related evidence.
- [x] 2.3 Verify properties absent from `unique_properties` remain unrestricted.

## 3. Verification

- [x] 3.1 Run `python -m unittest discover -s tests`, `python -m logseq_rig.release_validation check`, and `git diff --check`, recording any environment limitation rather than claiming an unavailable check passed.
- [x] 3.2 Update `openspec/specs/integrity-checks/spec.md` and run `openspec validate --specs --strict --no-interactive` if the CLI is available; otherwise report it as unavailable.
