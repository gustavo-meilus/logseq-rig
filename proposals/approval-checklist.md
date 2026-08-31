# Approval Checklist

Use this checklist before turning any normalized contract into an OpenSpec change.

- [ ] The change has one cohesive outcome.
- [ ] Its dependencies are approved/available or intentionally deferred.
- [ ] In-scope and out-of-scope boundaries match the intended release.
- [ ] Acceptance cases are observable and do not prescribe unnecessary implementation details.
- [ ] Canonical Logseq OG Markdown remains protected.
- [ ] Compatibility and uninstall/update behavior are explicit where relevant.
- [ ] Any vault-specific unknown that can materially change behavior is either resolved or remains an explicit open question.
- [ ] Optional semantic/MCP mechanisms have evidence that the simpler core is insufficient.
- [ ] The complete contract has explicit user approval.

After approval and once an OpenSpec context exists:

```bash
openspec context --json
openspec new change "<name>"
openspec status --change "<name>" --json
# Follow the resolved artifact graph/instructions.
openspec validate "<name>" --strict
```
