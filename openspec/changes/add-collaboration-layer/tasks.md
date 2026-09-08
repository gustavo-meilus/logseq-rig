## 1. Versioned collaboration policy

- [x] 1.1 Add the MIT `LICENSE` and PEP 621 license metadata in `pyproject.toml`, then verify `python -m pip install .` succeeds and the license file is present.
- [x] 1.2 Add `CONTRIBUTING.md` with the fork-to-PR flow, existing development commands, OpenSpec expectations, and local-first/graph-ownership constraints, then verify every command and linked path is current.
- [x] 1.3 Add `CODE_OF_CONDUCT.md` with a private enforcement contact and `SECURITY.md` with supported-version, report-content, acknowledgement, GitHub-private-reporting, and email-fallback guidance, then verify no policy directs exploit disclosure to public issues.
- [x] 1.4 Add concise Contributing and License sections to `README.md`, then verify the links resolve from a clean checkout.

## 2. GitHub contribution surfaces

- [x] 2.1 Add `.github/CODEOWNERS` assigning `@gustavo-meilus` to all files and `.github/`, then verify GitHub recognizes the file after the pull request is opened.
- [x] 2.2 Add bug and feature issue forms plus issue-template configuration that directs questions and early ideas to Discussions, then verify both forms render in GitHub and the bug form requires the specified diagnostic details.
- [x] 2.3 Add `.github/PULL_REQUEST_TEMPLATE.md` with change rationale, verification, documentation/OpenSpec, and graph-safety checklists, then verify a new pull request loads the template.

## 3. Continuous integration

- [x] 3.1 Add `.github/workflows/ci.yml` for `main` pushes and pull requests using Python 3.11, `pip install .`, unit tests, fast release validation, and whitespace checking, then verify the workflow appears in GitHub Actions.
- [x] 3.2 Add the minimal harness configuration that declares `python -m logseq_rig.release_validation check` as the canonical verifier, then run that command successfully.
- [x] 3.3 Confirm the workflow succeeds on `main`, then record its exact required-status-check name for the branch ruleset.

## 4. GitHub administrator configuration

- [x] 4.1 Enable GitHub Discussions and private vulnerability reporting, then verify the repository exposes both collaboration and private-reporting entrypoints.
- [x] 4.2 Create a `main` branch ruleset that blocks force pushes and deletions and requires pull requests, the successful CI check, and resolved conversations; keep required approvals disabled until a second trusted maintainer exists, then verify the ruleset targets the default branch.
- [x] 4.3 Decide whether to disable the Wiki after confirming no intended documentation lives there, then verify the selected setting matches the documented collaboration model.

## 5. Validate the delivered collaboration layer

- [x] 5.1 Run `python -m unittest discover -s tests`, `python -m logseq_rig.release_validation fast`, `openspec validate --specs --strict --no-interactive`, and `git diff --check`, then verify all commands exit successfully.
- [x] 5.2 Review the rendered GitHub forms, pull-request template, CI result, and repository settings after merge, then verify the collaboration-governance spec scenarios are satisfied.
