"""Command-line entrypoint for Logseq Vault Rig."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .detection import DetectionError, detect
from .lifecycle import LifecycleError, run
from .integrity import check
from .retrieval import RetrievalError, backlinks, block, context, find, history, load, page_evidence, refs, resolve
from .datascript import QueryError, execute


REQUIRED_PATHS = ("vault_rig", "payload", "tests/fixtures", "docs", ".agents/skills")
FORBIDDEN_PATHS = ("payload/pages", "payload/journals", "payload/assets", "payload/logseq/config.edn")


def check_layout(root: Path) -> list[str]:
    """Return deterministic layout-contract violations for *root*."""
    missing = [f"missing required path: {path}" for path in REQUIRED_PATHS if not (root / path).exists()]
    forbidden = [f"forbidden vault-owned path: {path}" for path in FORBIDDEN_PATHS if (root / path).exists()]
    return missing + forbidden


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage Logseq Vault Rig project boundaries.")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--check-layout", metavar="ROOT", nargs="?", const=".", help="validate a repository layout")
    parser.add_argument("command", nargs="?", choices=("detect", "install", "update", "doctor", "uninstall", "check", "status", "resolve", "find", "context", "page", "block", "refs", "backlinks", "history", "query"))
    parser.add_argument("target", nargs="?")
    parser.add_argument("query", nargs="?")
    parser.add_argument("arguments", nargs="*")
    parser.add_argument("--children", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true", help="show lifecycle changes without writing")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--all", action="store_true", help="check the full graph")
    modes.add_argument("--changed", action="store_true", help="check Git-changed graph files")
    parser.add_argument("--expected-path", action="append", default=[], help="declared changed path allowed by changed mode")
    args = parser.parse_args(argv)

    if args.check_layout is None:
        if args.command == "detect":
            if args.target is None:
                parser.error("detect requires a target folder")
            try:
                print(json.dumps(detect(Path(args.target)).to_dict(), sort_keys=True))
                return 0
            except DetectionError as error:
                print(json.dumps({"code": error.code, "message": error.message}, sort_keys=True), file=sys.stderr)
                return 2
        if args.command == "check":
            if args.target is None or args.all == args.changed:
                parser.error("check requires a vault folder and exactly one of --all or --changed")
            try:
                result = check(detect(Path(args.target)), "all" if args.all else "changed", tuple(args.expected_path))
                print(json.dumps(result, sort_keys=True))
                return 1 if result["status"] == "integrity_failure" else 0
            except RuntimeError as error:
                print(json.dumps({"status": "capability_error", "code": "git_unavailable", "message": str(error)}, sort_keys=True), file=sys.stderr)
                return 2
            except (DetectionError, OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
                print(json.dumps({"status": "capability_error", "code": getattr(error, "code", "integrity_error"), "message": str(error)}, sort_keys=True), file=sys.stderr)
                return 2
        if args.command in {"status", "resolve", "find", "context", "page", "block", "refs", "backlinks", "history", "query"}:
            if args.target is None:
                parser.error(f"{args.command} requires a vault folder")
            if args.command != "status" and args.query is None:
                parser.error(f"{args.command} requires a query")
            try:
                descriptor = detect(Path(args.target))
                pages = load(descriptor)
                if args.command == "status": result = {"descriptor": descriptor.to_dict(), "pages": len(pages)}
                elif args.command == "query": result = execute(args.query, args.arguments, pages)
                elif args.command == "resolve": result = page_evidence(resolve(pages, args.query))
                elif args.command == "find": result = find(pages, args.query)
                elif args.command == "context": result = context(pages, args.query, max(0, args.children))
                elif args.command == "page": result = page_evidence(resolve(pages, args.query))
                elif args.command == "block": result = block(pages, args.query)
                elif args.command == "refs": result = refs(pages, args.query)
                elif args.command == "backlinks": result = backlinks(pages, args.query)
                else: result = history(descriptor, args.query, pages)
                print(json.dumps({"command": args.command, "result": result}, sort_keys=True))
                return 0
            except (DetectionError, RetrievalError, QueryError, OSError, UnicodeError) as error:
                print(json.dumps({"code": getattr(error, "code", "retrieval_error"), "message": str(error)}, sort_keys=True), file=sys.stderr)
                return 2
        if args.command in {"install", "update", "doctor", "uninstall"}:
            if args.target is None:
                parser.error(f"{args.command} requires a target folder")
            try:
                actions = run(Path(args.target), args.command, args.dry_run)
                print(json.dumps([action.to_dict() for action in actions], sort_keys=True))
                return 2 if any(action.kind == "conflict" for action in actions) else 0
            except (DetectionError, LifecycleError) as error:
                code = getattr(error, "code", "lifecycle_error")
                print(json.dumps({"code": code, "message": str(error)}, sort_keys=True), file=sys.stderr)
                return 2
        parser.print_help()
        return 0

    errors = check_layout(Path(args.check_layout))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("layout OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
