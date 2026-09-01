"""Offline fixture validation for release candidates."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from .__main__ import check_layout, main
from .lifecycle import CONFIG, LEGACY_BEGIN, LEGACY_CONFIG, LEGACY_END, LEGACY_MANIFEST, _digest, plan, run as lifecycle_run


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "release"


def _hashes(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(root.rglob("*")) if path.is_file()}


def _call(*args: str) -> tuple[int, object, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(args))
    return code, json.loads(out.getvalue()) if out.getvalue() else None, err.getvalue()


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def _hooks(root: Path) -> None:
    hooks = root / ".codex" / "hooks"
    def invoke(name: str, payload: dict[str, object], code: int) -> dict[str, object]:
        output = io.StringIO()
        result = type("Result", (), {"returncode": code})()
        with patch("sys.stdin", io.StringIO(json.dumps(payload))), patch("sys.stdout", output), patch("subprocess.run", return_value=result):
            runpy.run_path(hooks / name, run_name="__main__")
        return json.loads(output.getvalue())
    started = invoke("session_start.py", {"cwd": str(root), "source": "startup"}, 0)
    assert "Logseq Rig:" in started["hookSpecificOutput"]["additionalContext"]
    assert invoke("stop.py", {"cwd": str(root), "stop_hook_active": False}, 0) == {}
    assert invoke("stop.py", {"cwd": str(root), "stop_hook_active": False}, 1)["decision"] == "block"
    assert "unresolved" in invoke("stop.py", {"cwd": str(root), "stop_hook_active": True}, 1)["systemMessage"]


def _installed_cli() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        prefix = Path(temporary) / "installed"
        source = Path(temporary) / "source"
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "build", "__pycache__", "*.pyc"))
        executable = prefix / "Scripts" / "logseq-rig.exe"
        install = subprocess.run([sys.executable, "-m", "pip", "install", "--no-build-isolation", "--no-deps", "--no-index", "--no-cache-dir", "--prefix", str(prefix), str(source)], check=True, capture_output=True, text=True)
        environment = os.environ | {"PYTHONPATH": str(prefix / "Lib" / "site-packages")}
        if not executable.is_file() or subprocess.run([str(executable), "--help"], capture_output=True, text=True, env=environment).returncode:
            raise RuntimeError(f"installed logseq-rig command failed: {install.stderr}")


def _legacy_migration() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        graph = Path(temporary) / "graph"
        (graph / "logseq").mkdir(parents=True); (graph / "pages").mkdir(); (graph / "journals").mkdir()
        (graph / "logseq" / "config.edn").write_text("{}", encoding="utf-8")
        canonical = (graph / "logseq" / "config.edn").read_bytes()
        legacy_region = LEGACY_BEGIN + "legacy\n" + LEGACY_END
        (graph / "AGENTS.md").write_text(legacy_region, encoding="utf-8")
        (graph / ".vault-rig").mkdir()
        manifest = {"schema": 1, "version": "1.0.0", "entries": [{"path": "AGENTS.md", "mode": "region", "sha256": _digest(legacy_region)}]}
        (graph / LEGACY_MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        (graph / LEGACY_CONFIG).write_text('{"controlled_properties":{"state":["ok"]}}', encoding="utf-8")
        assert plan(graph, "doctor")[0].kind == "migration-required", "legacy doctor"
        assert lifecycle_run(graph, "update")[0].kind == "migrate", "legacy update"
        assert plan(graph, "doctor")[0].kind == "healthy", "migrated doctor"
        assert (graph / CONFIG).read_text(encoding="utf-8") == (graph / LEGACY_CONFIG).read_text(encoding="utf-8"), "legacy config"
        assert (graph / "logseq" / "config.edn").read_bytes() == canonical, "canonical graph changed"


def verify_fixture(source: Path, *, break_expectation: bool = False) -> None:
    expected = json.loads((source / "expected.json").read_text(encoding="utf-8"))
    protected = json.loads((source / "protected.json").read_text(encoding="utf-8"))["paths"]
    source_hashes = _hashes(source)
    with tempfile.TemporaryDirectory() as temporary:
        graph = Path(temporary) / source.name
        shutil.copytree(source / "graph", graph)
        _git(graph, "init"); _git(graph, "config", "user.email", "fixture@example.invalid"); _git(graph, "config", "user.name", "Fixture")
        _git(graph, "add", "."); _git(graph, "commit", "-m", "fixture")
        before = {path: hashlib.sha256((graph / path).read_bytes()).hexdigest() for path in protected}
        code, status, _ = _call("status", str(graph))
        assert code == 0 and status["result"]["pages"] == expected["pages"], "status pages"
        if "resolve" in expected:
            code, result, _ = _call("resolve", str(graph), expected["resolve"]["query"])
            assert code == 0 and result["result"]["page"] == expected["resolve"]["page"], "resolve"
        if "find" in expected:
            code, result, _ = _call("find", str(graph), expected["find"])
            assert code == 0 and result["result"], "find"
        if "block" in expected:
            code, result, _ = _call("block", str(graph), expected["block"])
            assert code == 0 and result["result"]["id"] == expected["block"], "block"
        if "refs" in expected:
            code, result, _ = _call("refs", str(graph), expected["refs"]["query"])
            assert code == 0 and len(result["result"]) == expected["refs"]["count"], "refs"
        code, result, _ = _call("install", str(graph)); assert code == 0 and result[0]["action"] in {"add", "region-edit"}, "install"
        code, result, _ = _call("install", str(graph)); assert code == 0 and result[0]["action"] == "noop", "second install"
        code, result, _ = _call("doctor", str(graph)); assert code == 0 and result[0]["action"] == "healthy", "doctor"
        code, result, _ = _call("update", str(graph), "--dry-run"); assert code == 0 and result[0]["action"] == "noop", "update simulation"
        code, result, _ = _call("check", str(graph), "--all"); assert code == 0 and result["status"] == "pass", "integrity"
        _hooks(graph)
        code, result, _ = _call("uninstall", str(graph)); assert code == 0, "uninstall"
        for path, digest in before.items():
            actual = hashlib.sha256((graph / path).read_bytes()).hexdigest()
            assert actual == digest, f"protected path changed: {path}"
        if break_expectation:
            assert expected["pages"] == -1, "intentional expectation mismatch"
    assert _hashes(source) == source_hashes, "source fixture changed"


def run(fixtures: list[Path], *, break_expectation: bool = False) -> None:
    for fixture in fixtures:
        try:
            verify_fixture(fixture, break_expectation=break_expectation)
        except (AssertionError, OSError, ValueError, subprocess.CalledProcessError) as error:
            raise RuntimeError(f"{fixture.name}: {error}") from error


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("fast", "check"))
    parser.add_argument("--fixture")
    parser.add_argument("--break-expectation", action="store_true")
    args = parser.parse_args(argv)
    fixtures = sorted(path for path in FIXTURES.iterdir() if path.is_dir())
    if args.fixture:
        fixtures = [path for path in fixtures if path.name == args.fixture]
    elif args.command == "fast":
        fixtures = fixtures[:1]
    if not fixtures:
        parser.error("unknown or missing fixture")
    try:
        if check_layout(ROOT): raise RuntimeError("repository layout")
        _installed_cli()
        _legacy_migration()
        if args.command == "fast":
            result = unittest.TextTestRunner(verbosity=0).run(unittest.defaultTestLoader.discover(ROOT / "tests"))
            if not result.wasSuccessful(): return 1
        run(fixtures, break_expectation=args.break_expectation)
    except RuntimeError as error:
        print(f"release validation failed: {error}", file=sys.stderr)
        return 1
    print(f"release validation passed: {', '.join(path.name for path in fixtures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
