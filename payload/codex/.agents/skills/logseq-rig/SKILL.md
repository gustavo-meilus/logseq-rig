---
name: logseq-rig
description: Retrieve, edit, or verify knowledge in a supported Logseq OG graph.
---

Start with `logseq-rig status <graph>`. Use `resolve`, `find`, and `context` to retrieve evidence before editing. Preserve persisted IDs, block refs, properties, and asset paths. After editing canonical Markdown, run `logseq-rig check <graph> --changed`; report its JSON findings if it fails. Use `logseq-rig check <graph> --all` only when the task requires a full graph check.
