## 1. Establish the active public contract

- [x] 1.1 Rename the distribution, package directory/imports, console entrypoint, managed namespace, payload Skill path, environment variables, fixtures, and active terminology to the approved Logseq Rig/Graph names; verify `python -m logseq_rig --help` and the renamed layout check succeed.
- [x] 1.2 Rename public descriptor/diagnostic terminology and all active source, test, documentation, and current-spec references without changing retrieval, detection, integrity, or DataScript semantics; verify a scoped terminology scan has no old terms outside approved legacy migration coverage and historical records.
- [x] 1.3 Align active main-spec capability paths and headings with Graph terminology through the applicable OpenSpec synchronization/finalization workflow, preserving archived and stale proposal history; verify `openspec validate --specs --strict --no-interactive` passes.

## 2. Implement safe legacy managed-payload migration

- [x] 2.1 Add ownership-proven legacy detection and dry-run/doctor reporting for clean, modified, malformed, incomplete, duplicate-marker, dual-namespace, and destination-collision states; verify each unsafe state produces a no-write diagnostic.
- [x] 2.2 Make `update` migrate only a clean legacy managed payload into the active namespace using a durable, resumable migration phase record; verify injected failures at each migration phase recover deterministically without modifying canonical graph files.
- [x] 2.3 Preserve controlled-property configuration by copying one valid legacy configuration only when no conflicting active configuration exists, without deleting user-owned legacy configuration; verify matching rules remain enforced and disagreements conflict without writes.
- [x] 2.4 Update install, update, doctor, uninstall, payload markers, Skill, and hooks for the active name family while preserving hash-based ownership and idempotence; verify a migrated graph is healthy, its hooks invoke the renamed command, and uninstall removes only proven active managed state.

## 3. Extend deterministic verification

- [x] 3.1 Rename existing unit-test helpers and release fixtures to Graph terminology and add focused lifecycle regression cases for clean migration, every conflict class, resumable interruption, configuration preservation, and post-migration uninstall; verify the affected tests pass.
- [x] 3.2 Extend offline release validation with disposable fresh-install and legacy-migration fixtures plus an installed-package check in a temporary environment; verify the `logseq-rig` executable, hooks, lifecycle round trip, and canonical-content hashes pass without network or private graph content.
- [x] 3.3 Run `python -m unittest discover -s tests`, `python -m logseq_rig.release_validation check`, `git diff --check`, and strict OpenSpec validation; verify all commands pass against the final worktree.

## 4. Publish the rebrand safely

- [x] 4.1 Update active upgrade/release documentation with the required order: install `logseq-rig`, run doctor and update, verify hooks, then optionally remove the old distribution; verify the documented commands work in the installed-package check.
- [x] 4.2 After repository validation, rename the GitHub repository, update the local `origin` URL and checkout name, and update known external repository/action/package references; verify fetch/push use the new remote and external action consumers do not rely on redirects.
