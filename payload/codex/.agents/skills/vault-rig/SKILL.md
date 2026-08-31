---
name: vault-rig
description: Retrieve, edit, or verify knowledge in a supported Logseq OG vault.
---

Start with `vault-rig status <vault>`. Use `resolve`, `find`, and `context` to retrieve evidence before editing. Preserve persisted IDs, block refs, properties, and asset paths. After editing canonical Markdown, run `vault-rig check <vault> --changed`; report its JSON findings if it fails. Use `vault-rig check <vault> --all` only when the task requires a full graph check.
