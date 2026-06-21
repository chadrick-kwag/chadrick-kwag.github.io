"""Validate recovered Hugo page bundles."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


_REQUIRED = ("title", "date", "slug", "draft")
_MARKDOWN = MarkdownIt("commonmark", {"html": True})


def _srcset_candidates(value: str) -> list[str]:
    """Parse srcset URLs using the HTML candidate-tokenization rules."""
    candidates: list[str] = []
    cursor = 0
    while cursor < len(value):
        while cursor < len(value) and (
            value[cursor].isspace() or value[cursor] == ","
        ):
            cursor += 1
        start = cursor
        while cursor < len(value) and not value[cursor].isspace():
            cursor += 1
        token = value[start:cursor]
        url = token.rstrip(",")
        if url:
            candidates.append(url)
        if token.endswith(","):
            continue
        parentheses = 0
        while cursor < len(value):
            character = value[cursor]
            if character == "(":
                parentheses += 1
            elif character == ")" and parentheses:
                parentheses -= 1
            elif character == "," and not parentheses:
                cursor += 1
                break
            cursor += 1
    return candidates


def _front_matter(text: str) -> tuple[dict[str, Any] | None, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, ""
    closing = next(
        (index for index, line in enumerate(lines[1:], 1)
         if line.rstrip("\r\n") == "---"),
        None,
    )
    if closing is None:
        return None, ""
    try:
        loaded = yaml.safe_load("".join(lines[1:closing]))
    except yaml.YAMLError:
        return None, "".join(lines[closing + 1:])
    if not isinstance(loaded, dict):
        return None, "".join(lines[closing + 1:])
    return loaded, "".join(lines[closing + 1:])


def _rendered_destinations(body: str) -> list[tuple[bool, str]]:
    """Extract destinations from the rendered CommonMark document."""
    soup = BeautifulSoup(_MARKDOWN.render(body), "html.parser")
    destinations: list[tuple[bool, str]] = []
    for element in soup.find_all(["img", "source"]):
        if element.name == "img":
            source = element.get("src")
            if isinstance(source, str):
                destinations.append((True, source))
        srcset = element.get("srcset")
        if isinstance(srcset, str):
            destinations.extend(
                (True, candidate)
                for candidate in _srcset_candidates(srcset)
            )
    for anchor in soup.find_all("a"):
        target = anchor.get("href")
        if isinstance(target, str):
            destinations.append((False, target))
    return destinations


def _decoded_asset_path(destination: str) -> tuple[str, bool] | None:
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    filesystem_path = unquote(parsed.path)
    validation_path = filesystem_path
    while True:
        relative_validation = validation_path.removeprefix("/")
        if (
            "\\" in validation_path
            or not relative_validation
            or any(
                part in {"", ".", ".."}
                for part in relative_validation.split("/")
            )
        ):
            return filesystem_path, False
        decoded_again = unquote(validation_path)
        if decoded_again == validation_path:
            return filesystem_path, True
        validation_path = decoded_again


def _asset_exists(root: Path, relative: PurePosixPath) -> bool:
    try:
        resolved_root = root.resolve(strict=True)
        candidate = root.joinpath(*relative.parts).resolve(strict=True)
        size = candidate.stat().st_size
    except (OSError, RuntimeError):
        return False
    return (
        candidate.is_relative_to(resolved_root)
        and candidate.is_file()
        and size > 0
    )


def _asset_is_present(
    destination: str, bundle: Path, posts_root: Path
) -> tuple[str, bool] | None:
    decoded = _decoded_asset_path(destination)
    if decoded is None:
        return None
    filesystem_path, safe = decoded
    if not safe:
        return filesystem_path, False
    if filesystem_path.startswith("/"):
        parts = PurePosixPath(filesystem_path).parts[1:]
        if len(parts) >= 3 and parts[0] == "posts":
            root = posts_root
            parts = parts[1:]
        else:
            root = posts_root.parents[1] / "static"
        relative = PurePosixPath(*parts)
    else:
        root = bundle
        relative = PurePosixPath(filesystem_path)
    return filesystem_path, _asset_exists(root, relative)


def _post_slug(destination: str) -> str | None:
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    parts = path.split("/")
    if (
        len(parts) == 4
        and parts[0] == ""
        and parts[1] == "posts"
        and parts[3] == ""
    ):
        return parts[2] or None
    if len(parts) == 3 and parts[0] == "" and parts[1] == "posts":
        return parts[2] or None
    return None


def _valid_iso_date(value: Any) -> bool:
    if isinstance(value, datetime):
        return True
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_recovery(posts_root: Path, expected_count: int) -> dict[str, Any]:
    """Return a deterministic validation report for recovered posts."""
    index_paths = sorted(posts_root.glob("*/index.md"))
    missing_fields: list[str] = []
    invalid_fields: list[str] = []
    empty_bodies: list[str] = []
    missing_assets: list[str] = []
    unsafe_bundles: list[str] = []
    links: list[tuple[str, str]] = []
    slug_counts: dict[str, int] = {}
    try:
        posts_root_resolved = posts_root.resolve(strict=True)
    except OSError:
        posts_root_resolved = posts_root.resolve()

    for index_path in index_paths:
        bundle = index_path.parent
        identity = bundle.name
        try:
            unsafe = (
                bundle.is_symlink()
                or index_path.is_symlink()
                or bundle.parent.resolve(strict=True) != posts_root_resolved
                or not index_path.resolve(strict=True).is_relative_to(
                    posts_root_resolved
                )
            )
        except (OSError, RuntimeError):
            unsafe = True
        if unsafe:
            unsafe_bundles.append(identity)
            continue
        metadata, body = _front_matter(index_path.read_text(encoding="utf-8"))
        if metadata is None:
            missing_fields.append(f"{identity}:front_matter")
        else:
            for field in _REQUIRED:
                if field not in metadata or (
                    field != "draft"
                    and (metadata[field] is None or str(metadata[field]).strip() == "")
                ):
                    missing_fields.append(f"{identity}:{field}")
            slug = metadata.get("slug")
            title = metadata.get("title")
            date_value = metadata.get("date")
            draft = metadata.get("draft")
            if (
                title is not None
                and str(title).strip()
                and not isinstance(title, str)
            ):
                invalid_fields.append(f"{identity}:title")
            if (
                date_value is not None
                and str(date_value).strip()
                and not _valid_iso_date(date_value)
            ):
                invalid_fields.append(f"{identity}:date")
            if "draft" in metadata and not isinstance(draft, bool):
                invalid_fields.append(f"{identity}:draft")
            if slug is not None and str(slug).strip():
                if not isinstance(slug, str) or slug != identity:
                    invalid_fields.append(f"{identity}:slug")
                if isinstance(slug, str):
                    slug_counts[slug] = slug_counts.get(slug, 0) + 1
        if not body.strip():
            empty_bodies.append(identity)
        for is_image, destination in _rendered_destinations(body):
            if is_image:
                local = _asset_is_present(destination, bundle, posts_root)
                if local is not None and not local[1]:
                    missing_assets.append(f"{identity}:{local[0]}")
            else:
                linked_slug = _post_slug(destination)
                if linked_slug is not None:
                    links.append((identity, linked_slug))

    slugs = set(slug_counts)
    duplicate_slugs = sorted(
        slug for slug, count in slug_counts.items() if count > 1
    )
    broken_post_links = [
        f"{source}:{target}" for source, target in links if target not in slugs
    ]
    result: dict[str, Any] = {
        "expected_count": expected_count,
        "article_count": len(index_paths),
        "missing_fields": sorted(set(missing_fields)),
        "invalid_fields": sorted(set(invalid_fields)),
        "duplicate_slugs": duplicate_slugs,
        "empty_bodies": sorted(set(empty_bodies)),
        "missing_assets": sorted(set(missing_assets)),
        "unsafe_bundles": sorted(set(unsafe_bundles)),
        "broken_post_links": sorted(set(broken_post_links)),
    }
    result["valid"] = (
        result["article_count"] == expected_count
        and not any(result[key] for key in (
            "missing_fields", "invalid_fields", "duplicate_slugs",
            "empty_bodies", "missing_assets", "unsafe_bundles",
            "broken_post_links"
        ))
    )
    return result
