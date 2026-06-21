# Hugo S3 Blog Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Back up the published S3 blog and deterministically recover its 218 generated HTML articles into a tested, maintainable Hugo project. The 241 matching `posts/**/index.html` files comprise 218 articles, one posts index, and 22 pagination pages.

**Architecture:** Preserve the S3 tree as immutable input, convert one article at a time through focused Python modules, and validate the generated Hugo page bundles independently. The Hugo site uses PaperMod pinned to release `v8.0`; GitHub Pages workflow creation remains outside this plan until the GitHub username is known.

**Tech Stack:** Python 3.14, Beautiful Soup 4.15.0, markdownify 1.2.2, PyYAML 6.0.3, pytest 9.1.1, AWS CLI 2.35.9, Hugo Extended 0.163.3, Go modules, PaperMod v8.0 (`a2eb47bb4b805116dcd34c1605d39835121f8dbe`)

---

## File Map

- `pyproject.toml`: Python runtime, dependencies, and pytest configuration.
- `tools/recover/model.py`: immutable article and recovery result types.
- `tools/recover/inventory.py`: S3 manifest creation and local backup verification.
- `tools/recover/parser.py`: article metadata and content-container extraction.
- `tools/recover/markdown.py`: HTML normalization and Markdown conversion.
- `tools/recover/writer.py`: front matter, page bundle, and asset writing.
- `tools/recover/pipeline.py`: per-article orchestration and recovery report generation.
- `tools/recover/validate.py`: recovered-content, link, asset, and count validation.
- `tools/recover/__main__.py`: `inventory`, `recover`, and `validate` CLI commands.
- `tests/fixtures/article.html`: representative old Hugo/Paper article fixture.
- `tests/test_inventory.py`: manifest and backup comparison tests.
- `tests/test_parser.py`: metadata and content selection tests.
- `tests/test_markdown.py`: Markdown, URL, code, table, and raw HTML tests.
- `tests/test_writer.py`: page bundle and YAML front matter tests.
- `tests/test_pipeline.py`: success, warning, and failure report tests.
- `tests/test_validate.py`: acceptance-rule tests.
- `manifests/s3-objects.json`: generated remote inventory plus local SHA-256 values.
- `backup/s3/`: generated immutable S3 copy.
- `reports/recovery.json`: generated per-article recovery results.
- `reports/validation.json`: generated acceptance results.
- `site/hugo.yaml`: Hugo and PaperMod configuration.
- `site/go.mod`, `site/go.sum`: pinned PaperMod module dependency.
- `.hugo-version`: exact locally tested Hugo version.

### Task 1: Establish the Python Recovery Package

**Files:**
- Create: `pyproject.toml`
- Create: `tools/__init__.py`
- Create: `tools/recover/__init__.py`
- Modify: `.gitignore`

- [ ] **Step 1: Add the package configuration**

```toml
[build-system]
requires = ["setuptools>=82"]
build-backend = "setuptools.build_meta"

[project]
name = "chadrick-blog-recovery"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "beautifulsoup4==4.15.0",
  "markdownify==1.2.2",
  "PyYAML==6.0.3",
]

[project.optional-dependencies]
test = ["pytest==9.1.1"]

[tool.setuptools.packages.find]
include = ["tools*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

Create empty `tools/__init__.py` and `tools/recover/__init__.py`. Add these entries to `.gitignore`:

```gitignore
.venv/
*.egg-info/
.tools/
manifests/*.tmp
reports/*.tmp
```

- [ ] **Step 2: Install the isolated environment**

Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e '.[test]'
.venv/bin/python -c 'import bs4, markdownify, yaml; print("dependencies ok")'
```

Expected: `dependencies ok`.

- [ ] **Step 3: Commit the package skeleton**

```bash
git add .gitignore pyproject.toml tools/__init__.py tools/recover/__init__.py
git commit -m "build: scaffold blog recovery tooling"
```

### Task 2: Build and Verify the S3 Inventory

**Files:**
- Create: `tools/recover/inventory.py`
- Create: `tests/test_inventory.py`

- [ ] **Step 1: Write failing manifest comparison tests**

```python
from pathlib import Path

from tools.recover.inventory import ObjectRecord, compare_backup


def test_compare_backup_accepts_matching_file(tmp_path: Path):
    target = tmp_path / "posts/a/index.html"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"hello")
    records = [ObjectRecord("posts/a/index.html", 5, '"etag"', None)]

    result = compare_backup(tmp_path, records)

    assert result.missing == []
    assert result.size_mismatches == []
    assert result.extra == []
    assert result.sha256["posts/a/index.html"] == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_compare_backup_reports_missing_size_and_extra(tmp_path: Path):
    (tmp_path / "wrong.txt").write_bytes(b"x")
    (tmp_path / "extra.txt").write_bytes(b"extra")
    records = [
        ObjectRecord("missing.txt", 1, '"a"', None),
        ObjectRecord("wrong.txt", 2, '"b"', None),
    ]

    result = compare_backup(tmp_path, records)

    assert result.missing == ["missing.txt"]
    assert result.size_mismatches == ["wrong.txt"]
    assert result.extra == ["extra.txt"]
```

- [ ] **Step 2: Run the tests and confirm the missing module failure**

Run: `.venv/bin/pytest tests/test_inventory.py -v`

Expected: FAIL because `tools.recover.inventory` does not exist.

- [ ] **Step 3: Implement inventory records and local verification**

```python
# tools/recover/inventory.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class ObjectRecord:
    key: str
    size: int
    etag: str
    last_modified: str | None


@dataclass(frozen=True)
class BackupComparison:
    missing: list[str]
    size_mismatches: list[str]
    extra: list[str]
    sha256: dict[str, str]


def list_s3_objects(bucket: str) -> list[ObjectRecord]:
    command = [
        "aws", "s3api", "list-objects-v2", "--bucket", bucket,
        "--query", "Contents[].{key:Key,size:Size,etag:ETag,last_modified:LastModified}",
        "--output", "json",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    rows = json.loads(completed.stdout) or []
    return [ObjectRecord(**row) for row in rows]


def sync_bucket(bucket: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["aws", "s3", "sync", f"s3://{bucket}", str(destination), "--exact-timestamps"],
        check=True,
    )


def compare_backup(root: Path, records: list[ObjectRecord]) -> BackupComparison:
    expected = {record.key: record for record in records}
    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*") if path.is_file()
    }
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    size_mismatches = sorted(
        key for key in set(expected) & set(actual)
        if actual[key].stat().st_size != expected[key].size
    )
    digests = {
        key: sha256(path.read_bytes()).hexdigest()
        for key, path in sorted(actual.items()) if key in expected
    }
    return BackupComparison(missing, size_mismatches, extra, digests)


def write_manifest(path: Path, bucket: str, records: list[ObjectRecord], comparison: BackupComparison) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "bucket": bucket,
        "object_count": len(records),
        "total_size": sum(record.size for record in records),
        "objects": [asdict(record) | {"sha256": comparison.sha256.get(record.key)} for record in records],
        "verification": {
            "missing": comparison.missing,
            "size_mismatches": comparison.size_mismatches,
            "extra": comparison.extra,
        },
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
```

- [ ] **Step 4: Run the inventory tests**

Run: `.venv/bin/pytest tests/test_inventory.py -v`

Expected: 2 tests PASS.

- [ ] **Step 5: Commit inventory support**

```bash
git add tools/recover/inventory.py tests/test_inventory.py
git commit -m "feat: add verified S3 inventory support"
```

### Task 3: Parse Old Hugo Article Metadata and Content

**Files:**
- Create: `tools/recover/model.py`
- Create: `tools/recover/parser.py`
- Create: `tests/fixtures/article.html`
- Create: `tests/test_parser.py`

- [ ] **Step 1: Create a representative fixture**

```html
<!doctype html><html><head>
<meta itemprop="datePublished" content="2023-10-27T12:33:00+00:00">
<meta itemprop="dateModified" content="2023-10-28T12:33:00+00:00">
<meta property="og:title" content="Recovered post">
<meta property="og:url" content="https://chadrick-kwag.net/posts/recovered-post/">
</head><body><main><article>
<header><h1>Recovered post</h1></header>
<section>
<p>Hello <strong>world</strong>.</p>
<p><a href="https://chadrick-kwag.net/posts/other/">Other</a></p>
<pre><code class="language-python"><span>print(&quot;ok&quot;)</span></code></pre>
<table><tr><th>A</th></tr><tr><td>B</td></tr></table>
<img src="images/%EC%BA%A1%EC%B2%98.png" alt="capture">
<custom-element data-value="kept">raw</custom-element>
</section>
<footer><a href="/categories/python/">Python</a><a href="/tags/hugo/">Hugo</a></footer>
</article></main></body></html>
```

- [ ] **Step 2: Write failing parser tests**

```python
from pathlib import Path

from tools.recover.parser import parse_article


def test_parse_article_extracts_metadata_and_only_article_section():
    source = Path("tests/fixtures/article.html")
    article = parse_article(source, "recovered-post")

    assert article.slug == "recovered-post"
    assert article.title == "Recovered post"
    assert article.date == "2023-10-27T12:33:00+00:00"
    assert article.lastmod == "2023-10-28T12:33:00+00:00"
    assert article.categories == ("Python",)
    assert article.tags == ("Hugo",)
    assert article.source_path == source
    assert article.content.name == "section"
```

- [ ] **Step 3: Verify the parser test fails**

Run: `.venv/bin/pytest tests/test_parser.py -v`

Expected: FAIL because `parse_article` is undefined.

- [ ] **Step 4: Implement the article model and parser**

```python
# tools/recover/model.py
from dataclasses import dataclass
from pathlib import Path
from bs4.element import Tag


@dataclass(frozen=True)
class Article:
    slug: str
    title: str
    date: str
    lastmod: str
    categories: tuple[str, ...]
    tags: tuple[str, ...]
    source_path: Path
    content: Tag
```

```python
# tools/recover/parser.py
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.element import Tag

from tools.recover.model import Article


def _meta(soup: BeautifulSoup, *, prop: str | None = None, itemprop: str | None = None) -> str:
    attrs = {"property": prop} if prop else {"itemprop": itemprop}
    node = soup.find("meta", attrs=attrs)
    return str(node.get("content", "")).strip() if isinstance(node, Tag) else ""


def _taxonomy(article: Tag, prefix: str) -> tuple[str, ...]:
    values = {
        link.get_text(" ", strip=True)
        for link in article.select(f'a[href^="/{prefix}/"]')
        if link.get_text(" ", strip=True)
    }
    return tuple(sorted(values, key=str.casefold))


def parse_article(path: Path, slug: str) -> Article:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    article = soup.find("article")
    if not isinstance(article, Tag):
        raise ValueError("missing <article>")
    content = article.find("section", recursive=False)
    if not isinstance(content, Tag):
        raise ValueError("missing direct article <section>")
    heading = article.find("h1")
    title = _meta(soup, prop="og:title") or (heading.get_text(" ", strip=True) if heading else "")
    date = _meta(soup, itemprop="datePublished") or _meta(soup, prop="article:published_time")
    lastmod = _meta(soup, itemprop="dateModified") or _meta(soup, prop="article:modified_time") or date
    if not title or not date:
        raise ValueError("missing required title or publication date")
    return Article(
        slug=slug,
        title=title,
        date=date,
        lastmod=lastmod,
        categories=_taxonomy(article, "categories"),
        tags=_taxonomy(article, "tags"),
        source_path=path,
        content=content,
    )
```

- [ ] **Step 5: Run parser tests and commit**

Run: `.venv/bin/pytest tests/test_parser.py -v`

Expected: 1 test PASS.

```bash
git add tools/recover/model.py tools/recover/parser.py tests/fixtures/article.html tests/test_parser.py
git commit -m "feat: parse published Hugo articles"
```

### Task 4: Convert Article HTML to Stable Markdown

**Files:**
- Create: `tools/recover/markdown.py`
- Create: `tests/test_markdown.py`

- [ ] **Step 1: Write failing conversion tests**

```python
from pathlib import Path

from tools.recover.markdown import convert_content
from tools.recover.parser import parse_article


def test_convert_content_preserves_structure_and_rewrites_urls():
    article = parse_article(Path("tests/fixtures/article.html"), "recovered-post")

    result = convert_content(article.content)

    assert "Hello **world**." in result.markdown
    assert "[Other](/posts/other/)" in result.markdown
    assert '```python\nprint("ok")\n```' in result.markdown
    assert "| A |" in result.markdown
    assert "![capture](images/캡처.png)" in result.markdown
    assert "<custom-element" in result.markdown
    assert result.local_assets == ("images/캡처.png",)
    assert result.unsupported_elements == ("custom-element",)
```

- [ ] **Step 2: Verify conversion tests fail**

Run: `.venv/bin/pytest tests/test_markdown.py -v`

Expected: FAIL because `tools.recover.markdown` does not exist.

- [ ] **Step 3: Implement normalization and Markdown conversion**

```python
# tools/recover/markdown.py
from dataclasses import dataclass
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag
from markdownify import MarkdownConverter

SITE_HOST = "chadrick-kwag.net"
SUPPORTED = {
    "a", "blockquote", "br", "code", "del", "div", "em", "figure", "figcaption",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img", "li", "ol", "p", "pre",
    "section", "span", "strong", "table", "tbody", "td", "th", "thead", "tr", "ul",
}


@dataclass(frozen=True)
class MarkdownResult:
    markdown: str
    local_assets: tuple[str, ...]
    unsupported_elements: tuple[str, ...]


class RecoveryConverter(MarkdownConverter):
    def get_conv_fn(self, tag_name):
        convert = super().get_conv_fn(tag_name)
        if convert is not None or tag_name in (self.options.get("strip") or []):
            return convert
        return lambda el, text, parent_tags: str(el)

    def convert_pre(self, el, text, parent_tags):
        code = el.find("code")
        language = ""
        if code:
            for class_name in code.get("class", []):
                if class_name.startswith("language-"):
                    language = class_name.removeprefix("language-")
                    break
        value = code.get_text() if code else el.get_text()
        return f"\n```{language}\n{value.rstrip()}\n```\n"


def _rewrite_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.netloc == SITE_HOST:
        value = parsed.path or "/"
        if parsed.query:
            value += f"?{parsed.query}"
        if parsed.fragment:
            value += f"#{parsed.fragment}"
    return unquote(value)


def convert_content(content: Tag) -> MarkdownResult:
    soup = BeautifulSoup(str(content), "html.parser")
    root = soup.find("section")
    if not isinstance(root, Tag):
        raise ValueError("content section was lost during normalization")
    local_assets: set[str] = set()
    unsupported: set[str] = set()
    for tag in root.find_all(True):
        if tag.name not in SUPPORTED:
            unsupported.add(tag.name)
        if tag.name == "a" and tag.get("href"):
            tag["href"] = _rewrite_url(str(tag["href"]))
        if tag.name == "img" and tag.get("src"):
            tag["src"] = _rewrite_url(str(tag["src"]))
            if not urlparse(str(tag["src"])).scheme and not str(tag["src"]).startswith("/"):
                local_assets.add(str(tag["src"]))
    markdown = RecoveryConverter(
        heading_style="ATX",
        bullets="-",
        strip=["section", "span", "div"],
        escape_asterisks=False,
        escape_underscores=False,
    ).convert_soup(root).strip() + "\n"
    return MarkdownResult(markdown, tuple(sorted(local_assets)), tuple(sorted(unsupported)))
```

- [ ] **Step 4: Run conversion tests and commit**

Run: `.venv/bin/pytest tests/test_markdown.py -v`

Expected: 1 test PASS. If markdownify emits equivalent table spacing, normalize the exact expected fixture and retain semantic assertions for headers and cell values.

```bash
git add tools/recover/markdown.py tests/test_markdown.py
git commit -m "feat: convert article HTML to Markdown"
```

### Task 5: Write Hugo Page Bundles and Recovery Reports

**Files:**
- Create: `tools/recover/writer.py`
- Create: `tools/recover/pipeline.py`
- Create: `tests/test_writer.py`
- Create: `tests/test_pipeline.py`

- [ ] **Step 1: Write failing page-bundle tests**

```python
from pathlib import Path
import yaml

from tools.recover.markdown import MarkdownResult
from tools.recover.parser import parse_article
from tools.recover.writer import write_bundle


def test_write_bundle_creates_front_matter_body_and_assets(tmp_path: Path):
    source = tmp_path / "backup/posts/recovered-post"
    source.mkdir(parents=True)
    fixture = Path("tests/fixtures/article.html")
    (source / "index.html").write_bytes(fixture.read_bytes())
    (source / "images").mkdir()
    (source / "images/캡처.png").write_bytes(b"png")
    article = parse_article(source / "index.html", "recovered-post")
    converted = MarkdownResult("Body\n", ("images/캡처.png",), ())

    copied = write_bundle(article, converted, tmp_path / "site/content/posts")

    output = tmp_path / "site/content/posts/recovered-post/index.md"
    text = output.read_text(encoding="utf-8")
    _, front_matter, body = text.split("---\n", 2)
    metadata = yaml.safe_load(front_matter)
    assert metadata["slug"] == "recovered-post"
    assert metadata["draft"] is False
    assert body == "Body\n"
    assert copied == ("images/캡처.png",)
```

- [ ] **Step 2: Run the writer test and verify failure**

Run: `.venv/bin/pytest tests/test_writer.py -v`

Expected: FAIL because `write_bundle` does not exist.

- [ ] **Step 3: Implement atomic bundle writing**

```python
# tools/recover/writer.py
from pathlib import Path
import shutil
import tempfile
import yaml

from tools.recover.markdown import MarkdownResult
from tools.recover.model import Article


def write_bundle(article: Article, converted: MarkdownResult, posts_root: Path) -> tuple[str, ...]:
    posts_root.mkdir(parents=True, exist_ok=True)
    destination = posts_root / article.slug
    with tempfile.TemporaryDirectory(dir=posts_root) as temporary:
        staged = Path(temporary) / article.slug
        staged.mkdir()
        metadata = {
            "title": article.title,
            "date": article.date,
            "lastmod": article.lastmod,
            "slug": article.slug,
            "categories": list(article.categories),
            "tags": list(article.tags),
            "draft": False,
        }
        front_matter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
        (staged / "index.md").write_text(
            f"---\n{front_matter}---\n{converted.markdown}", encoding="utf-8"
        )
        copied = []
        source_root = article.source_path.parent
        for relative in converted.local_assets:
            source = source_root / relative
            if not source.is_file():
                continue
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(relative)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(staged), destination)
    return tuple(sorted(copied))
```

- [ ] **Step 4: Write failing pipeline report tests**

```python
from pathlib import Path

from tools.recover.pipeline import recover_all


def test_recover_all_records_success_and_failure(tmp_path: Path):
    source = tmp_path / "backup/posts"
    good = source / "good"
    bad = source / "bad"
    good.mkdir(parents=True)
    bad.mkdir(parents=True)
    good_html = Path("tests/fixtures/article.html").read_text(encoding="utf-8")
    (good / "index.html").write_text(good_html, encoding="utf-8")
    (bad / "index.html").write_text("<html></html>", encoding="utf-8")

    report = recover_all(source, tmp_path / "site/content/posts")

    assert report["source_count"] == 2
    assert report["success_count"] == 1
    assert report["failure_count"] == 1
    assert report["articles"][0]["slug"] == "bad"
    assert report["articles"][0]["status"] == "failed"
```

- [ ] **Step 5: Implement deterministic per-article orchestration**

```python
# tools/recover/pipeline.py
from pathlib import Path

from tools.recover.markdown import convert_content
from tools.recover.parser import parse_article
from tools.recover.writer import write_bundle


def recover_all(source_posts: Path, destination_posts: Path) -> dict:
    sources = sorted(source_posts.glob("*/index.html"))
    results = []
    for source in sources:
        slug = source.parent.name
        try:
            article = parse_article(source, slug)
            converted = convert_content(article.content)
            copied = write_bundle(article, converted, destination_posts)
            missing = sorted(set(converted.local_assets) - set(copied))
            source_text = article.content.get_text(" ", strip=True)
            results.append({
                "slug": slug,
                "status": "warning" if missing or converted.unsupported_elements else "ok",
                "source": source.as_posix(),
                "output": (destination_posts / slug / "index.md").as_posix(),
                "source_text_length": len(source_text),
                "markdown_length": len(converted.markdown),
                "copied_assets": list(copied),
                "missing_assets": missing,
                "unsupported_elements": list(converted.unsupported_elements),
                "error": None,
            })
        except Exception as error:
            results.append({
                "slug": slug, "status": "failed", "source": source.as_posix(),
                "output": None, "source_text_length": 0, "markdown_length": 0,
                "copied_assets": [], "missing_assets": [], "unsupported_elements": [],
                "error": f"{type(error).__name__}: {error}",
            })
    return {
        "source_count": len(sources),
        "success_count": sum(row["status"] != "failed" for row in results),
        "failure_count": sum(row["status"] == "failed" for row in results),
        "warning_count": sum(row["status"] == "warning" for row in results),
        "articles": results,
    }
```

- [ ] **Step 6: Run writer and pipeline tests and commit**

Run: `.venv/bin/pytest tests/test_writer.py tests/test_pipeline.py -v`

Expected: 2 tests PASS.

```bash
git add tools/recover/writer.py tools/recover/pipeline.py tests/test_writer.py tests/test_pipeline.py
git commit -m "feat: generate Hugo page bundles and reports"
```

### Task 6: Add CLI Commands and Create the Verified Backup

**Files:**
- Create: `tools/recover/__main__.py`
- Create: `manifests/.gitkeep`
- Create: `reports/.gitkeep`

- [ ] **Step 1: Implement explicit CLI commands**

```python
# tools/recover/__main__.py
import argparse
import json
from pathlib import Path

from tools.recover.inventory import compare_backup, list_s3_objects, sync_bucket, write_manifest
from tools.recover.pipeline import recover_all


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory")
    inventory.add_argument("--bucket", required=True)
    inventory.add_argument("--backup", type=Path, required=True)
    inventory.add_argument("--manifest", type=Path, required=True)
    recover = commands.add_parser("recover")
    recover.add_argument("--backup", type=Path, required=True)
    recover.add_argument("--site", type=Path, required=True)
    recover.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "inventory":
        records = list_s3_objects(args.bucket)
        sync_bucket(args.bucket, args.backup)
        comparison = compare_backup(args.backup, records)
        write_manifest(args.manifest, args.bucket, records, comparison)
        return 1 if comparison.missing or comparison.size_mismatches or comparison.extra else 0
    report = recover_all(args.backup / "posts", args.site / "content/posts")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if report["failure_count"] or report["source_count"] != report["success_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Verify CLI help**

Run: `.venv/bin/python -m tools.recover --help`

Expected: help lists `inventory` and `recover`.

- [ ] **Step 3: Download and verify AWS content**

Run:

```bash
set -a
source .env
set +a
.venv/bin/python -m tools.recover inventory \
  --bucket chadrick-kwag.net \
  --backup backup/s3 \
  --manifest manifests/s3-objects.json
```

Expected: exit 0; `manifests/s3-objects.json` reports `object_count: 1917`, `total_size: 29764583`, and empty `missing`, `size_mismatches`, and `extra` lists. If the bucket changed since discovery, inspect the delta and update the documented baseline before continuing.

- [ ] **Step 4: Commit the CLI and verified manifest**

```bash
touch manifests/.gitkeep reports/.gitkeep
git add tools/recover/__main__.py backup/s3 manifests/s3-objects.json \
  manifests/.gitkeep reports/.gitkeep
git commit -m "feat: back up and inventory published blog"
```

The 29.8 MB backup is committed because preserving the AWS-derived public files in this repository is an explicit goal. Confirm no individual object exceeds GitHub's per-file limit before the later remote push with `find backup/s3 -type f -size +90M -print`; expected output is empty.

### Task 7: Scaffold the Pinned Hugo Site

**Files:**
- Create: `.hugo-version`
- Create: `site/hugo.yaml`
- Create: `site/go.mod`
- Create: `site/go.sum`
- Create: `site/content/_index.md`
- Create: `site/content/archives.md`
- Create: `site/content/search.md`

- [ ] **Step 1: Install and verify build prerequisites**

Install Go and download the exact official Hugo Extended binary on macOS:

```bash
brew install go
mkdir -p .tools/bin .tools/downloads
curl -fL \
  https://github.com/gohugoio/hugo/releases/download/v0.163.3/hugo_extended_0.163.3_darwin-universal.tar.gz \
  -o .tools/downloads/hugo.tar.gz
tar -xzf .tools/downloads/hugo.tar.gz -C .tools/bin hugo
.tools/bin/hugo version
go version
```

Expected: Hugo reports `v0.163.3+extended` and Go is available.

- [ ] **Step 2: Pin the theme module**

```bash
printf '%s\n' '0.163.3' > .hugo-version
mkdir -p site/content
cd site
go mod init example.org/chadrick-blog
../.tools/bin/hugo mod get github.com/adityatelange/hugo-PaperMod@a2eb47bb4b805116dcd34c1605d39835121f8dbe
cd ..
```

Expected: `site/go.mod` and `site/go.sum` pin a pseudo-version resolving to commit `a2eb47bb4b805116dcd34c1605d39835121f8dbe`.

- [ ] **Step 3: Add deterministic Hugo configuration**

```yaml
# site/hugo.yaml
baseURL: https://example.invalid/
languageCode: en-us
title: Chadrick Blog
theme: []
enableRobotsTXT: true
permalinks:
  posts: /posts/:slug/
pagination:
  pagerSize: 10
outputs:
  home:
    - HTML
    - RSS
    - JSON
module:
  imports:
    - path: github.com/adityatelange/hugo-PaperMod
params:
  env: production
  defaultTheme: auto
  ShowCodeCopyButtons: true
  ShowReadingTime: true
  ShowPostNavLinks: true
  ShowBreadCrumbs: true
  fuseOpts:
    isCaseSensitive: false
    shouldSort: true
    location: 0
    distance: 1000
    threshold: 0.4
    minMatchCharLength: 0
    keys:
      - title
      - permalink
      - summary
      - content
menu:
  main:
    - identifier: archives
      name: Archives
      url: /archives/
      weight: 10
    - identifier: search
      name: Search
      url: /search/
      weight: 20
```

```markdown
<!-- site/content/_index.md -->
---
title: Chadrick Blog
---
```

```markdown
<!-- site/content/archives.md -->
---
title: Archives
layout: archives
url: /archives/
summary: archives
---
```

```markdown
<!-- site/content/search.md -->
---
title: Search
layout: search
url: /search/
summary: search
placeholder: Search posts
---
```

- [ ] **Step 4: Verify an empty Hugo build and commit**

Run: `.tools/bin/hugo --source site --minify --baseURL https://example.invalid/`

Expected: exit 0 and generated `site/public/index.html`.

```bash
git add .hugo-version site/hugo.yaml site/go.mod site/go.sum site/content
git commit -m "feat: scaffold pinned Hugo PaperMod site"
```

### Task 8: Recover All Articles and Validate Acceptance Rules

**Files:**
- Create: `tools/recover/validate.py`
- Create: `tests/test_validate.py`
- Modify: `tools/recover/__main__.py`
- Generate: `site/content/posts/**`
- Generate: `reports/recovery.json`
- Generate: `reports/validation.json`

- [ ] **Step 1: Write failing validator tests**

```python
from pathlib import Path

from tools.recover.validate import validate_recovery


def test_validate_recovery_reports_missing_assets_and_required_fields(tmp_path: Path):
    posts = tmp_path / "site/content/posts"
    bundle = posts / "one"
    bundle.mkdir(parents=True)
    (bundle / "index.md").write_text(
        "---\ntitle: One\ndate: 2020-01-01T00:00:00Z\nslug: one\ndraft: false\n---\n"
        "Body ![missing](images/no.png)\n",
        encoding="utf-8",
    )

    result = validate_recovery(posts, expected_count=1)

    assert result["valid"] is False
    assert result["article_count"] == 1
    assert result["missing_assets"] == ["one:images/no.png"]
```

- [ ] **Step 2: Run validator tests and confirm failure**

Run: `.venv/bin/pytest tests/test_validate.py -v`

Expected: FAIL because `validate_recovery` does not exist.

- [ ] **Step 3: Implement count, front matter, body, asset, and link checks**

```python
# tools/recover/validate.py
from pathlib import Path
import re
import yaml

IMAGE = re.compile(r"!\[[^]]*\]\(([^)]+)\)")
INTERNAL_POST = re.compile(r"\[[^]]+\]\(/posts/([^/)]+)/?[^)]*\)")


def _read_page(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    _, front_matter, body = text.split("---\n", 2)
    return yaml.safe_load(front_matter) or {}, body


def validate_recovery(posts_root: Path, expected_count: int) -> dict:
    pages = sorted(posts_root.glob("*/index.md"))
    slugs = {page.parent.name for page in pages}
    missing_fields = []
    empty_bodies = []
    missing_assets = []
    broken_post_links = []
    for page in pages:
        metadata, body = _read_page(page)
        slug = page.parent.name
        absent = [key for key in ("title", "date", "slug", "draft") if key not in metadata]
        if absent:
            missing_fields.append(f"{slug}:{','.join(absent)}")
        if not body.strip():
            empty_bodies.append(slug)
        for reference in IMAGE.findall(body):
            if "://" not in reference and not reference.startswith("/"):
                clean = reference.split("#", 1)[0].split("?", 1)[0]
                if not (page.parent / clean).is_file():
                    missing_assets.append(f"{slug}:{clean}")
        for target in INTERNAL_POST.findall(body):
            if target not in slugs:
                broken_post_links.append(f"{slug}:{target}")
    result = {
        "expected_count": expected_count,
        "article_count": len(pages),
        "missing_fields": sorted(missing_fields),
        "empty_bodies": sorted(empty_bodies),
        "missing_assets": sorted(missing_assets),
        "broken_post_links": sorted(broken_post_links),
    }
    result["valid"] = (
        result["article_count"] == expected_count
        and not result["missing_fields"]
        and not result["empty_bodies"]
        and not result["missing_assets"]
        and not result["broken_post_links"]
    )
    return result
```

- [ ] **Step 4: Add the `validate` CLI subcommand**

Add these imports and arguments to `tools/recover/__main__.py`:

```python
from tools.recover.validate import validate_recovery

validate = commands.add_parser("validate")
validate.add_argument("--site", type=Path, required=True)
validate.add_argument("--expected-count", type=int, required=True)
validate.add_argument("--report", type=Path, required=True)
```

Handle it before the recovery branch:

```python
if args.command == "validate":
    report = validate_recovery(args.site / "content/posts", args.expected_count)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if report["valid"] else 1
```

Change the final recovery code to be guarded by `if args.command == "recover":` so all three commands have exclusive paths.

- [ ] **Step 5: Run all unit tests**

Run: `.venv/bin/pytest -v`

Expected: all tests PASS.

- [ ] **Step 6: Run the complete recovery**

```bash
.venv/bin/python -m tools.recover recover \
  --backup backup/s3 \
  --site site \
  --report reports/recovery.json
.venv/bin/python -m tools.recover validate \
  --site site \
  --expected-count 218 \
  --report reports/validation.json
```

Expected: both commands exit 0; recovery reports 218 sources, 218 successes, and zero failures; validation reports `valid: true`.

- [ ] **Step 7: Inspect warning and text-loss outliers**

Run:

```bash
.venv/bin/python - <<'PY'
import json
rows = json.load(open('reports/recovery.json', encoding='utf-8'))['articles']
for row in rows:
    source = row['source_text_length']
    ratio = row['markdown_length'] / source if source else 0
    if row['status'] != 'ok' or ratio < 0.60 or ratio > 2.50:
        print(row['slug'], row['status'], f'{ratio:.2f}', row['missing_assets'], row['unsupported_elements'])
PY
```

Expected: every printed warning is manually reviewed against `backup/s3/posts/<slug>/index.html`. Fix converter rules and add a regression fixture before accepting a warning caused by content loss.

- [ ] **Step 8: Build Hugo with recovered content**

Run:

```bash
rm -rf site/public
.tools/bin/hugo --source site --minify --baseURL https://example.invalid/
.venv/bin/python - <<'PY'
from pathlib import Path
slugs = [path.parent.name for path in Path('site/content/posts').glob('*/index.md')]
missing = [slug for slug in slugs if not Path('site/public/posts', slug, 'index.html').is_file()]
assert len(slugs) == 218 and not missing, (len(slugs), missing)
PY
```

Expected: Hugo exits 0 and the article output count assertion succeeds.

- [ ] **Step 9: Commit recovered content and validation tooling**

```bash
git add tools/recover/validate.py tools/recover/__main__.py tests/test_validate.py \
  site/content/posts reports/recovery.json reports/validation.json
git commit -m "feat: recover and validate 218 blog articles"
```

### Task 9: Final Security and Recovery Audit

**Files:**
- Create: `docs/recovery-report.md`
- Modify: `.gitignore` if the audit finds generated local-only files

- [ ] **Step 1: Run the complete verification suite from a clean generated output directory**

```bash
.venv/bin/pytest -v
rm -rf site/public
.tools/bin/hugo --source site --minify --baseURL https://example.invalid/
.venv/bin/python -m tools.recover validate \
  --site site --expected-count 218 --report reports/validation.json
git diff --check
```

Expected: tests PASS, Hugo exits 0, validation exits 0, and `git diff --check` has no output.

- [ ] **Step 2: Scan tracked and staged files for credentials**

```bash
git ls-files -co --exclude-standard -z | \
  xargs -0 rg -n 'AKIA[0-9A-Z]{16}|AWS_SECRET_ACCESS_KEY\s*=\s*[^[:space:]]+' || true
git check-ignore -v .env
git ls-files .env
```

Expected: no credential match, `.env` is ignored, and `git ls-files .env` prints nothing.

- [ ] **Step 3: Manually review representative output**

Review these local pages using `.tools/bin/hugo server --source site --buildDrafts`:

- `adding-adsense-and-google-analytics-to-hugo` for Unicode images and code blocks
- `cv2-resize-interpolation-methods` for many images
- `densenet-paper-review` for image-heavy technical content
- `focal-loss-a-k-a-retinanet-paper-review` for GIF and equations
- one oldest post and one newest post from `reports/recovery.json`

Expected: titles, dates, paragraphs, code, tables, links, and images match the source content even though the theme differs.

- [ ] **Step 4: Record the final audit**

Run this after the manual review succeeds:

```bash
.venv/bin/python - <<'PY'
from datetime import date
import json
from pathlib import Path
import subprocess

manifest = json.loads(Path('manifests/s3-objects.json').read_text(encoding='utf-8'))
recovery = json.loads(Path('reports/recovery.json').read_text(encoding='utf-8'))
validation = json.loads(Path('reports/validation.json').read_text(encoding='utf-8'))
hugo = subprocess.run(['.tools/bin/hugo', 'version'], check=True, text=True, capture_output=True).stdout.strip()
samples = [
    'adding-adsense-and-google-analytics-to-hugo',
    'cv2-resize-interpolation-methods',
    'densenet-paper-review',
    'focal-loss-a-k-a-retinanet-paper-review',
]
report = f'''# Blog Recovery Report

- Executed: {date.today().isoformat()}
- Source: `s3://{manifest["bucket"]}`
- Source objects: {manifest["object_count"]}
- Source bytes: {manifest["total_size"]}
- Recovered articles: {recovery["success_count"]}
- Recovery failures: {recovery["failure_count"]}
- Recovery warnings: {recovery["warning_count"]}
- Validation passed: {validation["valid"]}
- Hugo: `{hugo}`
- PaperMod commit: `a2eb47bb4b805116dcd34c1605d39835121f8dbe`
- Unit tests: passed
- Manual samples: {", ".join(samples)} plus oldest and newest recovered posts
- AWS mutations: none; all AWS operations were read-only
'''
Path('docs/recovery-report.md').write_text(report, encoding='utf-8')
PY
```

Expected: `docs/recovery-report.md` records the measured values and `Validation passed: True`.

- [ ] **Step 5: Commit the audit report**

```bash
git add docs/recovery-report.md reports/validation.json .gitignore
git commit -m "docs: record Hugo recovery verification"
git status --short
```

Expected: final `git status --short` is empty. The repository is ready for a separate GitHub identity and Pages deployment plan.
