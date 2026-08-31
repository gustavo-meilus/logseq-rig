## Context

See proposal.md and specs/datascript-query-bridge/spec.md. Logseq OG exposes plugin APIs, including DataScript query capability, through an optional local HTTP API. The bridge is a live read view only; canonical Markdown and offline retrieval remain authoritative.

## Goals / Non-Goals

**Goals:**
- Reuse the existing local HTTP API and retrieval evidence model.
- Offer a small named-query surface with explicit availability errors.
- Keep credentials local and authority read-only.

**Non-Goals:**
- A bespoke Logseq plugin/protocol, raw-query command in the initial release, or graph writes.
- Reimplementing DataScript or making Logseq runtime a core dependency.

## Decisions

1. **Call the loopback Logseq HTTP API with the Python standard library.** The adapter invokes the supported DataScript query method and performs a capability probe before execution. A community CLI or plugin is unnecessary unless the built-in API fails the required fixtures.
2. **Accept endpoint and token only from environment variables in the initial release.** No secret is written into the vault or repository. Non-loopback endpoints are rejected by default.
3. **Store named Datalog queries as version-controlled managed files with a small registry.** The registry defines name, arguments, result shape, and query version; callers cannot select arbitrary methods.
4. **Omit raw query execution initially.** It adds authority and validation surface without an approved recurring need. New queries are drafted in development, verified against fixtures, then registered.
5. **Normalize through existing resolvers.** Returned page and block identities are mapped to canonical source evidence when possible; unresolved live entities remain explicitly marked rather than guessed.

## Risks / Trade-offs

- [HTTP API behavior differs across Logseq versions] → Probe capabilities, test supported versions, and fail with version/evidence details.
- [Token leaks through logs] → Redact request headers and never echo environment secrets.
- [Live results race with unsaved state] → Label results as live evidence and retain canonical source reconciliation.

## Migration Plan

Ship disabled by default. Enabling requires loopback endpoint and token environment variables. Removal deletes managed query files and adapter configuration only; core commands and knowledge remain unchanged.
