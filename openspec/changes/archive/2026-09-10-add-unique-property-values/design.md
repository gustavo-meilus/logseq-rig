## Context

See proposal.md and `specs/integrity-checks/spec.md`. The checker already builds an in-memory list of `(key, value, location)` property occurrences per run and already supports one opt-in, graph-local configuration shape (`controlled_properties`) with its own malformed-configuration handling. Duplicate detection for persisted `id` values already exists as a graph-wide check that is scoped to changed files in `check --changed` the same way this feature needs to behave for arbitrary configured properties.

## Goals / Non-Goals

**Goals:**

- Let a graph opt a property into graph-wide uniqueness without hardcoding any property name or taxonomy.
- Reuse the existing `duplicate_persisted_id` changed-mode scoping rule: report a collision if any conflicting occurrence is in a changed file, and include unchanged occurrences as related evidence.
- Validate `unique_properties` configuration with the same strictness and failure shape as `controlled_properties`.

**Non-Goals:**

- Cross-property or cross-graph identifier schemes (note-id, Zettelkasten, citation keys).
- Repairing or deduplicating conflicting values.
- Restricting properties that are not explicitly configured.

## Decisions

1. **Add a parallel `_unique_properties` loader.** It reads `.logseq-rig/integrity.json`, defaults to an empty set when the key or file is absent, and raises the same `ValueError` shape as `_controlled` for a malformed list. This matches the existing controlled-property validation pattern instead of introducing a new configuration error format.
2. **Group existing property occurrences by `(key, value)`.** The checker already visits every `(key, value, location)` triple once per run; duplicate detection adds a `defaultdict(list)` keyed on that pair, populated only for configured property names, with no extra file reads.
3. **Reuse the `duplicate_persisted_id` scoping shape for `duplicate_property_value`.** A collision is only emitted when at least one location in the group is `active` (changed-file-selected or full mode); the finding's `related` list always includes every known location, changed or not. This keeps changed-mode behavior consistent across both graph-wide duplicate checks.

## Risks / Trade-offs

- [A configured property with many values does a full graph scan] → Already true for `controlled_properties`; grouping is linear in the number of matched properties and does not add a new pass over file contents.
- [Users could point `unique_properties` at `id`] → No special-casing is added; behavior degrades gracefully to a redundant but harmless second finding for that property, not a broken one.

## Migration Plan

Purely additive and opt-in: graphs without `unique_properties` in `.logseq-rig/integrity.json` see no behavior change. No existing configuration shape changes.
