"""Parse published articles from old Hugo HTML output."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag

from tools.recover.model import Article


def parse_article(path: Path, slug: str) -> Article:
    """Parse one published Hugo article from *path*."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = soup.find("article")
    if not isinstance(article, Tag):
        raise ValueError(f"missing article element in {path}")

    content = article.find("section", recursive=False)
    if not isinstance(content, Tag):
        raise ValueError(f"missing direct article section in {path}")

    title = _meta_content(soup, "property", "og:title")
    if not title:
        heading = article.find("h1")
        title = (
            heading.get_text(" ", strip=True)
            if isinstance(heading, Tag)
            else None
        )
    if not title:
        raise ValueError(f"missing required title in {path}")

    date = _meta_content(soup, "itemprop", "datePublished")
    if not date:
        date = _meta_content(soup, "property", "article:published_time")
    if not date:
        raise ValueError(f"missing required publication date in {path}")

    lastmod = _meta_content(soup, "itemprop", "dateModified")
    if not lastmod:
        lastmod = _meta_content(soup, "property", "article:modified_time")

    return Article(
        slug=slug,
        title=title,
        date=date,
        lastmod=lastmod or date,
        categories=_taxonomy(article, "/categories/"),
        tags=_taxonomy(article, "/tags/"),
        source_path=path,
        content=content,
    )


def _meta_content(soup: BeautifulSoup, attribute: str, value: str) -> str | None:
    meta = soup.find("meta", attrs={attribute: value})
    if not isinstance(meta, Tag):
        return None
    content = meta.get("content")
    if not isinstance(content, str):
        return None
    return content.strip()


def _taxonomy(article: Tag, prefix: str) -> tuple[str, ...]:
    names = {
        link.get_text(" ", strip=True)
        for link in article.find_all("a")
        if isinstance(link.get("href"), str)
        and _is_taxonomy_href(link["href"], prefix)
        and link.get_text(" ", strip=True)
    }
    return tuple(sorted(names, key=str.casefold))


def _is_taxonomy_href(href: str, prefix: str) -> bool:
    parsed = urlparse(href)
    if parsed.hostname not in (None, "chadrick-kwag.net"):
        return False
    if parsed.scheme and parsed.hostname is None:
        return False
    taxonomy_path = prefix.rstrip("/")
    return parsed.path == taxonomy_path or parsed.path.startswith(
        f"{taxonomy_path}/"
    )
