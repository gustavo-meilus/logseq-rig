## 1. Ownership Model

- [ ] 1.1 Define the JSON manifest schema for versions, relative paths, ownership modes, and SHA-256 identities, then verify valid round trips and rejection of unsafe or unknown entries.
- [ ] 1.2 Implement bounded managed-region parsing for shared text files, then verify absent, valid, duplicate, malformed, and locally changed marker cases preserve surrounding bytes.

## 2. Planning and Execution

- [ ] 2.1 Implement one plan builder for install, update, and uninstall actions, then verify dry-run serializes deterministic add, replace, region-edit, conflict, and remove results without filesystem changes.
- [ ] 2.2 Implement staged managed writes and atomic replacement with canonical-path guards, then verify injected failure leaves canonical fixture hashes unchanged and reports incomplete managed state.

## 3. Lifecycle Commands

- [ ] 3.1 Implement install and repeat-install behavior, then verify a clean fixture receives the expected manifest and a second install produces no changes.
- [ ] 3.2 Implement doctor state classification, then verify healthy, missing, modified, and version-mismatched fixtures are reported without mutation.
- [ ] 3.3 Implement update conflict handling and uninstall ownership checks, then verify local managed edits are preserved and pre-existing root instructions survive uninstall.

## 4. Integration Verification

- [ ] 4.1 Run lifecycle tests across default and custom detected vault fixtures, then verify dry-run, install, update, doctor, and uninstall satisfy the full vault-lifecycle spec.
