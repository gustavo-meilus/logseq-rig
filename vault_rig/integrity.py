"""Deterministic, read-only integrity checks for supported vault files."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess

from .detection import VaultDescriptor
from .retrieval import BLOCK_REF, PROPERTY, load


UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.I)
ASSET = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Location:
    file: str
    line: int

    def to_dict(self) -> dict[str, object]:
        return {"file": self.file, "line": self.line}


def _finding(code: str, source: Location, message: str, related: list[Location] | None = None, severity: str = "error") -> dict[str, object]:
    return {"code": code, "severity": severity, "source": source.to_dict(), "related": [item.to_dict() for item in related or []], "message": message}


def _controlled(root: Path) -> dict[str, set[str]]:
    path = root / ".vault-rig" / "integrity.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    rules = value.get("controlled_properties", {})
    if not isinstance(rules, dict) or not all(isinstance(key, str) and isinstance(values, list) and all(isinstance(item, str) for item in values) for key, values in rules.items()):
        raise ValueError("invalid controlled-property configuration")
    return {key: set(values) for key, values in rules.items()}


def _changed(descriptor: VaultDescriptor) -> tuple[set[str], dict[str, set[str]]]:
    root = Path(descriptor.root)
    try:
        tracked = subprocess.run(["git", "-C", str(root), "diff", "--name-only", "HEAD"], text=True, capture_output=True, check=True).stdout.splitlines()
        untracked = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"], text=True, capture_output=True, check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError) as error:
        raise RuntimeError("Git changed-file selection is unavailable") from error
    changed = {path.replace("\\", "/") for path in [*tracked, *untracked]}
    prefixes = (descriptor.pages_directory + "/", descriptor.journals_directory + "/")
    changed = {path for path in changed if path.startswith(prefixes) and path.endswith(".md")}
    deleted: dict[str, set[str]] = defaultdict(set)
    for path in changed:
        diff = subprocess.run(["git", "-C", str(root), "diff", "HEAD", "--", path], text=True, capture_output=True).stdout
        deleted[path].update(match["value"] for line in diff.splitlines() if line.startswith("-") and not line.startswith("---") for match in [PROPERTY.match(line[1:])] if match and match["key"] == "id")
    return changed, deleted


def check(descriptor: VaultDescriptor, mode: str, expected_paths: tuple[str, ...] = ()) -> dict[str, object]:
    """Return deterministic findings for *descriptor* without changing files."""
    root = Path(descriptor.root)
    pages = load(descriptor)
    selected: set[str] | None = None
    deleted: dict[str, set[str]] = {}
    if mode == "changed":
        selected, deleted = _changed(descriptor)
    controlled = _controlled(root)
    ids: dict[str, list[Location]] = defaultdict(list)
    refs: list[tuple[str, Location]] = []
    properties: list[tuple[str, str, Location]] = []
    assets: list[tuple[str, Location]] = []
    for page in pages:
        path = root / page.path
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            location = Location(page.path, line_number)
            match = PROPERTY.match(line)
            if match:
                properties.append((match["key"], match["value"], location))
                if match["key"] == "id": ids[match["value"]].append(location)
            refs.extend((identifier, location) for identifier in BLOCK_REF.findall(line))
            for raw in ASSET.findall(line):
                target = raw.split("#", 1)[0]
                if target and not "://" in target and (target.startswith("assets/") or target.startswith("../assets/")):
                    assets.append((target, location))
    active = lambda location: selected is None or location.file in selected
    findings: list[dict[str, object]] = []
    for identifier, locations in sorted(ids.items()):
        if not UUID.fullmatch(identifier):
            findings.extend(_finding("invalid_persisted_id", location, f"invalid persisted id: {identifier}") for location in locations if active(location))
        elif len(locations) > 1 and any(active(location) for location in locations):
            findings.append(_finding("duplicate_persisted_id", next(location for location in locations if active(location)), f"duplicate persisted id: {identifier}", locations))
    for identifier, location in refs:
        if active(location) and identifier not in ids:
            findings.append(_finding("missing_block_target", location, f"missing persisted block target: {identifier}"))
    for path, identifiers in deleted.items():
        for identifier in sorted(identifiers):
            remaining = [location for reference, location in refs if reference == identifier]
            if remaining:
                findings.append(_finding("referenced_block_deleted", Location(path, 1), f"deleted persisted block is still referenced: {identifier}", remaining))
    for target, location in assets:
        resolved = (root / location.file).parent.joinpath(target).resolve()
        if active(location) and root.resolve() in (resolved, *resolved.parents) and not resolved.exists():
            findings.append(_finding("missing_local_asset", location, f"missing local asset: {resolved.relative_to(root).as_posix()}"))
    for key, value, location in properties:
        if active(location) and key in controlled and value not in controlled[key]:
            findings.append(_finding("invalid_controlled_property", location, f"unsupported value for {key}: {value}"))
    if selected is not None and expected_paths:
        allowed = set(expected_paths)
        for path in sorted(selected - allowed):
            findings.append(_finding("unexpected_changed_file", Location(path, 1), f"changed file is outside declared mutation scope: {path}", severity="warning"))
    findings.sort(key=lambda item: (item["source"]["file"], item["source"]["line"], item["code"]))
    errors = [item for item in findings if item["severity"] == "error"]
    return {"status": "integrity_failure" if errors else "warning" if findings else "pass", "mode": mode, "findings": findings}
