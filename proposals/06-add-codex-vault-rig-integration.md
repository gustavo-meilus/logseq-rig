# Proposed OpenSpec Change: add-codex-vault-rig-integration

> Status: **Normalized proposal contract - approval required before creating an OpenSpec change.** These files are planning contracts, not implementation artifacts.


**Name:** `add-codex-vault-rig-integration`  
**Release target:** `0.1`  
**Depends on:** `add-vault-rig-retrieval-core`, `add-vault-rig-integrity-checks`

## Intent

Install the minimum repository-local Codex integration for Logseq Vault Rig so Codex understands Logseq OG semantics, retrieval routing, safe editing, and completion verification without turning `AGENTS.md` into an encyclopedia.

## Current / Problem

Codex can read Markdown directly but generic behavior may flatten block structure, infer wrong paths, overuse web/semantic search, or make edits without checking stable block identity. Repeating all rules in every prompt wastes context and is inconsistent across vaults.

## Desired Behavior

Each Logseq Vault Rig installation exposes a concise operating contract, one progressively disclosed `vault-rig` Skill, bounded Codex configuration, and lifecycle hooks that orient sessions and enforce deterministic graph checks after canonical edits.

## In Scope

- Provide a concise root operating contract covering source of truth, Logseq invariants, search routing, editing boundaries, and verification command.
- Provide one repository-local `.agents/skills/vault-rig/` Skill that routes retrieval and editing workflows.
- Provide a small SessionStart hook that reports discovered vault state, Git state, retrieval capabilities, and current integrity status without dumping the graph.
- Provide a bounded Stop hook that runs `vault-rig check --changed` when canonical graph files changed and allows at most one repair continuation before reporting unresolved failure.
- Provide a conservative Codex config baseline using workspace-scoped write authority and approvals appropriate to the currently installed Codex version.
- Keep external web research disabled/not selected for ordinary personal-knowledge queries unless explicitly requested.
- Document optional read-only reviewer use for high-risk semantic restructuring without making it mandatory.

## Out of Scope

- Create five+ default Skills or a multi-agent swarm.
- Require semantic indexing, MCP, or live Logseq API for basic operation.
- Automatically rewrite the user's existing root instructions without a reversible merge strategy.
- Use hooks for style advice or optional preferences that can remain documentation.

## Acceptance Cases

- A new Codex session can discover how to search and verify the graph without embedding the full Logseq manual in always-loaded context.
- Exact/structural questions route through deterministic `vault-rig` commands before broad semantic reasoning.
- Canonical Markdown edits trigger the graph check before Codex can report clean completion.
- A failing Stop check cannot create an unbounded autonomous loop.
- Read-only knowledge questions can be performed without granting unnecessary mutation authority.
- Logseq Vault Rig remains functional when Logseq is closed, except explicitly live-query features.

## Constraints / Preservation

- One primary agent by default.
- Progressive disclosure: root instructions contain stable invariants/map; procedures live in the Skill; mechanics live in scripts; lifecycle enforcement lives in hooks.
- Hook behavior must be compatible with the currently installed Codex hook API at implementation time.
- No destructive Git commands or automatic commits/pushes.

## Migration / Rollout

- Installer adds/updates only managed Codex/Skill/hook payload and preserves user-owned instructions through the lifecycle ownership strategy.

## Validation

- Fixture installation plus Codex/hook unit tests where possible; deterministic hook scripts tested independently; manual smoke test that SessionStart context is bounded and Stop gate behaves on pass/fail/second-fail paths.

## Assumptions

- Start with one `vault-rig` Skill and one primary agent; add specialist agents only after observed context isolation/independent-review need.

## Material Decisions

- Use hooks only for lifecycle state/invariants that should not depend on model memory.
- Use the `vault-rig` CLI as the stable agent-computer interface.

## Open Questions

- Exact Codex config keys/locations should be verified against the installed Codex release when implementing, because the product evolves.
