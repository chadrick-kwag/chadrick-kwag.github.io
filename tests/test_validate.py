from pathlib import Path

import pytest

from tools.recover.validate import validate_recovery


def _post(root: Path, slug: str, front: str, body: str) -> Path:
    bundle = root / slug
    bundle.mkdir(parents=True)
    (bundle / "index.md").write_text(
        f"---\n{front}---\n{body}", encoding="utf-8"
    )
    return bundle


VALID_FRONT = "title: One\ndate: 2024-01-01\nslug: one\ndraft: false\n"


def test_missing_image_makes_recovery_invalid(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(posts, "one", VALID_FRONT, "Body.\n\n![alt](images/no.png)\n")

    result = validate_recovery(posts, 1)

    assert result["expected_count"] == 1
    assert result["article_count"] == 1
    assert result["missing_assets"] == ["one:images/no.png"]
    assert result["valid"] is False


def test_reports_malformed_front_matter(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(posts, "one", "title: [unterminated\n", "Body.\n")

    result = validate_recovery(posts, 1)

    assert result["missing_fields"] == ["one:front_matter"]
    assert result["valid"] is False


def test_reports_empty_required_values_and_body(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        "title: ''\ndate: null\nslug: ''\ndraft: false\n",
        " \n\t\n",
    )

    result = validate_recovery(posts, 1)

    assert result["missing_fields"] == ["one:date", "one:slug", "one:title"]
    assert result["empty_bodies"] == ["one"]
    assert result["valid"] is False


def test_rejects_image_traversal_and_symlink_escape(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    bundle = _post(
        posts,
        "one",
        VALID_FRONT,
        "![up](../outside.png) ![link](images/link.png)\n",
    )
    (bundle / "images").mkdir()
    (bundle / "images/link.png").symlink_to(outside)

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == [
        "one:../outside.png",
        "one:images/link.png",
    ]


def test_accepts_encoded_unicode_image_and_ignores_query_fragment(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    bundle = _post(
        posts,
        "one",
        VALID_FRONT,
        "![그림](<images/%ED%95%9C%EA%B8%80.png?raw=1#view> \"title\")\n",
    )
    (bundle / "images").mkdir()
    (bundle / "images/한글.png").write_bytes(b"image")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == []
    assert result["valid"] is True


def test_rejects_zero_byte_local_asset(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    bundle = _post(
        posts,
        "one",
        VALID_FRONT,
        "![empty](images/empty.png)\n",
    )
    (bundle / "images").mkdir()
    (bundle / "images/empty.png").write_bytes(b"")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == ["one:images/empty.png"]
    assert result["valid"] is False


def test_internal_post_link_accepts_query_fragment_and_percent_encoding(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "[next](</posts/%ED%95%9C%EA%B8%80/?from=one#section> \"go\")\n",
    )
    _post(
        posts,
        "한글",
        "title: Two\ndate: 2024-01-02\nslug: 한글\ndraft: false\n",
        "Body.\n",
    )

    result = validate_recovery(posts, 2)

    assert result["broken_post_links"] == []
    assert result["valid"] is True


def test_reports_broken_post_link_and_is_deterministically_sorted(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "[z](/posts/z/) and [a](</posts/a/#part> 'title')\n",
    )

    result = validate_recovery(posts, 1)

    assert result["broken_post_links"] == ["one:a", "one:z"]
    assert result["valid"] is False


def test_count_mismatch_is_invalid(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(posts, "one", VALID_FRONT, "Body.\n")

    result = validate_recovery(posts, 2)

    assert result["article_count"] == 1
    assert result["valid"] is False


@pytest.mark.parametrize(
    ("body", "asset"),
    [
        ("![alt][pic]\n\n[pic]: images/ref.png 'title'\n", "images/ref.png"),
        ("![alt][]\n\n[alt]: <images/collapsed.png>\n", "images/collapsed.png"),
        ("![alt]\n\n[alt]: images/shortcut.png\n", "images/shortcut.png"),
        ('<img alt="raw" src="images/raw.png?x=1#y">\n', "images/raw.png"),
    ],
)
@pytest.mark.parametrize("exists", [False, True])
def test_validates_reference_and_raw_html_image_assets(
    tmp_path: Path, body: str, asset: str, exists: bool
) -> None:
    posts = tmp_path / "posts"
    bundle = _post(posts, "one", VALID_FRONT, body)
    if exists:
        target = bundle / asset
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"image")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == ([] if exists else [f"one:{asset}"])
    assert result["valid"] is exists


def test_ignores_image_examples_inside_inline_and_fenced_code(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "`![inline](missing-inline.png)`\n\n"
        "````md\n![backtick](missing-backtick.png)\n```\n````\n\n"
        "~~~~ markdown\n![tilde](missing-tilde.png)\n~~~~\n",
    )

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == []
    assert result["valid"] is True


def test_rejects_invalid_metadata_types_values_and_slug_mismatch(
    tmp_path: Path,
) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        "title: 42\ndate: nope\nslug: different\ndraft: null\n",
        "Body.\n",
    )

    result = validate_recovery(posts, 1)

    assert result["invalid_fields"] == [
        "one:date", "one:draft", "one:slug", "one:title"
    ]
    assert result["valid"] is False


def test_reports_duplicate_metadata_slugs_deterministically(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    duplicate = "date: 2024-01-01\nslug: same\ndraft: false\n"
    _post(posts, "a", f"title: A\n{duplicate}", "A\n")
    _post(posts, "b", f"title: B\n{duplicate}", "B\n")

    result = validate_recovery(posts, 2)

    assert result["duplicate_slugs"] == ["same"]
    assert result["valid"] is False


@pytest.mark.parametrize("kind", ["bundle", "index"])
def test_rejects_symlinked_bundle_or_index_without_reading_external_bytes(
    tmp_path: Path, kind: str
) -> None:
    posts = tmp_path / "posts"
    posts.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / "index.md"
    external.write_bytes(b"\xff")
    try:
        if kind == "bundle":
            (posts / "one").symlink_to(outside, target_is_directory=True)
        else:
            bundle = posts / "one"
            bundle.mkdir()
            (bundle / "index.md").symlink_to(external)
    except OSError:
        pytest.skip("symlinks are unavailable")

    result = validate_recovery(posts, 1)

    assert result["unsafe_bundles"] == ["one"]
    assert result["valid"] is False


@pytest.mark.parametrize(
    "body",
    [
        "[next][target]\n\n[target]: /posts/two/?from=one#part\n",
        '<a href="/posts/two/?from=one#part">next</a>\n',
    ],
)
def test_reference_and_raw_html_internal_links_resolve(
    tmp_path: Path, body: str
) -> None:
    posts = tmp_path / "posts"
    _post(posts, "one", VALID_FRONT, body)
    _post(
        posts,
        "two",
        "title: Two\ndate: 2024-01-02\nslug: two\ndraft: false\n",
        "Body.\n",
    )

    result = validate_recovery(posts, 2)

    assert result["broken_post_links"] == []
    assert result["valid"] is True


@pytest.mark.parametrize(
    "body",
    [
        "[next][target]\n\n[target]: /posts/missing/?from=one#part\n",
        '<a href="/posts/missing/?from=one#part">next</a>\n',
    ],
)
def test_reference_and_raw_html_internal_links_report_broken(
    tmp_path: Path, body: str
) -> None:
    posts = tmp_path / "posts"
    _post(posts, "one", VALID_FRONT, body)

    result = validate_recovery(posts, 1)

    assert result["broken_post_links"] == ["one:missing"]
    assert result["valid"] is False


def test_ignores_assets_and_links_in_indented_code_blocks(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "    ![example](missing.png)\n"
        "\n"
        "    [example](/posts/missing/)\n"
        "\t<img src=\"also-missing.png\">\n",
    )

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == []
    assert result["broken_post_links"] == []
    assert result["valid"] is True


def test_validates_nested_list_image_and_link_destinations(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "- nested item\n\n"
        "    ![nested](images/nested.png)\n\n"
        "    [next](/posts/missing/)\n",
    )

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == ["one:images/nested.png"]
    assert result["broken_post_links"] == ["one:missing"]
    assert result["valid"] is False


def test_validates_every_local_raw_html_srcset_candidate(tmp_path: Path) -> None:
    posts = tmp_path / "posts"
    bundle = _post(
        posts,
        "one",
        VALID_FRONT,
        '<img src="images/main.png" '
        'srcset="data:image/png;base64,AAAA 0.5x, images/small.png 1x, '
        'images/large%20copy.png 2x">\n',
    )
    images = bundle / "images"
    images.mkdir()
    (images / "main.png").write_bytes(b"main")
    (images / "small.png").write_bytes(b"small")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == ["one:images/large copy.png"]
    assert result["valid"] is False


@pytest.mark.parametrize("exists", [False, True])
def test_validates_picture_source_srcset_candidates(
    tmp_path: Path, exists: bool
) -> None:
    posts = tmp_path / "site/content/posts"
    bundle = _post(
        posts,
        "one",
        VALID_FRONT,
        '<picture><source srcset="data:image/webp;base64,AAAA 1x, '
        'images/picture.webp 2x"><img src="images/fallback.png"></picture>\n',
    )
    images = bundle / "images"
    images.mkdir()
    (images / "fallback.png").write_bytes(b"fallback")
    if exists:
        (images / "picture.webp").write_bytes(b"picture")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == (
        [] if exists else ["one:images/picture.webp"]
    )
    assert result["valid"] is exists


def test_validates_root_relative_post_and_static_assets(tmp_path: Path) -> None:
    posts = tmp_path / "site/content/posts"
    _post(
        posts,
        "one",
        VALID_FRONT,
        "![post](/posts/one/images/post.png?raw=1#view)\n"
        "![static](/images/global.png)\n"
        "![missing](/images/missing.png)\n"
        "![external](//cdn.example/image.png)\n",
    )
    post_images = posts / "one/images"
    post_images.mkdir()
    (post_images / "post.png").write_bytes(b"post")
    static_images = tmp_path / "site/static/images"
    static_images.mkdir(parents=True)
    (static_images / "global.png").write_bytes(b"global")

    result = validate_recovery(posts, 1)

    assert result["missing_assets"] == ["one:/images/missing.png"]
    assert result["valid"] is False


@pytest.mark.parametrize(
    "destination",
    [
        "/../outside.png",
        "/posts/one/../two/image.png",
        "/posts/one/%2e%2e/two/image.png",
        "/posts/one/%252e%252e/two/image.png",
    ],
)
def test_rejects_root_relative_asset_traversal(
    tmp_path: Path, destination: str
) -> None:
    posts = tmp_path / "site/content/posts"
    _post(posts, "one", VALID_FRONT, f"![unsafe]({destination})\n")

    result = validate_recovery(posts, 1)

    assert len(result["missing_assets"]) == 1
    assert result["missing_assets"][0].startswith("one:/")
    assert result["valid"] is False
