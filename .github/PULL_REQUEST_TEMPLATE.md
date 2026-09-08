## Change

Describe the problem and the smallest change that solves it.

## Verification

- [ ] I ran the affected tests and recorded the result below.
- [ ] I ran `python -m logseq_rig.release_validation check` when applicable.
- [ ] I ran `git diff --check`.

Verification evidence:

## Documentation and OpenSpec

- [ ] Documentation is updated, or no documentation change is needed.
- [ ] OpenSpec artifacts are updated for behavior changes, or this change is docs-only/maintenance.

## Graph safety

- [ ] No personal-graph data, credentials, or raw query output is included.
- [ ] Canonical Markdown, assets, and Logseq configuration remain graph-owned.
- [ ] Managed payload ownership is unchanged, or the change has an approved OpenSpec contract.
