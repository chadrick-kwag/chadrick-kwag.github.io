from pathlib import Path

import pytest

from tools.recover.parser import parse_article


FIXTURE = Path(__file__).parent / "fixtures" / "article.html"


def test_parse_article_extracts_metadata_taxonomy_and_content() -> None:
    article = parse_article(FIXTURE, "recovered-post")

    assert article.slug == "recovered-post"
    assert article.title == "Recovered post"
    assert article.date == "2023-10-27T12:33:00+00:00"
    assert article.lastmod == "2023-10-28T12:33:00+00:00"
    assert article.categories == ("Python",)
    assert article.tags == ("Hugo",)
    assert article.source_path == FIXTURE
    assert article.content.name == "section"


def test_parse_article_uses_fallback_metadata_and_date_for_lastmod(
    tmp_path: Path,
) -> None:
    path = tmp_path / "fallback.html"
    path.write_text(
        """<html><head>
        <meta property="article:published_time" content="2024-01-02T03:04:05Z">
        </head><body><article><h1>Fallback title</h1><section>Body</section>
        </article></body></html>""",
        encoding="utf-8",
    )

    article = parse_article(path, "fallback")

    assert article.title == "Fallback title"
    assert article.date == "2024-01-02T03:04:05Z"
    assert article.lastmod == article.date


def test_parse_article_uses_modified_time_fallback(tmp_path: Path) -> None:
    path = tmp_path / "modified.html"
    path.write_text(
        """<meta property="og:title" content="Title">
        <meta itemprop="datePublished" content="published">
        <meta property="article:modified_time" content="modified">
        <article><section>Body</section></article>""",
        encoding="utf-8",
    )

    assert parse_article(path, "modified").lastmod == "modified"


def test_parse_article_skips_empty_primary_metadata(tmp_path: Path) -> None:
    path = tmp_path / "empty-primary.html"
    path.write_text(
        """<meta property="og:title" content=" ">
        <meta itemprop="datePublished" content="">
        <meta property="article:published_time" content="published">
        <meta itemprop="dateModified" content="">
        <meta property="article:modified_time" content="modified">
        <article><h1>Fallback title</h1><section>Body</section></article>""",
        encoding="utf-8",
    )

    article = parse_article(path, "empty-primary")

    assert (article.title, article.date, article.lastmod) == (
        "Fallback title",
        "published",
        "modified",
    )


def test_parse_article_deduplicates_strips_and_casefold_sorts_taxonomy(
    tmp_path: Path,
) -> None:
    path = tmp_path / "taxonomy.html"
    path.write_text(
        """<meta property="og:title" content="Title">
        <meta itemprop="datePublished" content="date">
        <article><section>Body</section>
        <a href="/categories/z/"> zebra </a>
        <a href="/categories/a/">Apple</a>
        <a href="/categories/z-again/">zebra</a>
        <a href="/tags/b/"> beta </a><a href="/tags/a/">Alpha</a>
        <a href="/outside/categories/no/">Ignored</a>
        </article>""",
        encoding="utf-8",
    )

    article = parse_article(path, "taxonomy")

    assert article.categories == ("Apple", "zebra")
    assert article.tags == ("Alpha", "beta")


def test_parse_article_separates_nested_heading_text(tmp_path: Path) -> None:
    path = tmp_path / "nested-heading.html"
    path.write_text(
        """<meta itemprop="datePublished" content="date">
        <article><h1><span>Nested</span><em>title</em></h1>
        <section>Body</section></article>""",
        encoding="utf-8",
    )

    assert parse_article(path, "nested-heading").title == "Nested title"


def test_parse_article_separates_nested_taxonomy_text(tmp_path: Path) -> None:
    path = tmp_path / "nested-taxonomy.html"
    path.write_text(
        """<meta property="og:title" content="Title">
        <meta itemprop="datePublished" content="date">
        <article><section>Body</section>
        <a href="/categories/nested/"><span>Nested</span><em>category</em></a>
        <a href="/tags/nested/"><span>Nested</span><em>tag</em></a>
        </article>""",
        encoding="utf-8",
    )

    article = parse_article(path, "nested-taxonomy")

    assert article.categories == ("Nested category",)
    assert article.tags == ("Nested tag",)


def test_parse_article_accepts_same_site_absolute_taxonomy_only(
    tmp_path: Path,
) -> None:
    path = tmp_path / "absolute-taxonomy.html"
    path.write_text(
        """<meta property="og:title" content="Title">
        <meta itemprop="datePublished" content="date">
        <article><section>Body</section>
        <a href="https://chadrick-kwag.net/categories/python">Python</a>
        <a href="https://chadrick-kwag.net/tags/hugo">Hugo</a>
        <a href="https://external.example/categories/deceptive">External</a>
        </article>""",
        encoding="utf-8",
    )

    article = parse_article(path, "absolute-taxonomy")

    assert article.categories == ("Python",)
    assert article.tags == ("Hugo",)


@pytest.mark.parametrize(
    ("html", "message"),
    [
        ("<h1>Title</h1>", "article"),
        ("<article><h1>Title</h1></article>", "section"),
        (
            '<meta itemprop="datePublished" content="date">'
            "<article><section>Body</section></article>",
            "title",
        ),
        ("<article><h1>Title</h1><section>Body</section></article>", "date"),
    ],
)
def test_parse_article_reports_missing_required_structure_or_metadata(
    tmp_path: Path, html: str, message: str
) -> None:
    path = tmp_path / "invalid.html"
    path.write_text(html, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        parse_article(path, "invalid")
