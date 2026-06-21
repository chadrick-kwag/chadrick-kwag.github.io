import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml


ROOT = Path(__file__).parents[1]
SITE = ROOT / "site"
PAPERMOD_VERSION = "v0.0.0-20240915081152-a2eb47bb4b80"


def test_hugo_version_is_pinned():
    assert (ROOT / ".hugo-version").read_text() == "0.163.3\n"


def test_papermod_module_is_pinned():
    go_mod = (SITE / "go.mod").read_text()
    assert "module example.org/chadrick-blog" in go_mod
    assert (
        f"github.com/adityatelange/hugo-PaperMod {PAPERMOD_VERSION}" in go_mod
    )
    go_sum_lines = (SITE / "go.sum").read_text().splitlines()
    assert len(go_sum_lines) == 2
    assert all(
        f"github.com/adityatelange/hugo-PaperMod {PAPERMOD_VERSION}" in line
        for line in go_sum_lines
    )


def test_hugo_configuration():
    config = yaml.safe_load((SITE / "hugo.yaml").read_text())
    assert config == {
        "baseURL": "https://example.invalid/",
        "locale": "en-us",
        "title": "Chadrick Blog",
        "theme": [],
        "enableRobotsTXT": True,
        "permalinks": {"posts": "/posts/:slug/"},
        "pagination": {"pagerSize": 10},
        "outputs": {"home": ["HTML", "RSS", "JSON"]},
        "module": {
            "imports": [{"path": "github.com/adityatelange/hugo-PaperMod"}]
        },
        "params": {
            "env": "production",
            "defaultTheme": "auto",
            "ShowCodeCopyButtons": True,
            "ShowReadingTime": True,
            "ShowPostNavLinks": True,
            "ShowBreadCrumbs": True,
            "fuseOpts": {
                "isCaseSensitive": False,
                "shouldSort": True,
                "location": 0,
                "distance": 1000,
                "threshold": 0.4,
                "minMatchCharLength": 0,
                "keys": ["title", "permalink", "summary", "content"],
            },
        },
        "menu": {
            "main": [
                {
                    "identifier": "archives",
                    "name": "Archives",
                    "url": "/archives/",
                    "weight": 10,
                },
                {
                    "identifier": "search",
                    "name": "Search",
                    "url": "/search/",
                    "weight": 20,
                },
            ]
        },
    }


def test_content_pages_have_expected_front_matter():
    expected = {
        "_index.md": {"title": "Chadrick Blog"},
        "archives.md": {
            "title": "Archives",
            "layout": "archives",
            "url": "/archives/",
            "summary": "archives",
        },
        "search.md": {
            "title": "Search",
            "layout": "search",
            "url": "/search/",
            "summary": "search",
            "placeholder": "Search posts",
        },
    }
    for filename, front_matter in expected.items():
        text = (SITE / "content" / filename).read_text()
        assert text.startswith("---\n") and text.endswith("---\n")
        assert yaml.safe_load(text.removeprefix("---\n").removesuffix("---\n")) == front_matter


def _require_hugo(env=os.environ, local_bin=ROOT / ".tools" / "bin" / "hugo", which=shutil.which):
    candidates = [env.get("HUGO_BIN"), local_bin, which("hugo")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    pytest.skip("Hugo binary unavailable: set HUGO_BIN or install Hugo 0.163.3 Extended")


def test_missing_hugo_binary_is_an_explicit_skip(tmp_path):
    with pytest.raises(pytest.skip.Exception, match="Hugo binary unavailable"):
        _require_hugo(env={}, local_bin=tmp_path / "missing", which=lambda _: None)


def test_hugo_build_has_no_compatibility_sentinel_or_fake_author(tmp_path):
    hugo = _require_hugo()
    version = subprocess.run(
        [hugo, "version"], check=True, capture_output=True, text=True
    ).stdout
    assert "v0.163.3" in version
    assert "+extended" in version

    destination = tmp_path / "public"
    result = subprocess.run(
        [
            hugo,
            "--source",
            SITE,
            "--destination",
            destination,
            "--minify",
            "--baseURL",
            "https://example.invalid/",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    warnings = [
        line for line in (result.stdout + result.stderr).splitlines() if line.startswith("WARN")
    ]
    # Pinned PaperMod warnings must be explicitly audited; owned config/overrides allow none.
    assert warnings == []
    rendered = "\n".join(
        path.read_text(errors="replace")
        for path in destination.rglob("*")
        if path.is_file()
    )
    assert "_compat" not in rendered
    assert "map[_compat:true]" not in rendered
    assert "<author>" not in (destination / "index.xml").read_text()
