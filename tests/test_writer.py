from pathlib import Path
from unittest.mock import Mock

from bs4 import BeautifulSoup
from bs4.element import Tag
import pytest
import yaml

from tools.recover import writer as writer_module
from tools.recover.markdown import MarkdownResult
from tools.recover.model import Article
from tools.recover.writer import write_bundle


def _article(source: Path, slug: str = "unicode-post") -> Article:
    content = BeautifulSoup("<section>body</section>", "html.parser").find(
        "section"
    )
    assert isinstance(content, Tag)
    return Article(
        slug=slug,
        title="Unicode 제목",
        date="2024-01-02T03:04:05Z",
        lastmod="2024-01-03T03:04:05Z",
        categories=("Python",),
        tags=("Hugo", "복구"),
        source_path=source,
        content=content,
    )


def test_write_bundle_writes_front_matter_body_and_unicode_asset(
    tmp_path: Path,
) -> None:
    source = tmp_path / "backup" / "unicode-post" / "index.html"
    image = source.parent / "images" / "캡처.png"
    image.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    image.write_bytes(b"image")
    posts = tmp_path / "content" / "posts"

    copied = write_bundle(
        _article(source),
        MarkdownResult("Hello **world**.\n", ("images/캡처.png",), ()),
        posts,
    )

    output = posts / "unicode-post" / "index.md"
    text = output.read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    metadata = yaml.safe_load(front)
    assert metadata["slug"] == "unicode-post"
    assert metadata["draft"] is False
    assert metadata["categories"] == ["Python"]
    assert metadata["tags"] == ["Hugo", "복구"]
    assert body == "Hello **world**.\n"
    assert (posts / "unicode-post" / "images" / "캡처.png").read_bytes() == b"image"
    assert copied == ("images/캡처.png",)


def test_write_bundle_skips_missing_assets(tmp_path: Path) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")

    copied = write_bundle(
        _article(source), MarkdownResult("body\n", ("missing.png",), ()),
        tmp_path / "posts",
    )

    assert copied == ()
    assert (tmp_path / "posts" / "unicode-post" / "index.md").exists()


@pytest.mark.parametrize("asset", ["../secret", "/etc/passwd"])
def test_write_bundle_rejects_asset_path_escape(
    tmp_path: Path, asset: str
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")

    with pytest.raises(ValueError, match="asset path"):
        write_bundle(
            _article(source), MarkdownResult("body\n", (asset,), ()),
            tmp_path / "posts",
        )


def test_write_bundle_rejects_symlinked_asset_escape(tmp_path: Path) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"secret")
    (source.parent / "linked.png").symlink_to(outside)

    with pytest.raises(ValueError, match="asset path"):
        write_bundle(
            _article(source), MarkdownResult("body\n", ("linked.png",), ()),
            tmp_path / "posts",
        )


def test_write_bundle_leaves_existing_bundle_when_staging_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    asset = source.parent / "asset.png"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    asset.write_bytes(b"image")
    destination = tmp_path / "posts" / "unicode-post"
    destination.mkdir(parents=True)
    old = destination / "index.md"
    old.write_text("old", encoding="utf-8")

    def fail_copy(*args: object, **kwargs: object) -> None:
        raise OSError("copy failed")

    monkeypatch.setattr("tools.recover.writer.shutil.copy2", fail_copy)
    with pytest.raises(OSError, match="copy failed"):
        write_bundle(
            _article(source), MarkdownResult("new\n", ("asset.png",), ()),
            tmp_path / "posts",
        )

    assert old.read_text(encoding="utf-8") == "old"


def test_write_bundle_keeps_existing_bundle_when_atomic_exchange_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    destination = tmp_path / "posts" / "unicode-post"
    destination.mkdir(parents=True)
    old = destination / "index.md"
    old.write_text("old", encoding="utf-8")

    def fail_exchange(staged: Path, live: Path) -> None:
        raise OSError("exchange failed")

    monkeypatch.setattr("tools.recover.writer._atomic_exchange", fail_exchange)

    with pytest.raises(OSError, match="exchange failed"):
        write_bundle(
            _article(source), MarkdownResult("new\n", (), ()),
            tmp_path / "posts",
        )

    assert old.read_text(encoding="utf-8") == "old"


def test_write_bundle_uses_one_exchange_for_existing_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    destination = tmp_path / "posts" / "unicode-post"
    destination.mkdir(parents=True)
    (destination / "index.md").write_text("old", encoding="utf-8")
    exchange = Mock(wraps=writer_module._atomic_exchange)

    monkeypatch.setattr("tools.recover.writer._atomic_exchange", exchange)

    write_bundle(
        _article(source), MarkdownResult("new\n", (), ()), tmp_path / "posts"
    )

    exchange.assert_called_once()
    assert exchange.call_args.args[1] == destination
    assert (destination / "index.md").read_text(encoding="utf-8").endswith(
        "new\n"
    )


def test_write_bundle_ignores_exchanged_bundle_cleanup_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    destination = tmp_path / "posts" / "unicode-post"
    destination.mkdir(parents=True)
    (destination / "index.md").write_text("old", encoding="utf-8")

    def fail_cleanup(path: Path) -> None:
        raise OSError(f"cleanup failed: {path}")

    monkeypatch.setattr("tools.recover.writer._remove_staged", fail_cleanup)

    write_bundle(
        _article(source), MarkdownResult("new\n", (), ()), tmp_path / "posts"
    )

    assert (destination / "index.md").read_text(encoding="utf-8").endswith(
        "new\n"
    )


def test_write_bundle_rejects_glob_slug_without_touching_victim(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source" / "post" / "index.html"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    marker = tmp_path / "posts" / ".previous-victim-marker"
    marker.mkdir(parents=True)
    (marker / "keep").write_text("victim", encoding="utf-8")

    with pytest.raises(ValueError, match="unsafe slug"):
        write_bundle(
            _article(source, slug="*"), MarkdownResult("new\n", (), ()),
            tmp_path / "posts",
        )

    assert (marker / "keep").read_text(encoding="utf-8") == "victim"
