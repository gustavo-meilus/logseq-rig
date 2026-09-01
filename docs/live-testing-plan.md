# Live graph test plan

Use a disposable graph clone. Run `logseq-rig doctor <graph>`, retrieval commands, `check --all`, then `install`, `update`, and `uninstall`. Record unavailable live DataScript checks as unavailable.

For a legacy payload, install `logseq-rig`, run `logseq-rig update <graph>`, confirm doctor is healthy and the new hooks work, then optionally remove the legacy distribution.
