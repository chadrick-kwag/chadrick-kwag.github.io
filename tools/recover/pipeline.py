"""Run the HTML-to-Hugo recovery pipeline and build a report."""

from __future__ import annotations

from pathlib import Path
import shutil
import stat
from typing import Any

from tools.recover import writer as writer_module
from tools.recover.markdown import convert_content
from tools.recover.parser import parse_article
from tools.recover.writer import AtomicExchangeError, write_bundle


def recover_all(source_posts: Path, destination_posts: Path) -> dict[str, Any]:
    """Recover every one-level page bundle found below *source_posts*."""
    source_root = source_posts.resolve()
    destination_posts.mkdir(parents=True, exist_ok=True)
    destination_root = destination_posts.resolve()
    cleanup_failures = _cleanup_abandoned_staging(destination_root)
    sources = sorted(source_root.glob("*/index.html"))
    source_slugs = {source.parent.name for source in sources}
    removed_stale, stale_failures = _reconcile_destination(
        destination_root, source_slugs
    )
    articles: list[dict[str, Any]] = []

    for source in sources:
        slug = source.parent.name
        source_label = f"posts/{slug}/index.html"
        item: dict[str, Any] = {
            "slug": slug,
            "status": "failed",
            "source": source_label,
            "output": None,
            "source_text_length": 0,
            "markdown_length": 0,
            "copied_assets": [],
            "missing_assets": [],
            "unsupported_elements": [],
            "error": None,
        }
        try:
            _validate_source(source, source_root)
            article = parse_article(source, slug)
            item["source_text_length"] = len(
                article.content.get_text(" ", strip=True)
            )
            converted = convert_content(article.content)
            item["markdown_length"] = len(converted.markdown)
            item["unsupported_elements"] = list(converted.unsupported_elements)
            copied = write_bundle(article, converted, destination_posts)
            item["copied_assets"] = list(copied)
            item["missing_assets"] = list(
                sorted(set(converted.local_assets) - set(copied))
            )
            item["output"] = f"content/posts/{slug}/index.md"
            item["status"] = (
                "warning"
                if item["missing_assets"] or item["unsupported_elements"]
                else "ok"
            )
        except Exception as error:
            message = str(error).replace(str(source), source_label)
            item["error"] = f"{type(error).__name__}: {message}"
            bundle = destination_root / slug
            if not isinstance(error, AtomicExchangeError):
                try:
                    _require_direct_child(bundle, destination_root)
                    _remove_stale_bundle(bundle)
                except Exception as cleanup_error:
                    item["error"] += (
                        "; cleanup failed: "
                        f"{type(cleanup_error).__name__}: {cleanup_error}"
                    )
        articles.append(item)

    cleanup_failures = _merge_cleanup_failures(
        cleanup_failures, _cleanup_abandoned_staging(destination_root)
    )
    failure_count = sum(item["status"] == "failed" for item in articles)
    warning_count = (
        sum(item["status"] == "warning" for item in articles)
        + len(stale_failures)
        + len(cleanup_failures)
    )
    return {
        "source_count": len(sources),
        "success_count": len(sources) - failure_count,
        "failure_count": failure_count,
        "warning_count": warning_count,
        "removed_stale": removed_stale,
        "stale_failures": stale_failures,
        "cleanup_failures": cleanup_failures,
        "articles": articles,
    }


def _remove_stale_bundle(bundle: Path) -> None:
    if bundle.is_symlink() or bundle.is_file():
        bundle.unlink(missing_ok=True)
    elif bundle.exists():
        shutil.rmtree(bundle)


def _validate_source(source: Path, source_root: Path) -> None:
    if source.parent.is_symlink() or source.is_symlink():
        raise ValueError(f"unsafe source symlink: {source}")
    resolved = source.resolve()
    if (
        not resolved.is_relative_to(source_root)
        or resolved.parent.parent != source_root
    ):
        raise ValueError(f"unsafe source path: {source}")


def _require_direct_child(path: Path, root: Path) -> None:
    if path.parent.resolve() != root or path.name in {"", ".", ".."}:
        raise ValueError(f"unsafe destination path: {path}")


def _reconcile_destination(
    root: Path, source_slugs: set[str]
) -> tuple[list[str], list[dict[str, str]]]:
    removed: list[str] = []
    failures: list[dict[str, str]] = []
    for candidate in sorted(root.iterdir()):
        if (
            candidate.name.startswith(".")
            or candidate.name in source_slugs
            or candidate.is_symlink()
            or not candidate.is_dir()
        ):
            continue
        index = candidate / "index.md"
        try:
            is_bundle = stat.S_ISREG(index.lstat().st_mode)
        except FileNotFoundError:
            is_bundle = False
        if not is_bundle:
            continue
        try:
            _require_direct_child(candidate, root)
            _remove_stale_bundle(candidate)
        except Exception as error:
            failures.append(
                {
                    "slug": candidate.name,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            continue
        removed.append(candidate.name)
    return removed, failures


def _cleanup_abandoned_staging(root: Path) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for candidate in sorted(root.iterdir()):
        if candidate.is_symlink() or not _is_staging_name(candidate.name):
            continue
        try:
            is_directory = stat.S_ISDIR(candidate.lstat().st_mode)
        except FileNotFoundError:
            continue
        if not is_directory or candidate.parent.resolve() != root:
            continue
        try:
            writer_module._remove_staged(candidate)
        except Exception as error:
            failures.append(
                {
                    "path": str(candidate),
                    "error": f"{type(error).__name__}: {error}",
                }
            )
    return failures


def _is_staging_name(name: str) -> bool:
    prefix = ".staged-"
    if not name.startswith(prefix):
        return False
    slug, separator, suffix = name[len(prefix):].rpartition("-")
    if not separator or not suffix or not all(
        character.isascii() and (character.isalnum() or character == "_")
        for character in suffix
    ):
        return False
    try:
        writer_module._safe_slug(slug)
    except ValueError:
        return False
    return True


def _merge_cleanup_failures(
    first: list[dict[str, str]], second: list[dict[str, str]]
) -> list[dict[str, str]]:
    merged = {failure["path"]: failure for failure in first}
    merged.update({failure["path"]: failure for failure in second})
    return [merged[path] for path in sorted(merged)]
