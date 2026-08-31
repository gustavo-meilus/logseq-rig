# Live vault test plan

Test the installed vault without changing canonical knowledge. Use a disposable clone for lifecycle mutations.

## Tactic switch

| Scope | Route | Owner | Pass condition |
| --- | --- | --- | --- |
| Installed vault read-only checks | R0 | Operator | Every command returns expected JSON and `doctor` is healthy. |
| Staging install/update/uninstall | R1 | Operator, then fresh verifier | Managed files change only as planned; clone's canonical content is unchanged. |
| Optional DataScript | R0 | Operator | A configured local bridge returns registered-query evidence; otherwise record `unavailable`. |

## 1. Preflight

Run from a known `logseq-vrig` checkout and record its `HEAD`; never place tokens in logs or test notes.

```powershell
$vault = '<vault-path>'
git -C $vault status --short
python -m vault_rig doctor $vault
python -m vault_rig status $vault
```

Expected: `doctor` reports `healthy`; `status` returns the detected vault descriptor and page count. Stop if the vault has unexpected Git changes or the descriptor is wrong.

## 2. Read-only retrieval and integrity

Choose a known page title and a known unique phrase; do not invent or edit vault content for this phase.

```powershell
python -m vault_rig resolve $vault '<page-title>'
python -m vault_rig find $vault '<unique-phrase>'
python -m vault_rig context $vault '<unique-phrase>' --children 1
python -m vault_rig check $vault --all
python -m vault_rig install $vault --dry-run
python -m vault_rig update $vault --dry-run
```

Expected: retrieval results contain file, line, page, and block evidence; integrity returns `pass`; both lifecycle dry runs return `noop`. Save command exit codes and redacted JSON summaries only.

## 3. Codex session smoke test

With Logseq closed, open Codex in the vault directory. Ask one read-only question answered by the commands above. Confirm SessionStart context is bounded, the installed `AGENTS.md` routes retrieval through `vault-rig`, and no canonical files change. Do not turn an unavailable manual host check into a passed result; record it as `unavailable` if Codex cannot run.

## 4. Isolated lifecycle round trip

Clone the vault repository outside the live vault, then test managed payload ownership there. This is the R1 boundary: a fresh verifier inspects the clone's final Git diff and the command evidence.

```powershell
$stage = Join-Path ([System.IO.Path]::GetTempPath()) ("logseq-vrig-live-stage-" + [guid]::NewGuid())
git clone --no-local $vault $stage
$agentsBefore = if (Test-Path "$stage\AGENTS.md") { (Get-FileHash "$stage\AGENTS.md").Hash } else { 'absent' }
python -m vault_rig install $stage
python -m vault_rig install $stage
python -m vault_rig doctor $stage
python -m vault_rig update $stage --dry-run
python -m vault_rig uninstall $stage
$agentsAfter = if (Test-Path "$stage\AGENTS.md") { (Get-FileHash "$stage\AGENTS.md").Hash } else { 'absent' }
$agentsBefore -eq $agentsAfter
git -C $stage diff --check
```

Expected: first install plans only managed paths, second install is `noop`, `doctor` is `healthy`, update is `noop`, uninstall removes only owned payload, and the verifier finds no page, journal, asset, configuration, or pre-existing instruction changes.

## 5. Optional live DataScript

Run only with a supported local Logseq endpoint and a locally supplied token. Confirm endpoint is loopback-only, then use a registered query with a real page title.

```powershell
python -m vault_rig query $vault page-by-name '<page-title>'
```

Expected: output identifies the query version and resolved evidence. If Logseq, endpoint, token, or supported API is unavailable, record `unavailable`; core acceptance remains based on sections 1–4.

## 6. Closeout

Record source `HEAD`, vault `HEAD`, commands, exit codes, redacted result summaries, route used, and any unavailable checks. A failed R0 check blocks usage acceptance. A failed R1 verification returns one correction to the operator; a second failure is `BLOCKED` with its cause.

## Continuation after a lifecycle defect

Fix and run the focused round-trip regression first, then the repository gates. A fresh verifier reviews the source change. Only after that `PASS`, repeat section 4 in a new disposable clone; a fresh verifier then accepts the live lifecycle evidence. The installed vault remains read-only throughout; the unavailable DataScript check stays `unavailable`.
