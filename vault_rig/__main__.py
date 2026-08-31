"""Command-line entrypoint for Vault Rig."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__


REQUIRED_PATHS = ("vault_rig", "payload", "tests/fixtures", "docs", ".agents/skills")
FORBIDDEN_PATHS = ("payload/pages", "payload/journals", "payload/assets", "payload/logseq/config.edn")


def check_layout(root: Path) -> list[str]:
    """Return deterministic layout-contract violations for *root*."""
    missing = [f"missing required path: {path}" for path in REQUIRED_PATHS if not (root / path).exists()]
    forbidden = [f"forbidden vault-owned path: {path}" for path in FORBIDDEN_PATHS if (root / path).exists()]
    return missing + forbidden


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage Vault Rig project boundaries.")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--check-layout", metavar="ROOT", nargs="?", const=".", help="validate a repository layout")
    args = parser.parse_args(argv)

    if args.check_layout is None:
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
