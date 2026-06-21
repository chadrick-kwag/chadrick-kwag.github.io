import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tools.recover import io as recovery_io
from tools.recover.inventory import (
    BackupComparison,
    ObjectRecord,
    compare_backup,
    compare_remote_snapshots,
    list_s3_objects,
    snapshot_and_sync,
    sync_bucket,
    write_manifest,
)


def test_compare_backup_matching_file(tmp_path: Path) -> None:
    target = tmp_path / "posts" / "a" / "index.html"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"hello")
    records = [ObjectRecord("posts/a/index.html", 5, '"etag"', None)]

    comparison = compare_backup(tmp_path, records)

    assert comparison == BackupComparison(
        missing=[],
        size_mismatches=[],
        extra=[],
        sha256={
            "posts/a/index.html": (
                "2cf24dba5fb0a30e26e83b2ac5b9e29"
                "e1b161e5c1fa7425e73043362938b9824"
            )
        },
    )


def test_compare_backup_reports_missing_mismatched_and_extra_files(
    tmp_path: Path,
) -> None:
    (tmp_path / "wrong.txt").write_bytes(b"x")
    (tmp_path / "extra.txt").write_bytes(b"extra")
    records = [
        ObjectRecord("missing.txt", 3, '"missing"', None),
        ObjectRecord("wrong.txt", 2, '"wrong"', "2026-06-20T00:00:00Z"),
    ]

    comparison = compare_backup(tmp_path, records)

    assert comparison.missing == ["missing.txt"]
    assert comparison.size_mismatches == ["wrong.txt"]
    assert comparison.extra == ["extra.txt"]
    assert comparison.sha256 == {
        "wrong.txt": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }


def test_compare_backup_rejects_symlink_and_reports_it_as_extra(
    tmp_path: Path,
) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_bytes(b"secret")
    (tmp_path / "linked.txt").symlink_to(outside)
    records = [ObjectRecord("linked.txt", 6, '"etag"', None)]

    comparison = compare_backup(tmp_path, records)

    assert comparison.missing == ["linked.txt"]
    assert comparison.extra == ["linked.txt"]
    assert comparison.sha256 == {}


def test_compare_remote_snapshots_detects_same_size_etag_change() -> None:
    before = [ObjectRecord("changed.txt", 5, '"before"', None)]
    after = [ObjectRecord("changed.txt", 5, '"after"', None)]

    assert compare_remote_snapshots(before, after) == ["changed.txt"]


def test_compare_remote_snapshots_detects_added_key() -> None:
    before = [ObjectRecord("stable.txt", 1, '"stable"', None)]
    after = [
        ObjectRecord("stable.txt", 1, '"stable"', None),
        ObjectRecord("added.txt", 2, '"added"', None),
    ]

    assert compare_remote_snapshots(before, after) == ["added.txt"]


def test_compare_remote_snapshots_detects_removed_key() -> None:
    before = [
        ObjectRecord("stable.txt", 1, '"stable"', None),
        ObjectRecord("removed.txt", 2, '"removed"', None),
    ]
    after = [ObjectRecord("stable.txt", 1, '"stable"', None)]

    assert compare_remote_snapshots(before, after) == ["removed.txt"]


@patch("tools.recover.inventory.compare_backup")
@patch("tools.recover.inventory.sync_bucket")
@patch("tools.recover.inventory.list_s3_objects")
def test_snapshot_and_sync_rejects_same_size_etag_mutation(
    list_objects: Mock,
    sync: Mock,
    compare: Mock,
    tmp_path: Path,
) -> None:
    before = [ObjectRecord("changed.txt", 5, '"before"', None)]
    after = [ObjectRecord("changed.txt", 5, '"after"', None)]
    list_objects.side_effect = [before, after]

    try:
        snapshot_and_sync("source-bucket", tmp_path)
    except RuntimeError as error:
        assert "changed.txt" in str(error)
    else:
        raise AssertionError("snapshot mutation was not rejected")

    assert list_objects.call_args_list == [
        (("source-bucket",),),
        (("source-bucket",),),
    ]
    sync.assert_called_once_with("source-bucket", tmp_path)
    compare.assert_not_called()


@patch("tools.recover.inventory.compare_backup")
@patch("tools.recover.inventory.sync_bucket")
@patch("tools.recover.inventory.list_s3_objects")
def test_snapshot_and_sync_returns_original_inventory_and_local_comparison(
    list_objects: Mock,
    sync: Mock,
    compare: Mock,
    tmp_path: Path,
) -> None:
    before = [ObjectRecord("stable.txt", 5, '"same"', None)]
    after = [ObjectRecord("stable.txt", 5, '"same"', "later")]
    comparison = BackupComparison([], [], [], {"stable.txt": "digest"})
    list_objects.side_effect = [before, after]
    compare.return_value = comparison

    result = snapshot_and_sync("source-bucket", tmp_path)

    assert result == (before, comparison)
    sync.assert_called_once_with("source-bucket", tmp_path)
    compare.assert_called_once_with(tmp_path, before)


@patch("tools.recover.inventory.subprocess.run")
def test_list_s3_objects_uses_aws_cli_and_parses_records(run: Mock) -> None:
    run.return_value.stdout = json.dumps(
        [
            {
                "key": "posts/한글.html",
                "size": 12,
                "etag": '"abc"',
                "last_modified": "2026-06-20T00:00:00Z",
            }
        ]
    )

    result = list_s3_objects("source-bucket")

    run.assert_called_once_with(
        [
            "aws",
            "s3api",
            "list-objects-v2",
            "--bucket",
            "source-bucket",
            "--query",
            "Contents[].{key:Key,size:Size,etag:ETag,last_modified:LastModified}",
            "--output",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result == [
        ObjectRecord(
            "posts/한글.html", 12, '"abc"', "2026-06-20T00:00:00Z"
        )
    ]


@patch("tools.recover.inventory.subprocess.run")
def test_list_s3_objects_treats_json_null_as_empty(run: Mock) -> None:
    run.return_value.stdout = "null\n"

    assert list_s3_objects("empty-bucket") == []


@patch("tools.recover.inventory.subprocess.run")
def test_sync_bucket_creates_destination_and_checks_aws_sync(
    run: Mock, tmp_path: Path
) -> None:
    destination = tmp_path / "nested" / "backup"

    sync_bucket("source-bucket", destination)

    assert destination.is_dir()
    run.assert_called_once_with(
        [
            "aws",
            "s3",
            "sync",
            "s3://source-bucket",
            str(destination),
            "--exact-timestamps",
        ],
        check=True,
    )


def test_write_manifest_serializes_inventory_and_verification(tmp_path: Path) -> None:
    path = tmp_path / "metadata" / "manifest.json"
    records = [ObjectRecord("한글.html", 5, '"abc"', None)]
    comparison = BackupComparison(
        missing=[],
        size_mismatches=[],
        extra=["orphan.txt"],
        sha256={"한글.html": "digest"},
    )

    write_manifest(path, "source-bucket", records, comparison)

    assert path.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "bucket": "source-bucket",
        "object_count": 1,
        "total_size": 5,
        "objects": [
            {
                "key": "한글.html",
                "size": 5,
                "etag": '"abc"',
                "last_modified": None,
                "sha256": "digest",
            }
        ],
        "verification": {
            "missing": [],
            "size_mismatches": [],
            "extra": ["orphan.txt"],
        },
    }
    assert "한글.html" in path.read_text(encoding="utf-8")


def test_write_manifest_sorts_objects_by_key(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    records = [
        ObjectRecord("z-last.txt", 1, '"z"', None),
        ObjectRecord("a-first.txt", 1, '"a"', None),
    ]
    comparison = BackupComparison([], [], [], {})

    write_manifest(path, "source-bucket", records, comparison)

    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert [item["key"] for item in manifest["objects"]] == [
        "a-first.txt",
        "z-last.txt",
    ]


def test_write_manifest_preserves_existing_file_when_atomic_write_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "manifest.json"
    original = b"existing manifest\n"
    path.write_bytes(original)

    def fail_after_partial_write(file, content: str) -> None:
        file.write(content[:10])
        file.flush()
        raise OSError("disk full")

    monkeypatch.setattr(recovery_io, "_write_and_sync", fail_after_partial_write)

    with pytest.raises(OSError, match="disk full"):
        write_manifest(path, "bucket", [], BackupComparison([], [], [], {}))

    assert path.read_bytes() == original
    assert list(tmp_path.glob("*.tmp")) == []
