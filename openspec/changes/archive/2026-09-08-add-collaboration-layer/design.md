## Context

See proposal.md and `specs/collaboration-governance/spec.md`. The repository has no license, contribution policies, GitHub templates, or CI workflow. Its existing development commands are the authoritative validation surface, and the project must retain its local-first and graph-ownership guarantees.

## Goals / Non-Goals

**Goals:**

- Give external contributors one concise, versioned route from question or report through a reviewed pull request.
- Make the ordinary PR gate deterministic, dependency-free for the project, and quick enough for each pull request.
- Keep administrator-only GitHub configuration explicit and separately verifiable.

**Non-Goals:**

- Changing runtime code, CLI behavior, target-graph content, or managed payload ownership.
- Adding bots, funding files, a contributor-license agreement, a governance board, or a custom security-reporting service.
- Requiring an approval until a second trusted maintainer exists.

## Decisions

1. **Use an MIT `LICENSE` and PEP 621 license metadata.** This is the selected permissive license and makes reuse terms visible to GitHub and packaging tools. Apache-2.0 was not selected because the owner chose MIT.
2. **Use GitHub-native contribution surfaces.** Place CODEOWNERS, the pull-request template, issue forms, and a single CI workflow in `.github/`; use GitHub Discussions for questions and early design conversation. This keeps contributor intake close to the pull-request workflow instead of adding a hosted tool or bot.
3. **Keep CI to the existing fast gate.** The workflow uses checkout, Python 3.11 setup, `pip install .`, unit tests, fast release validation, and `git diff --check` on pushes and pull requests to `main`. The full release gate remains a release/manual command because it is deliberately broader and slower.
4. **Use GitHub private vulnerability reporting first, email second.** Administrators enable GitHub private vulnerability reporting; `SECURITY.md` lists it as preferred and `gmeilus@outlook.com` as a durable fallback. This avoids publishing exploit details while retaining a route if GitHub reporting is unavailable.
5. **Make repository settings a documented manual deployment step.** Branch rulesets, Discussions, private vulnerability reporting, and optional Wiki disablement cannot be reliably represented by repository files. The implementation documents the exact settings and records that successful CI must run once before its check is required.
6. **Declare, rather than duplicate, the existing full release gate.** A minimal harness configuration points to `python -m logseq_rig.release_validation check`. This supplies one discoverable canonical verifier without a new script, target, or competing validation path.

## Risks / Trade-offs

- [GitHub settings are not version-controlled] → List them as explicit administrator tasks and verify them in the repository settings after the pull request merges.
- [A one-person project can be blocked by mandatory review] → Require PRs and CI now; add one required approval only after a second trusted maintainer is active.
- [The email address can receive non-security mail] → State that it is for confidential vulnerability reports and prefer GitHub private reporting.
- [Fast CI can miss broader release failures] → Preserve the existing full release validation as the release gate.

## Migration Plan

1. Merge the version-controlled collaboration files and confirm the workflow completes on `main`.
2. Enable Discussions and private vulnerability reporting in GitHub.
3. Create a `main` branch ruleset with pull-request, CI, conversation-resolution, force-push, and deletion controls; select the successful CI check as required.
4. Optionally disable the Wiki after confirming no intended documentation is hosted there.

Rollback is removal of the added repository files and relaxation of the GitHub settings. No graph data, payload, or runtime state is migrated.
