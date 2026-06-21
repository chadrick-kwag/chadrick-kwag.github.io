"""Command-line entry point for inventory and recovery operations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.recover.inventory import snapshot_and_sync, write_manifest
from tools.recover.io import write_json_atomic
from tools.recover.pipeline import recover_all
from tools.recover.validate import validate_recovery


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tools.recover")
    commands = parser.add_subparsers(dest="command", required=True)

    inventory = commands.add_parser("inventory")
    inventory.add_argument("--bucket", required=True)
    inventory.add_argument("--backup", required=True, type=Path)
    inventory.add_argument("--manifest", required=True, type=Path)

    recover = commands.add_parser("recover")
    recover.add_argument("--backup", required=True, type=Path)
    recover.add_argument("--site", required=True, type=Path)
    recover.add_argument("--report", required=True, type=Path)

    validate = commands.add_parser("validate")
    validate.add_argument("--site", required=True, type=Path)
    validate.add_argument("--expected-count", required=True, type=int)
    validate.add_argument("--report", required=True, type=Path)
    return parser


def _inventory(args: argparse.Namespace) -> int:
    records, comparison = snapshot_and_sync(args.bucket, args.backup)
    write_manifest(args.manifest, args.bucket, records, comparison)
    return int(bool(
        comparison.missing or comparison.size_mismatches or comparison.extra
    ))


def _recover(args: argparse.Namespace) -> int:
    report = recover_all(args.backup / "posts", args.site / "content/posts")
    write_json_atomic(args.report, report)
    incomplete = (
        report["failure_count"]
        or report["source_count"] != report["success_count"]
        or report["stale_failures"]
        or report["cleanup_failures"]
        or any(article.get("missing_assets") for article in report["articles"])
    )
    return int(bool(incomplete))


def _validate(args: argparse.Namespace) -> int:
    report = validate_recovery(
        args.site / "content/posts", args.expected_count
    )
    write_json_atomic(args.report, report)
    return int(not report["valid"])


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "inventory":
            return _inventory(args)
        if args.command == "recover":
            return _recover(args)
        return _validate(args)
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
