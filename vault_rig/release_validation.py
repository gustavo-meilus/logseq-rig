"""Offline fixture validation for release candidates."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from .__main__ import check_layout, main


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
    assert "Vault Rig:" in started["hookSpecificOutput"]["additionalContext"]
    assert invoke("stop.py", {"cwd": str(root), "stop_hook_active": False}, 0) == {}
    assert invoke("stop.py", {"cwd": str(root), "stop_hook_active": False}, 1)["decision"] == "block"
    assert "unresolved" in invoke("stop.py", {"cwd": str(root), "stop_hook_active": True}, 1)["systemMessage"]


def verify_fixture(source: Path, *, break_expectation: bool = False) -> None:
    expected = json.loads((source / "expected.json").read_text(encoding="utf-8"))
    protected = json.loads((source / "protected.json").read_text(encoding="utf-8"))["paths"]
    source_hashes = _hashes(source)
    with tempfile.TemporaryDirectory() as temporary:
        vault = Path(temporary) / source.name
        shutil.copytree(source / "vault", vault)
        _git(vault, "init"); _git(vault, "config", "user.email", "fixture@example.invalid"); _git(vault, "config", "user.name", "Fixture")
        _git(vault, "add", "."); _git(vault, "commit", "-m", "fixture")
        before = {path: hashlib.sha256((vault / path).read_bytes()).hexdigest() for path in protected}
        code, status, _ = _call("status", str(vault))
        assert code == 0 and status["result"]["pages"] == expected["pages"], "status pages"
        if "resolve" in expected:
            code, result, _ = _call("resolve", str(vault), expected["resolve"]["query"])
            assert code == 0 and result["result"]["page"] == expected["resolve"]["page"], "resolve"
        if "find" in expected:
            code, result, _ = _call("find", str(vault), expected["find"])
            assert code == 0 and result["result"], "find"
        if "block" in expected:
            code, result, _ = _call("block", str(vault), expected["block"])
            assert code == 0 and result["result"]["id"] == expected["block"], "block"
        if "refs" in expected:
            code, result, _ = _call("refs", str(vault), expected["refs"]["query"])
            assert code == 0 and len(result["result"]) == expected["refs"]["count"], "refs"
        code, result, _ = _call("install", str(vault)); assert code == 0 and result[0]["action"] in {"add", "region-edit"}, "install"
        code, result, _ = _call("install", str(vault)); assert code == 0 and result[0]["action"] == "noop", "second install"
        code, result, _ = _call("doctor", str(vault)); assert code == 0 and result[0]["action"] == "healthy", "doctor"
        code, result, _ = _call("update", str(vault), "--dry-run"); assert code == 0 and result[0]["action"] == "noop", "update simulation"
        code, result, _ = _call("check", str(vault), "--all"); assert code == 0 and result["status"] == "pass", "integrity"
        _hooks(vault)
        code, result, _ = _call("uninstall", str(vault)); assert code == 0, "uninstall"
        for path, digest in before.items():
            actual = hashlib.sha256((vault / path).read_bytes()).hexdigest()
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
