# Logseq Rig

Logseq Rig is a stdlib-only local control layer for Logseq OG graphs. Markdown and Git remain authoritative while deterministic retrieval, lifecycle, and integrity commands protect graph invariants.

## Commands

```text
python -m logseq_rig --help
python -m logseq_rig detect /path/to/graph
python -m logseq_rig install /path/to/graph
python -m logseq_rig update /path/to/graph
python -m logseq_rig doctor /path/to/graph
python -m logseq_rig check /path/to/graph --changed
```

The optional DataScript bridge reads only loopback endpoints configured by:

```text
LOGSEQ_RIG_LOGSEQ_ENDPOINT=http://127.0.0.1:1234/query
LOGSEQ_RIG_LOGSEQ_TOKEN=local-token
```

Upgrade an installed legacy payload by installing `logseq-rig`, running `logseq-rig doctor <graph>`, then `logseq-rig update <graph>`. Verify the new hooks before optionally removing the legacy distribution.

Run `python -m logseq_rig.release_validation check` before release.
