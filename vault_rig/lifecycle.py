"""Safe, minimal lifecycle management for a detected Logseq vault."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile

from . import __version__
from .detection import detect


MANIFEST = ".vault-rig/manifest.json"
INCOMPLETE = ".vault-rig/incomplete.json"
BEGIN = "<!-- logseq-vault-rig:begin v1 -->\n"
END = "<!-- logseq-vault-rig:end -->\n"
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


def _payload(relative: str) -> str:
    return (PAYLOAD / relative).read_text(encoding="utf-8")


def _entries(root: Path, manifest: dict[str, object] | None = None) -> list[tuple[str, str, str]]:
    region = BEGIN + _payload("AGENTS.md") + END
    agents = root / "AGENTS.md"
    managed_paths = {entry["path"] for entry in manifest["entries"]} if manifest else None
    agents_mode = next((entry["mode"] for entry in manifest["entries"] if entry["path"] == "AGENTS.md"), None) if manifest else None
    if agents_mode == "file" or not agents.exists():
        managed, mode = region, "file"
    else:
        current = _region(agents.read_text(encoding="utf-8"))
        managed, mode = (agents.read_text(encoding="utf-8") + ("" if agents.read_text(encoding="utf-8").endswith("\n") else "\n") + region, "region") if current is None else (current[0] + region + current[2], "region")
    files = [("AGENTS.md", mode, managed)]
    files.extend((relative, "file", path.read_text(encoding="utf-8")) for path in PAYLOAD.rglob("*") if path.is_file() and path.name != "AGENTS.md" for relative in [path.relative_to(PAYLOAD).as_posix()] if not (root / relative).exists() or managed_paths is not None and relative in managed_paths)
    return files


def _safe_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise LifecycleError("unsafe managed path")
    path = (root / relative).resolve()
    if path.parent != root.resolve() and root.resolve() not in path.parents:
        raise LifecycleError("managed path escapes vault")
    return path


def _read_manifest(root: Path) -> dict[str, object] | None:
    path = root / MANIFEST
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise LifecycleError(f"invalid manifest: {error}") from error
    if not isinstance(value, dict) or set(value) != {"schema", "version", "entries"}:
        raise LifecycleError("invalid manifest schema")
    if value["schema"] != 1 or not isinstance(value["version"], str) or not isinstance(value["entries"], list):
        raise LifecycleError("invalid manifest schema")
    for entry in value["entries"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "mode", "sha256"} or entry.get("mode") not in {"file", "region"}:
            raise LifecycleError("invalid manifest entry")
        _safe_path(root, entry.get("path", ""))
        if not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64:
            raise LifecycleError("invalid manifest entry")
    return value


def _region(text: str) -> tuple[str, str, str] | None:
    starts, ends = text.count(BEGIN), text.count(END)
    if starts == ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise LifecycleError("managed region is malformed or duplicated")
    start, end = text.index(BEGIN), text.index(END) + len(END)
    if start > end:
        raise LifecycleError("managed region is malformed")
    return text[:start], text[start:end], text[end:]


def plan(root: Path, command: str) -> list[Action]:
    root = root.resolve()
    detect(root)
    manifest = _read_manifest(root)
    agents = root / "AGENTS.md"
    if command == "doctor":
        if (root / INCOMPLETE).exists():
            return [Action("incomplete", INCOMPLETE)]
        if manifest is None:
            return [Action("missing", MANIFEST)]
        result = [Action("version-mismatch", MANIFEST) for _ in []]
        if manifest["version"] != __version__:
            result.append(Action("version-mismatch", MANIFEST, str(manifest["version"])))
        for entry in manifest["entries"]:
            path = _safe_path(root, entry["path"])
            if not path.exists(): result.append(Action("missing", entry["path"]))
            elif entry["mode"] == "region":
                try: current = _region(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, LifecycleError): current = None
                if current is None or _digest(current[1]) != entry["sha256"]: result.append(Action("modified", entry["path"]))
            elif _digest(path.read_text(encoding="utf-8")) != entry["sha256"]: result.append(Action("modified", entry["path"]))
        return result or [Action("healthy", MANIFEST)]
    if command in {"install", "update"}:
        entries = _entries(root, manifest)
        if manifest is not None:
            state = plan(root, "doctor")
            if any(action.kind in {"missing", "modified"} for action in state):
                return [Action("conflict", action.path, action.kind) for action in state if action.kind in {"missing", "modified"}]
        if manifest is not None and manifest["version"] == __version__ and all((root / path).exists() and _digest((root / path).read_text(encoding="utf-8") if mode == "file" else (_region((root / path).read_text(encoding="utf-8")) or ("", "", ""))[1]) == _digest(content if mode == "file" else _region(content)[1]) for path, mode, content in entries):
            return [Action("noop", "AGENTS.md")]
        return [Action("region-edit" if entries[0][1] == "region" else "add", "AGENTS.md"), *[Action("replace", path) for path, _, _ in entries[1:]], Action("replace", MANIFEST)]
    if command == "uninstall":
        if manifest is None:
            return [Action("conflict", MANIFEST, "ownership is unproven")]
        entries = {entry["path"]: entry for entry in manifest["entries"]}
        entry = entries.pop("AGENTS.md", None)
        if not entry:
            return [Action("conflict", MANIFEST, "unsupported ownership record")]
        if not agents.exists(): return [Action("conflict", "AGENTS.md", "missing")]
        text = agents.read_text(encoding="utf-8")
        if entry["mode"] == "region":
            parsed = _region(text)
            if parsed is None or _digest(parsed[1]) != entry["sha256"]: return [Action("conflict", "AGENTS.md", "modified")]
            for path, extra in entries.items():
                target = root / path
                if not target.exists() or _digest(target.read_text(encoding="utf-8")) != extra["sha256"]: return [Action("conflict", path, "modified")]
            return [Action("region-edit", "AGENTS.md"), *[Action("remove", path) for path in sorted(entries)], Action("remove", MANIFEST)]
        if _digest(text) != entry["sha256"]: return [Action("conflict", "AGENTS.md", "modified")]
        for path, extra in entries.items():
            target = root / path
            if not target.exists() or _digest(target.read_text(encoding="utf-8")) != extra["sha256"]: return [Action("conflict", path, "modified")]
        return [Action("remove", "AGENTS.md"), *[Action("remove", path) for path in sorted(entries)], Action("remove", MANIFEST)]
    raise LifecycleError(f"unknown lifecycle command: {command}")


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".vault-rig-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as output:
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except BaseException:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def run(root: Path, command: str, dry_run: bool = False) -> list[Action]:
    root = root.resolve()
    actions = plan(root, command)
    if dry_run or any(action.kind == "conflict" for action in actions) or command == "doctor": return actions
    if command in {"install", "update"}:
        manifest = _read_manifest(root)
        entries = _entries(root, manifest)
        try:
            _atomic_write(root / INCOMPLETE, json.dumps({"operation": command}, sort_keys=True) + "\n")
            for path, _, content in entries: _atomic_write(root / path, content)
            manifest = {"schema": 1, "version": __version__, "entries": [{"path": path, "mode": mode, "sha256": _digest(_region(content)[1] if mode == "region" else content)} for path, mode, content in entries]}
            _atomic_write(root / MANIFEST, json.dumps(manifest, sort_keys=True, indent=2) + "\n")
            (root / INCOMPLETE).unlink()
        except OSError as error:
            raise LifecycleError("incomplete managed state; rerun doctor before retrying") from error
    elif command == "uninstall":
        manifest = _read_manifest(root)
        assert manifest is not None
        entries = {entry["path"]: entry for entry in manifest["entries"]}
        entry = entries.pop("AGENTS.md")
        agents = root / "AGENTS.md"
        _atomic_write(root / INCOMPLETE, json.dumps({"operation": command}, sort_keys=True) + "\n")
        if entry["mode"] == "region":
            before, _, after = _region(agents.read_text(encoding="utf-8")) or ("", "", "")
            _atomic_write(agents, before + after)
        else:
            agents.unlink()
        for path in entries: (root / path).unlink()
        (root / MANIFEST).unlink()
        (root / INCOMPLETE).unlink()
    return actions
