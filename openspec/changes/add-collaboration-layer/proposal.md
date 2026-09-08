## Why

The public repository lacks the versioned policies, contributor entrypoints, and automated checks that let outside contributors submit safe, reviewable changes. A small collaboration layer establishes those expectations without changing Logseq Rig's runtime or graph-ownership model.

## What Changes

- Add an MIT license and matching package metadata.
- Add contributor, conduct, and security policies, plus README links to the contribution routes.
- Add a CODEOWNERS file, pull-request template, and bug and feature issue forms.
- Add a GitHub Actions pull-request check for installation, unit tests, fast release validation, and whitespace errors.
- Declare the existing full release-validation command as the repository's canonical local verification command.
- Document the required GitHub administration steps: enable private vulnerability reporting and Discussions; protect `main` with pull requests, passing CI, resolved conversations, deletion restriction, and force-push blocking; defer required approvals until a second maintainer is available.

## Capabilities

### New Capabilities
- `collaboration-governance`: Defines the public contribution, security-reporting, review, and continuous-integration contract for the repository.

### Modified Capabilities
- None.

## Impact

Adds repository-root policy files and verifier configuration, `.github/` templates and CI configuration, README and `pyproject.toml` metadata, and documented GitHub settings. It adds no runtime dependency, changes no CLI or target-graph behavior, and does not modify archived OpenSpec history.
