## Context

See `proposal.md` for motivation. The public surface is presently split between a layout-first README, a generic package description, and empty GitHub metadata, while CLI help and synced specs describe a broader implemented core.

## Goals / Non-Goals

**Goals:**

- Make the first public explanation match implemented behavior and existing ownership boundaries.
- Give GitHub discovery metadata the same concise position as repository copy.

**Non-Goals:**

- Create a marketing site, brand system, package distribution, or new runtime capability.
- Change canonical graph ownership, commands, APIs, or live DataScript boundaries.

## Decisions

- Use the approved product name, repository/package/CLI names, and promise without renaming any public identifier. Renaming has migration cost and no demonstrated discovery benefit.
- Treat the CLI, synced OpenSpec specs, and repository tests as the claim oracle. Public copy may simplify terminology but must not add a capability absent from those sources.
- Lead README copy with audience, OG scope, and Markdown/Git authority; move implementation layout behind the product explanation. A layout-first introduction does not establish the product boundary.
- Keep GitHub metadata limited to the approved description and ten topics. A homepage, Marketplace packaging, and registry distribution are separate outcomes.
- State exclusions directly: no hosted knowledge service, DB-graph support claim, second knowledge store, semantic retrieval, or MCP server.

## Risks / Trade-offs

- [Copy drifts from implementation] -> Check each capability claim against CLI help and synced specs before merge.
- [Metadata cannot be reviewed in a repository diff] -> Verify the public GitHub page after applying its settings.
- [Positioning is mistaken for a compatibility expansion] -> Preserve all current names and explicit OG-only/non-goal language.

## Migration Plan

Apply copy and metadata changes together. Rollback is a revert of repository documentation and restoration of prior GitHub settings; no user vault data or runtime state migrates.
