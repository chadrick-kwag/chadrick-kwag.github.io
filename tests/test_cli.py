import json
from pathlib import Path

import pytest

from tools.recover import io as recovery_io
from tools.recover import __main__ as cli
from tools.recover.inventory import BackupComparison, ObjectRecord


def test_inventory_uses_snapshot_and_sync_and_writes_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    backup = tmp_path / "backup"
    manifest = tmp_path / "manifest.json"
    records = [ObjectRecord("post", 4, "etag", "2024-01-01")]
    comparison = BackupComparison([], [], [], {"post": "digest"})
    calls = []

    def snapshot(bucket: str, destination: Path):
        calls.append((bucket, destination))
        return records, comparison

    monkeypatch.setattr(cli, "snapshot_and_sync", snapshot)

    status = cli.main(
        [
            "inventory", "--bucket", "site-bucket", "--backup", str(backup),
            "--manifest", str(manifest),
        ]
    )

    assert status == 0
    assert calls == [("site-bucket", backup)]
    assert json.loads(manifest.read_text(encoding="utf-8"))["objects"][0][
        "sha256"
    ] == "digest"


@pytest.mark.parametrize("field", ["missing", "size_mismatches", "extra"])
def test_inventory_returns_one_for_verification_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    values = {"missing": [], "size_mismatches": [], "extra": []}
    values[field] = ["bad"]
    comparison = BackupComparison(**values, sha256={})
    monkeypatch.setattr(cli, "snapshot_and_sync", lambda *_: ([], comparison))

    status = cli.main([
        "inventory", "--bucket", "bucket", "--backup", str(tmp_path / "b"),
        "--manifest", str(tmp_path / "m.json"),
    ])

    assert status == 1


def test_inventory_source_mutation_is_concise_and_does_not_leak_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "never-print-this-secret")
    monkeypatch.setattr(
        cli, "snapshot_and_sync", lambda *_: (_ for _ in ()).throw(
            RuntimeError("S3 bucket changed during sync")
        )
    )

    status = cli.main([
        "inventory", "--bucket", "bucket", "--backup", str(tmp_path / "b"),
        "--manifest", str(tmp_path / "m.json"),
    ])

    captured = capsys.readouterr()
    assert status != 0
    assert captured.out == ""
    assert captured.err == "error: S3 bucket changed during sync\n"
    assert "never-print-this-secret" not in captured.err
    assert "Traceback" not in captured.err


def test_recover_writes_utf8_report_and_routes_posts_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    backup, site, report_path = tmp_path / "backup", tmp_path / "site", tmp_path / "r.json"
    report = {
        "source_count": 1, "success_count": 1, "failure_count": 0,
        "stale_failures": [], "cleanup_failures": [],
        "articles": [{"status": "warning", "missing_assets": [],
                      "unsupported_elements": ["사용자태그"]}],
    }
    calls = []
    monkeypatch.setattr(cli, "recover_all", lambda source, destination: calls.append(
        (source, destination)
    ) or report)

    status = cli.main([
        "recover", "--backup", str(backup), "--site", str(site),
        "--report", str(report_path),
    ])

    assert status == 0
    assert calls == [(backup / "posts", site / "content/posts")]
    text = report_path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert "사용자태그" in text
    assert "\\u" not in text
    assert json.loads(text) == report


@pytest.mark.parametrize(
    "updates",
    [
        {"failure_count": 1, "success_count": 0},
        {"source_count": 2},
        {"stale_failures": [{"slug": "old"}]},
        {"cleanup_failures": [{"path": "staged"}]},
        {"articles": [{"status": "warning", "missing_assets": ["image.png"]}]},
    ],
)
def test_recover_returns_one_for_incomplete_or_asset_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, updates: dict
) -> None:
    report = {
        "source_count": 1, "success_count": 1, "failure_count": 0,
        "stale_failures": [], "cleanup_failures": [], "articles": [],
    }
    report.update(updates)
    monkeypatch.setattr(cli, "recover_all", lambda *_: report)

    status = cli.main([
        "recover", "--backup", str(tmp_path / "b"), "--site", str(tmp_path / "s"),
        "--report", str(tmp_path / "report.json"),
    ])

    assert status == 1


def test_recover_preserves_existing_report_when_atomic_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str]
) -> None:
    report_path = tmp_path / "report.json"
    original = b"existing report\n"
    report_path.write_bytes(original)
    report = {
        "source_count": 0, "success_count": 0, "failure_count": 0,
        "stale_failures": [], "cleanup_failures": [], "articles": [],
    }
    monkeypatch.setattr(cli, "recover_all", lambda *_: report)
    monkeypatch.setattr(
        recovery_io.os, "replace", lambda *_: (_ for _ in ()).throw(
            OSError("replace blocked")
        )
    )

    status = cli.main([
        "recover", "--backup", str(tmp_path / "b"),
        "--site", str(tmp_path / "s"), "--report", str(report_path),
    ])

    assert status == 1
    assert capsys.readouterr().err == "error: replace blocked\n"
    assert report_path.read_bytes() == original
    assert list(tmp_path.glob("*.tmp")) == []


def test_validate_writes_report_and_returns_validity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = tmp_path / "site"
    report_path = tmp_path / "validation.json"
    expected = {
        "expected_count": 1,
        "article_count": 1,
        "missing_fields": [],
        "empty_bodies": [],
        "missing_assets": [],
        "broken_post_links": [],
        "valid": True,
    }
    calls = []
    monkeypatch.setattr(
        cli,
        "validate_recovery",
        lambda root, count: calls.append((root, count)) or expected,
        raising=False,
    )

    status = cli.main([
        "validate", "--site", str(site), "--expected-count", "1",
        "--report", str(report_path),
    ])

    assert status == 0
    assert calls == [(site / "content/posts", 1)]
    assert json.loads(report_path.read_text(encoding="utf-8")) == expected


def test_validate_returns_one_for_invalid_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        cli,
        "validate_recovery",
        lambda *_: {"valid": False},
        raising=False,
    )

    status = cli.main([
        "validate", "--site", str(tmp_path / "site"),
        "--expected-count", "1", "--report", str(tmp_path / "report.json"),
    ])

    assert status == 1
