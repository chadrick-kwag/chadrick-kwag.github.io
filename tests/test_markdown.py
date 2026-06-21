from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag

from tools.recover.markdown import (
    SITE_HOST,
    SUPPORTED,
    MarkdownResult,
    RecoveryConverter,
    _rewrite_url,
    convert_content,
)


FIXTURE = Path(__file__).parent / "fixtures" / "article.html"


def _section(html: str) -> Tag:
    section = BeautifulSoup(html, "html.parser").find("section")
    assert isinstance(section, Tag)
    return section


def test_public_api_constants_and_frozen_result() -> None:
    assert SITE_HOST == "chadrick-kwag.net"
    assert {"a", "blockquote", "br", "code", "del", "div", "em", "figure",
            "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img",
            "li", "ol", "p", "pre", "section", "span", "strong", "table",
            "tbody", "td", "th", "thead", "tr", "ul"} <= SUPPORTED
    result = MarkdownResult("body\n", (), ())
    with pytest.raises(AttributeError):
        result.markdown = "changed"
    assert isinstance(RecoveryConverter(), RecoveryConverter)


def test_recovery_converter_defaults_strip_wrappers_and_preserve_unknown_html() -> None:
    converted = RecoveryConverter().convert(
        "<section><div><span>body</span><unknown-tag>raw</unknown-tag></div></section>"
    )

    assert "<section>" not in converted
    assert "<div>" not in converted
    assert "<span>" not in converted
    assert "body<unknown-tag>raw</unknown-tag>" in converted


def test_convert_fixture_to_markdown_and_reports_assets_and_elements() -> None:
    soup = BeautifulSoup(FIXTURE.read_text(encoding="utf-8"), "html.parser")
    content = soup.find("section")
    assert isinstance(content, Tag)

    result = convert_content(content)

    assert "Hello **world**." in result.markdown
    assert "[Other](/posts/other/)" in result.markdown
    assert '```python\nprint("ok")\n```' in result.markdown
    assert "| A |" in result.markdown
    assert "![capture](images/캡처.png)" in result.markdown
    assert "<custom-element" in result.markdown
    assert result.local_assets == ("images/캡처.png",)
    assert result.unsupported_elements == ("custom-element",)
    assert result.markdown.endswith("\n")


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://chadrick-kwag.net/a%20b/?x=a%20b#c%20d", "/a%20b/?x=a%20b#c%20d"),
        ("https://chadrick-kwag.net/%7Euser", "/~user"),
        ("images/%EC%BA%A1%EC%B2%98.png", "images/캡처.png"),
        ("images/a%2Fb%3Fc%23d.png", "images/a%2Fb%3Fc%23d.png"),
        ("images/%2e%2e/secret.png", "images/%2e%2e/secret.png"),
        ("http://chadrick-kwag.net/path", "/path"),
        ("https://external.example/path", "https://external.example/path"),
        (
            "https://chadrick-kwag.net.evil.example/path",
            "https://chadrick-kwag.net.evil.example/path",
        ),
        (
            "https://evil.example/chadrick-kwag.net/path",
            "https://evil.example/chadrick-kwag.net/path",
        ),
    ],
)
def test_rewrite_url_only_rewrites_exact_same_site_host(url: str, expected: str) -> None:
    assert _rewrite_url(url) == expected


def test_convert_rewrites_links_and_images_and_deduplicates_assets() -> None:
    content = _section(
        '<section><a href="https://chadrick-kwag.net/post?q=x%20y#part">Post</a>'
        '<img src="images/a%20b.png"><img src="images/a%20b.png">'
        '<img src="/images/root.png"><img src="https://cdn.example/a.png">'
        '<img src="data:image/png;base64,x"></section>'
    )

    result = convert_content(content)

    assert "[Post](/post?q=x%20y#part)" in result.markdown
    assert result.local_assets == ("images/a b.png",)


def test_local_asset_is_decoded_to_an_existing_filesystem_path(
    tmp_path: Path,
) -> None:
    image = tmp_path / "images" / "a b.png"
    image.parent.mkdir()
    image.write_bytes(b"image")
    result = convert_content(
        _section('<section><img alt="a" src="images/a%20b.png"></section>')
    )

    assert "![a](images/a%20b.png)" in result.markdown
    assert result.local_assets == ("images/a b.png",)
    assert (tmp_path / result.local_assets[0]).read_bytes() == b"image"


def test_local_asset_decodes_reserved_filename_characters_for_filesystem() -> None:
    result = convert_content(
        _section(
            '<section><img alt="a" src="images/a%23b%3Fc.png"></section>'
        )
    )

    assert "![a](images/a%23b%3Fc.png)" in result.markdown
    assert result.local_assets == ("images/a#b?c.png",)


def test_local_asset_uses_path_while_markdown_retains_query_and_fragment() -> None:
    result = convert_content(
        _section('<section><img alt="a" src="images/a.png?v=1#x"></section>')
    )

    assert "![a](images/a.png?v=1#x)" in result.markdown
    assert result.local_assets == ("images/a.png",)


@pytest.mark.parametrize(
    "src",
    [
        "../secret.png",
        "images/../secret.png",
        "images/%2e%2e/secret.png",
        "images/%2E%2E/secret.png",
        "images/%252e%252e/secret.png",
        "%2Fetc/passwd",
    ],
)
def test_traversing_image_paths_are_not_local_assets(src: str) -> None:
    result = convert_content(
        _section(f'<section><img alt="bad" src="{src}"></section>')
    )

    assert result.local_assets == ()


def test_convert_does_not_mutate_content() -> None:
    content = _section(
        '<section><a href="https://chadrick-kwag.net/a%20b">Link</a>'
        '<img src="images/a%20b.png"></section>'
    )
    original = str(content)

    convert_content(content)

    assert str(content) == original


def test_unsupported_nested_markup_is_preserved_as_raw_html() -> None:
    content = _section(
        '<section><outer-tag id="one"><inner-tag data-x="2">'
        "raw <strong>bold</strong></inner-tag></outer-tag></section>"
    )

    result = convert_content(content)

    assert '<outer-tag id="one"><inner-tag data-x="2">raw <strong>bold</strong>' in result.markdown
    assert result.unsupported_elements == ("inner-tag", "outer-tag")


def test_stripped_wrappers_are_not_reported_or_rendered() -> None:
    result = convert_content(
        _section("<section><div><span>wrapped</span></div></section>")
    )

    assert result.markdown == "wrapped\n"
    assert result.unsupported_elements == ()


def test_pre_preserves_literal_code_text_and_language() -> None:
    result = convert_content(
        _section(
            '<section><pre><code class="foo language-js bar">'
            '<span>if (a &lt; b) {</span>\n  console.log("x");\n}'
            "</code></pre></section>"
        )
    )

    assert result.markdown == (
        '```js\nif (a < b) {\n  console.log("x");\n}\n```\n'
    )


def test_pre_preserves_existing_terminal_newlines_in_literal_code() -> None:
    result = convert_content(
        _section("<section><pre><code>line\n\n</code></pre></section>")
    )

    assert result.markdown == "```\nline\n\n```\n"


def test_pre_uses_a_longer_fence_than_backtick_runs_in_code() -> None:
    result = convert_content(
        _section("<section><pre><code>before\n```\nafter</code></pre></section>")
    )

    assert result.markdown == "````\nbefore\n```\nafter\n````\n"


def test_convert_requires_section() -> None:
    paragraph = BeautifulSoup("<p>body</p>", "html.parser").find("p")
    assert isinstance(paragraph, Tag)

    with pytest.raises(ValueError, match="section"):
        convert_content(paragraph)
