from pathlib import Path

import pytest

from tools.recover.pipeline import recover_all


def _html(title: str | None, body: str = "Body") -> str:
    title_meta = f'<meta property="og:title" content="{title}">' if title else ""
    return (
        title_meta
        + '<meta itemprop="datePublished" content="2024-01-02">'
        + f"<article><section>{body}</section></article>"
    )


def test_recover_all_reports_sorted_success_and_failure(tmp_path: Path) -> None:
    source = tmp_path / "backup"
    bad = source / "a-bad" / "index.html"
    good = source / "z-good" / "index.html"
    bad.parent.mkdir(parents=True)
    good.parent.mkdir(parents=True)
    bad.write_text(_html(None), encoding="utf-8")
    good.write_text(_html("Good", "<p>Hello</p>"), encoding="utf-8")

    report = recover_all(source, tmp_path / "posts")

    assert report["source_count"] == 2
    assert report["success_count"] == 1
    assert report["failure_count"] == 1
    assert report["warning_count"] == 0
    assert [item["slug"] for item in report["articles"]] == ["a-bad", "z-good"]
    failed, succeeded = report["articles"]
    assert failed == {
        "slug": "a-bad",
        "status": "failed",
        "source": "posts/a-bad/index.html",
        "output": None,
        "source_text_length": 0,
        "markdown_length": 0,
        "copied_assets": [],
        "missing_assets": [],
        "unsupported_elements": [],
        "error": "ValueError: missing required title in posts/a-bad/index.html",
    }
    assert succeeded["status"] == "ok"
    assert succeeded["output"] == "content/posts/z-good/index.md"
    assert succeeded["source_text_length"] == len("Hello")
    assert succeeded["markdown_length"] > 0
    assert succeeded["copied_assets"] == []
    assert succeeded["missing_assets"] == []
    assert succeeded["unsupported_elements"] == []


def test_recover_all_warns_for_missing_assets_and_unsupported_elements(
    tmp_path: Path,
) -> None:
    source = tmp_path / "backup"
    page = source / "warning" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        _html("Warning", '<custom-box>x</custom-box><img src="missing.png">'),
        encoding="utf-8",
    )

    report = recover_all(source, tmp_path / "posts")

    item = report["articles"][0]
    assert item["status"] == "warning"
    assert item["missing_assets"] == ["missing.png"]
    assert item["unsupported_elements"] == ["custom-box"]
    assert report["success_count"] == 1
    assert report["warning_count"] == 1


def test_recover_all_removes_stale_output_for_failed_article(tmp_path: Path) -> None:
    source = tmp_path / "backup"
    page = source / "broken" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(_html(None), encoding="utf-8")
    stale = tmp_path / "posts" / "broken"
    stale.mkdir(parents=True)
    (stale / "index.md").write_text("stale", encoding="utf-8")

    report = recover_all(source, tmp_path / "posts")

    assert report["articles"][0]["status"] == "failed"
    assert not (stale / "index.md").exists()


@pytest.mark.parametrize("link_kind", ["directory", "file"])
def test_recover_all_rejects_symlinked_article_sources(
    tmp_path: Path, link_kind: str
) -> None:
    source = tmp_path / "backup"
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / "index.html"
    external.write_text(_html("External"), encoding="utf-8")
    source.mkdir()
    article_dir = source / "linked"
    try:
        if link_kind == "directory":
            article_dir.symlink_to(outside, target_is_directory=True)
        else:
            article_dir.mkdir()
            (article_dir / "index.html").symlink_to(external)
    except OSError:
        pytest.skip("symlinks are unavailable")

    report = recover_all(source, tmp_path / "posts")

    assert report["source_count"] == 1
    item = report["articles"][0]
    assert item["slug"] == "linked"
    assert item["status"] == "failed"
    assert item["source_text_length"] == 0
    assert item["output"] is None
    assert "unsafe source" in item["error"]


def test_recover_all_contains_cleanup_failure_and_continues(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "backup"
    bad = source / "a-bad" / "index.html"
    good = source / "z-good" / "index.html"
    bad.parent.mkdir(parents=True)
    good.parent.mkdir(parents=True)
    bad.write_text(_html(None), encoding="utf-8")
    good.write_text(_html("Good"), encoding="utf-8")

    def fail_cleanup(bundle: Path) -> None:
        raise OSError(f"cannot clean {bundle.name}")

    monkeypatch.setattr(
        "tools.recover.pipeline._remove_stale_bundle", fail_cleanup
    )

    report = recover_all(source, tmp_path / "posts")

    assert [item["status"] for item in report["articles"]] == ["failed", "ok"]
    assert "missing required title" in report["articles"][0]["error"]
    assert (
        "cleanup failed: OSError: cannot clean a-bad"
        in report["articles"][0]["error"]
    )


def test_recover_all_cleanup_failure_after_install_keeps_new_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "backup"
    page = source / "post" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(_html("New", "new body"), encoding="utf-8")
    destination = tmp_path / "posts" / "post"
    destination.mkdir(parents=True)
    (destination / "index.md").write_text("old", encoding="utf-8")

    def fail_cleanup(path: Path) -> None:
        raise OSError(f"cleanup failed: {path}")

    monkeypatch.setattr("tools.recover.writer._remove_staged", fail_cleanup)

    report = recover_all(source, tmp_path / "posts")

    assert report["articles"][0]["status"] == "ok"
    assert (destination / "index.md").read_text(encoding="utf-8").endswith(
        "new body\n"
    )


def test_recover_all_exchange_failure_does_not_delete_live_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "backup"
    page = source / "post" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(_html("New", "new body"), encoding="utf-8")
    destination = tmp_path / "posts" / "post"
    destination.mkdir(parents=True)
    live = destination / "index.md"
    live.write_text("old", encoding="utf-8")

    def fail_exchange(staged: Path, target: Path) -> None:
        raise OSError("exchange unavailable")

    monkeypatch.setattr("tools.recover.writer._atomic_exchange", fail_exchange)

    report = recover_all(source, tmp_path / "posts")

    assert report["articles"][0]["status"] == "failed"
    assert live.read_text(encoding="utf-8") == "old"


def test_recover_all_reconciles_only_stale_page_bundle_directories(
    tmp_path: Path,
) -> None:
    source = tmp_path / "backup"
    current = source / "current" / "index.html"
    current.parent.mkdir(parents=True)
    current.write_text(_html("Current"), encoding="utf-8")
    posts = tmp_path / "posts"
    stale = posts / "removed"
    stale.mkdir(parents=True)
    (stale / "index.md").write_text("stale", encoding="utf-8")
    reserved = posts / ".recover-reserved"
    reserved.mkdir()
    (reserved / "index.md").write_text("reserved", encoding="utf-8")
    non_bundle = posts / "notes"
    non_bundle.mkdir()
    (non_bundle / "keep.txt").write_text("keep", encoding="utf-8")
    file_at_root = posts / "README.md"
    file_at_root.write_text("keep", encoding="utf-8")

    report = recover_all(source, posts)

    assert report["removed_stale"] == ["removed"]
    assert not stale.exists()
    assert reserved.exists()
    assert non_bundle.exists()
    assert file_at_root.exists()


def test_recover_all_reports_stale_bundle_deletion_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "backup"
    current = source / "current" / "index.html"
    current.parent.mkdir(parents=True)
    current.write_text(_html("Current"), encoding="utf-8")
    posts = tmp_path / "posts"
    stale = posts / "removed"
    stale.mkdir(parents=True)
    (stale / "index.md").write_text("stale", encoding="utf-8")
    real_cleanup = __import__(
        "tools.recover.pipeline", fromlist=["_remove_stale_bundle"]
    )._remove_stale_bundle

    def fail_stale(bundle: Path) -> None:
        if bundle.name == "removed":
            raise OSError("permission denied")
        real_cleanup(bundle)

    monkeypatch.setattr(
        "tools.recover.pipeline._remove_stale_bundle", fail_stale
    )

    report = recover_all(source, posts)

    assert report["removed_stale"] == []
    assert report["stale_failures"] == [
        {"slug": "removed", "error": "OSError: permission denied"}
    ]
    assert report["warning_count"] == 1
    assert stale.exists()


def test_recover_all_reports_abandoned_staging_and_retries_next_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "backup"
    page = source / "post" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(_html("New", "new body"), encoding="utf-8")
    destination = tmp_path / "posts" / "post"
    destination.mkdir(parents=True)
    (destination / "index.md").write_text("old", encoding="utf-8")

    def fail_cleanup(path: Path) -> None:
        raise OSError("cleanup blocked")

    monkeypatch.setattr("tools.recover.writer._remove_staged", fail_cleanup)

    first = recover_all(source, tmp_path / "posts")

    abandoned = list((tmp_path / "posts").glob(".staged-post-*"))
    assert len(abandoned) == 1
    assert first["articles"][0]["status"] == "ok"
    assert first["cleanup_failures"] == [
        {"path": str(abandoned[0]), "error": "OSError: cleanup blocked"}
    ]
    assert first["warning_count"] == 1

    monkeypatch.undo()
    second = recover_all(source, tmp_path / "posts")

    assert not abandoned[0].exists()
    assert second["cleanup_failures"] == []
    assert second["warning_count"] == 0


def test_recover_all_staging_cleanup_ignores_unsafe_names_and_symlinks(
    tmp_path: Path,
) -> None:
    source = tmp_path / "backup"
    source.mkdir()
    posts = tmp_path / "posts"
    posts.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = outside / "marker"
    marker.write_text("safe", encoding="utf-8")
    unsafe_name = posts / ".staged-*-abcdefgh"
    unsafe_name.mkdir()
    (unsafe_name / "keep").write_text("unsafe slug", encoding="utf-8")
    linked = posts / ".staged-safe-abcdefgh"
    try:
        linked.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks are unavailable")

    report = recover_all(source, posts)

    assert report["cleanup_failures"] == []
    assert unsafe_name.exists()
    assert linked.is_symlink()
    assert marker.read_text(encoding="utf-8") == "safe"
