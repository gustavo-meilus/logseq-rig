## Context

See proposal.md and specs/codex-integration/spec.md. Current official Codex documentation confirms repository AGENTS.md discovery, repository Skills under .agents/skills, SessionStart and Stop hooks, and workspace-write/on-request configuration. Project-scoped Codex layers require repository trust.

## Goals / Non-Goals

**Goals:**
- Keep always-loaded instructions short and procedures progressively disclosed.
- Make graph verification mechanical after canonical edits.
- Bound authority and retry behavior using supported Codex primitives.

**Non-Goals:**
- Mandatory subagents, automatic web research, style hooks, or general prompt policy.
- Depending on unstable transcript contents.

## Decisions

1. **Install one bounded AGENTS.md region.** It names source of truth, retrieval order, edit invariants, and completion command. The lifecycle manifest owns only that region when the file pre-exists.
2. **Install one Skill at .agents/skills/vault-rig/.** It routes lookup, context expansion, safe edits, and verification to the CLI. Deterministic mechanics remain in Python commands.
3. **Keep hook scripts under the managed namespace and reference them from current project hook configuration.** SessionStart emits a bounded status summary as additional context.
4. **Use Stop's current JSON contract and stop_hook_active flag.** On the first failed changed-content check, return a block decision with evidence; when already active, allow completion while reporting unresolved failure. The hook never parses transcript internals.
5. **Use workspace-write with on-request approvals and no default network access.** Read-only tasks need no elevated authority. Exact keys and generated config are checked against the installed Codex release during implementation.
6. **Do not install a reviewer agent.** Document read-only independent review as an optional escalation for high-risk semantic restructuring.

## Risks / Trade-offs

- [Codex hook/config schemas evolve] → Pin fixtures to the installed release and verify official documentation before updating payload.
- [Project config is ignored in an untrusted repository] → Session orientation reports inactive integration and installation docs require explicit trust review.
- [Hook latency interrupts routine work] → Run only the changed-content check and bound output.

## Migration Plan

Install through the lifecycle ownership plan, smoke-test startup and Stop pass/fail/second-fail paths, then enable by default for installed vaults. Uninstall removes only proven managed files and regions.
