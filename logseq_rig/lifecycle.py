"""Safe lifecycle management for a detected Logseq graph."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile

from . import __version__
from .detection import detect

MANIFEST = ".logseq-rig/manifest.json"
INCOMPLETE = ".logseq-rig/incomplete.json"
MIGRATION = ".logseq-rig/migration.json"
CONFIG = ".logseq-rig/integrity.json"
BEGIN, END = "<!-- logseq-rig:begin v1 -->\n", "<!-- logseq-rig:end -->\n"
LEGACY_MANIFEST = ".vault-rig/manifest.json"
LEGACY_INCOMPLETE = ".vault-rig/incomplete.json"
LEGACY_CONFIG = ".vault-rig/integrity.json"
LEGACY_BEGIN, LEGACY_END = "<!-- logseq-vault-rig:begin v1 -->\n", "<!-- logseq-vault-rig:end -->\n"
PAYLOAD = Path(__file__).parent.parent / "payload" / "codex"


class LifecycleError(Exception):
    pass


@dataclass(frozen=True)
class Action:
    kind: str
    path: str
    detail: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"action": self.kind, "path": self.path, "detail": self.detail}


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _safe_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise LifecycleError("unsafe managed path")
    path = (root / relative).resolve()
    if root.resolve() not in path.parents and path.parent != root.resolve():
        raise LifecycleError("managed path escapes graph")
    return path


def _region(text: str, begin: str = BEGIN, end: str = END) -> tuple[str, str, str] | None:
    if text.count(begin) == text.count(end) == 0:
        return None
    if text.count(begin) != 1 or text.count(end) != 1:
        raise LifecycleError("managed region is malformed or duplicated")
    start, finish = text.index(begin), text.index(end) + len(end)
    return text[:start], text[start:finish], text[finish:]


def _read_manifest(root: Path, relative: str = MANIFEST) -> dict[str, object] | None:
    path = root / relative
    if not path.exists(): return None
    try: value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: raise LifecycleError(f"invalid manifest: {error}") from error
    if not isinstance(value, dict) or set(value) != {"schema", "version", "entries"} or value.get("schema") != 1 or not isinstance(value.get("version"), str) or not isinstance(value.get("entries"), list):
        raise LifecycleError("invalid manifest schema")
    for entry in value["entries"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "mode", "sha256"} or entry["mode"] not in {"file", "region"} or not isinstance(entry["sha256"], str) or len(entry["sha256"]) != 64:
            raise LifecycleError("invalid manifest entry")
        _safe_path(root, entry["path"])
    return value


def _content(root: Path, entry: dict[str, object], begin: str = BEGIN, end: str = END) -> str | None:
    path = _safe_path(root, entry["path"])
    if not path.exists(): return None
    try:
        text = path.read_text(encoding="utf-8")
        return text if entry["mode"] == "file" else (_region(text, begin, end) or ("", "", ""))[1]
    except (OSError, UnicodeError, LifecycleError): return None


def _state(root: Path, manifest: dict[str, object], begin: str = BEGIN, end: str = END) -> list[Action]:
    result = []
    for entry in manifest["entries"]:
        text = _content(root, entry, begin, end)
        result.append(Action("missing" if text is None else "modified", entry["path"])) if text is None or _digest(text) != entry["sha256"] else None
    return result


def _payload(relative: str) -> str:
    return (PAYLOAD / relative).read_text(encoding="utf-8")


def _entries(root: Path, manifest: dict[str, object] | None = None) -> list[tuple[str, str, str]]:
    region, agents = BEGIN + _payload("AGENTS.md") + END, root / "AGENTS.md"
    known = {entry["path"] for entry in manifest["entries"]} if manifest else set()
    mode = next((entry["mode"] for entry in manifest["entries"] if entry["path"] == "AGENTS.md"), None) if manifest else None
    if mode == "file" or not agents.exists(): first = ("AGENTS.md", "file", region)
    else:
        text, found = agents.read_text(encoding="utf-8"), _region(agents.read_text(encoding="utf-8"))
        first = ("AGENTS.md", "region", text + ("" if text.endswith("\n") else "\n") + region if found is None else found[0] + region + found[2])
    result = [first]
    for path in PAYLOAD.rglob("*"):
        if path.is_file() and path.name != "AGENTS.md":
            relative = path.relative_to(PAYLOAD).as_posix()
            if not (root / relative).exists() or relative in known: result.append((relative, "file", path.read_text(encoding="utf-8")))
    return result


def _manifest(entries: list[tuple[str, str, str]]) -> str:
    value = {"schema": 1, "version": __version__, "entries": [{"path": path, "mode": mode, "sha256": _digest(_region(text)[1] if mode == "region" else text)} for path, mode, text in entries]}
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def _legacy_entries(root: Path, legacy: dict[str, object]) -> list[tuple[str, str, str]]:
    old = next((entry for entry in legacy["entries"] if entry["path"] == "AGENTS.md"), None)
    if old is None: raise LifecycleError("legacy ownership record lacks AGENTS.md")
    text = (root / "AGENTS.md").read_text(encoding="utf-8")
    if old["mode"] == "file":
        if _digest(text) != old["sha256"]: raise LifecycleError("legacy AGENTS.md is modified")
        first = ("AGENTS.md", "file", BEGIN + _payload("AGENTS.md") + END)
    else:
        found = _region(text, LEGACY_BEGIN, LEGACY_END)
        if found is None or _digest(found[1]) != old["sha256"]: raise LifecycleError("legacy AGENTS.md is modified")
        first = ("AGENTS.md", "region", found[0] + BEGIN + _payload("AGENTS.md") + END + found[2])
    old_paths, result = {entry["path"] for entry in legacy["entries"]}, [first]
    for path in PAYLOAD.rglob("*"):
        if path.is_file() and path.name != "AGENTS.md":
            relative = path.relative_to(PAYLOAD).as_posix()
            if (root / relative).exists() and relative not in old_paths: raise LifecycleError(f"destination collision: {relative}")
            result.append((relative, "file", path.read_text(encoding="utf-8")))
    return result


def _valid_config(path: Path) -> bool:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        rules = value.get("controlled_properties", {}) if isinstance(value, dict) else None
        return isinstance(rules, dict) and all(isinstance(key, str) and isinstance(values, list) and all(isinstance(item, str) for item in values) for key, values in rules.items())
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False


def _migration_conflicts(root: Path, legacy: dict[str, object]) -> list[Action]:
    if (root / LEGACY_INCOMPLETE).exists(): return [Action("conflict", LEGACY_INCOMPLETE, "legacy operation is incomplete")]
    state = _state(root, legacy, LEGACY_BEGIN, LEGACY_END)
    if state: return [Action("conflict", item.path, item.kind) for item in state]
    if (root / MANIFEST).exists() and not (root / MIGRATION).exists(): return [Action("conflict", MANIFEST, "active ownership already exists")]
    old, new = root / LEGACY_CONFIG, root / CONFIG
    if old.exists() and not _valid_config(old): return [Action("conflict", LEGACY_CONFIG, "invalid configuration")]
    if new.exists() and not _valid_config(new): return [Action("conflict", CONFIG, "invalid configuration")]
    if old.exists() and new.exists() and old.read_bytes() != new.read_bytes(): return [Action("conflict", CONFIG, "configuration differs")]
    try: _legacy_entries(root, legacy)
    except (LifecycleError, OSError, UnicodeError) as error: return [Action("conflict", LEGACY_MANIFEST, str(error))]
    return []


def plan(root: Path, command: str) -> list[Action]:
    root = root.resolve(); detect(root)
    active, legacy = _read_manifest(root), _read_manifest(root, LEGACY_MANIFEST)
    if command == "doctor":
        if (root / MIGRATION).exists() or (root / INCOMPLETE).exists(): return [Action("incomplete", MIGRATION if (root / MIGRATION).exists() else INCOMPLETE)]
        if active and legacy: return [Action("conflict", MANIFEST, "both active and legacy ownership exist")]
        if legacy: return _migration_conflicts(root, legacy) or [Action("migration-required", LEGACY_MANIFEST)]
        if not active: return [Action("missing", MANIFEST)]
        result = [Action("version-mismatch", MANIFEST, active["version"])] if active["version"] != __version__ else []
        return result + _state(root, active) or [Action("healthy", MANIFEST)]
    if command in {"install", "update"} and legacy:
        if command == "update" and (root / MIGRATION).exists() and active:
            return [Action("migrate", LEGACY_MANIFEST, MANIFEST)]
        conflicts = _migration_conflicts(root, legacy)
        return conflicts or ([Action("migrate", LEGACY_MANIFEST, MANIFEST)] if command == "update" else [Action("conflict", LEGACY_MANIFEST, "run update to migrate")])
    if command in {"install", "update"}:
        entries = _entries(root, active)
        if active and _state(root, active): return [Action("conflict", item.path, item.kind) for item in _state(root, active)]
        if active and active["version"] == __version__ and all((_content(root, {"path": path, "mode": mode}) or "") == (_region(text)[1] if mode == "region" else text) for path, mode, text in entries): return [Action("noop", "AGENTS.md")]
        return [Action("region-edit" if entries[0][1] == "region" else "add", "AGENTS.md"), *[Action("replace", path) for path, _, _ in entries[1:]], Action("replace", MANIFEST)]
    if command == "uninstall":
        if not active: return [Action("conflict", MANIFEST, "ownership is unproven")]
        state = _state(root, active)
        if state: return [Action("conflict", item.path, item.kind) for item in state]
        entries = {entry["path"]: entry for entry in active["entries"]}; agent = entries.pop("AGENTS.md", None)
        if not agent: return [Action("conflict", MANIFEST, "unsupported ownership record")]
        return [Action("region-edit" if agent["mode"] == "region" else "remove", "AGENTS.md"), *[Action("remove", path) for path in sorted(entries)], Action("remove", MANIFEST)]
    raise LifecycleError(f"unknown lifecycle command: {command}")


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".logseq-rig-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as output: output.write(text); output.flush(); os.fsync(output.fileno())
        os.replace(temporary, path)
    except BaseException:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def _migrate(root: Path, legacy: dict[str, object]) -> list[Action]:
    active = _read_manifest(root)
    if (root / MIGRATION).exists() and active:
        state = _state(root, active)
        if state: return [Action("conflict", item.path, item.kind) for item in state]
        active_paths = {entry["path"] for entry in active["entries"]}
        for entry in legacy["entries"]:
            path = root / entry["path"]
            if entry["path"] != "AGENTS.md" and entry["path"] not in active_paths and path.exists():
                text = _content(root, entry, LEGACY_BEGIN, LEGACY_END)
                if text is None or _digest(text) != entry["sha256"]: return [Action("conflict", entry["path"], "modified")]
                path.unlink()
        (root / LEGACY_MANIFEST).unlink(); (root / MIGRATION).unlink()
        return [Action("migrate", LEGACY_MANIFEST, MANIFEST)]
    conflicts = _migration_conflicts(root, legacy)
    if conflicts: return conflicts
    entries = _legacy_entries(root, legacy)
    try:
        _atomic_write(root / MIGRATION, '{"operation":"migration","phase":"write-active"}\n')
        for path, _, text in entries: _atomic_write(root / path, text)
        if (root / LEGACY_CONFIG).exists() and not (root / CONFIG).exists(): _atomic_write(root / CONFIG, (root / LEGACY_CONFIG).read_text(encoding="utf-8"))
        _atomic_write(root / MANIFEST, _manifest(entries)); _atomic_write(root / MIGRATION, '{"operation":"migration","phase":"cleanup"}\n')
        active_paths = {path for path, _, _ in entries}
        for entry in legacy["entries"]:
            path = root / entry["path"]
            if entry["path"] != "AGENTS.md" and entry["path"] not in active_paths and path.exists(): path.unlink()
        (root / LEGACY_MANIFEST).unlink(); (root / MIGRATION).unlink()
    except OSError as error: raise LifecycleError("incomplete managed migration; rerun update after doctor") from error
    return [Action("migrate", LEGACY_MANIFEST, MANIFEST)]


def run(root: Path, command: str, dry_run: bool = False) -> list[Action]:
    root = root.resolve(); actions = plan(root, command)
    if dry_run or command == "doctor" or any(action.kind == "conflict" for action in actions): return actions
    legacy = _read_manifest(root, LEGACY_MANIFEST)
    if command == "update" and legacy: return _migrate(root, legacy)
    if command in {"install", "update"}:
        entries = _entries(root, _read_manifest(root))
        try:
            _atomic_write(root / INCOMPLETE, json.dumps({"operation": command}) + "\n")
            for path, _, text in entries: _atomic_write(root / path, text)
            _atomic_write(root / MANIFEST, _manifest(entries)); (root / INCOMPLETE).unlink()
        except OSError as error: raise LifecycleError("incomplete managed state; rerun doctor before retrying") from error
    elif command == "uninstall":
        active = _read_manifest(root); assert active
        entries = {entry["path"]: entry for entry in active["entries"]}; agent = entries.pop("AGENTS.md"); agents = root / "AGENTS.md"
        _atomic_write(root / INCOMPLETE, '{"operation":"uninstall"}\n')
        if agent["mode"] == "region":
            before, _, after = _region(agents.read_text(encoding="utf-8")) or ("", "", ""); _atomic_write(agents, before + after)
        else: agents.unlink()
        for path in entries: (root / path).unlink()
        (root / MANIFEST).unlink(); (root / INCOMPLETE).unlink()
    return actions
