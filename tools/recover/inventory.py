"""Inventory and verify an S3 backup downloaded with the AWS CLI."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from tools.recover.io import write_json_atomic


@dataclass(frozen=True)
class ObjectRecord:
    key: str
    size: int
    etag: str
    last_modified: str | None


@dataclass(frozen=True)
class BackupComparison:
    missing: list[str]
    size_mismatches: list[str]
    extra: list[str]
    sha256: dict[str, str]


def list_s3_objects(bucket: str) -> list[ObjectRecord]:
    """Return the objects reported by ``aws s3api list-objects-v2``."""
    result = subprocess.run(
        [
            "aws",
            "s3api",
            "list-objects-v2",
            "--bucket",
            bucket,
            "--query",
            "Contents[].{key:Key,size:Size,etag:ETag,last_modified:LastModified}",
            "--output",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    objects = json.loads(result.stdout) or []
    return [ObjectRecord(**item) for item in objects]


def sync_bucket(bucket: str, destination: str | Path) -> None:
    """Synchronize an S3 bucket into a local directory."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "aws",
            "s3",
            "sync",
            f"s3://{bucket}",
            str(destination),
            "--exact-timestamps",
        ],
        check=True,
    )


def compare_remote_snapshots(
    before: list[ObjectRecord], after: list[ObjectRecord]
) -> list[str]:
    """Return keys whose remote identity differs between two inventories."""
    before_by_key = {record.key: record for record in before}
    after_by_key = {record.key: record for record in after}
    changed = before_by_key.keys() ^ after_by_key.keys()
    changed.update(
        key
        for key in before_by_key.keys() & after_by_key.keys()
        if (
            before_by_key[key].size,
            before_by_key[key].etag,
        )
        != (
            after_by_key[key].size,
            after_by_key[key].etag,
        )
    )
    return sorted(changed)


def snapshot_and_sync(
    bucket: str, destination: str | Path
) -> tuple[list[ObjectRecord], BackupComparison]:
    """Sync a bucket only if its inventory remains stable during transfer."""
    before = list_s3_objects(bucket)
    sync_bucket(bucket, destination)
    after = list_s3_objects(bucket)
    changed = compare_remote_snapshots(before, after)
    if changed:
        raise RuntimeError(
            "S3 bucket changed during sync: " + ", ".join(changed)
        )
    comparison = compare_backup(destination, before)
    return before, comparison


def compare_backup(
    root: str | Path, records: list[ObjectRecord]
) -> BackupComparison:
    """Compare downloaded files with inventory records and hash present objects."""
    root = Path(root)
    paths = list(root.rglob("*"))
    symlinks = {
        path.relative_to(root).as_posix() for path in paths if path.is_symlink()
    }
    actual = {
        path.relative_to(root).as_posix(): path
        for path in paths
        if not path.is_symlink() and path.is_file()
    }
    expected = {record.key: record for record in records}

    missing = sorted(expected.keys() - actual.keys())
    extra = sorted((actual.keys() - expected.keys()) | symlinks)
    present = sorted(expected.keys() & actual.keys())
    size_mismatches = [
        key for key in present if actual[key].stat().st_size != expected[key].size
    ]
    sha256 = {key: _sha256_file(actual[key]) for key in present}

    return BackupComparison(missing, size_mismatches, extra, sha256)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(
    path: str | Path,
    bucket: str,
    records: list[ObjectRecord],
    comparison: BackupComparison,
) -> None:
    """Write inventory records and verification results as UTF-8 JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    objects = [
        {**asdict(record), "sha256": comparison.sha256.get(record.key)}
        for record in sorted(records, key=lambda record: record.key)
    ]
    manifest = {
        "bucket": bucket,
        "object_count": len(records),
        "total_size": sum(record.size for record in records),
        "objects": objects,
        "verification": {
            "missing": comparison.missing,
            "size_mismatches": comparison.size_mismatches,
            "extra": comparison.extra,
        },
    }
    write_json_atomic(path, manifest)
