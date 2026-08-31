## 1. Fixture Corpus

- [x] 1.1 Create separate minimal synthetic fixtures for default layout, custom directories/journal format, aliases/namespaces, nested blocks/properties, persisted refs, assets, and pre-existing Codex configuration, then verify the corpus contains no private data.
- [x] 1.2 Add expected machine-readable outcomes and protected-path manifests per fixture, then verify every supported behavior class has one explicit oracle.

## 2. Disposable Harness

- [x] 2.1 Implement fixture copying, temporary Git setup, content hashing, and diff reporting with the Python standard library, then verify source fixtures remain unchanged after an intentionally failing run.
- [x] 2.2 Implement the stable check-fast entrypoint for layout, unit, and selected fixture checks, then verify it returns non-zero with a focused diagnostic when one expectation is broken.

## 3. Authoritative Release Check

- [x] 3.1 Implement the full check entrypoint to run install twice, doctor, update simulation, retrieval, integrity checks, and uninstall on clean fixture copies, then verify the complete healthy corpus passes offline.
- [x] 3.2 Add canonical and user-owned content preservation assertions, then verify an unexpected note or root-configuration mutation fails with the exact path.
- [x] 3.3 Add SessionStart and Stop pass/first-fail/second-fail fixture scenarios, then verify hook behavior is deterministic and independent of model judgment.

## 4. Release Use

- [x] 4.1 Document check-fast for iteration and check as the release gate without selecting a CI provider, then verify both commands run from a fresh checkout with Python 3.11+ and Git only.
