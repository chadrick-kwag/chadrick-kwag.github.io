"""Convert recovered article HTML into Markdown."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag
from markdownify import MarkdownConverter


SITE_HOST = "chadrick-kwag.net"
SUPPORTED = frozenset(
    {
        "a", "blockquote", "br", "code", "del", "div", "em", "figure",
        "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img",
        "li", "ol", "p", "pre", "section", "span", "strong", "table",
        "tbody", "td", "th", "thead", "tr", "ul",
    }
)
_STRIPPED_WRAPPERS = {"section", "span", "div"}
_LANGUAGE_CLASS = re.compile(r"^language-(.+)$")
_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")
_UNRESERVED_ASCII = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)


@dataclass(frozen=True)
class MarkdownResult:
    markdown: str
    local_assets: tuple[str, ...]
    unsupported_elements: tuple[str, ...]


class RecoveryConverter(MarkdownConverter):
    """Markdown converter that retains unfamiliar elements as raw HTML."""

    def process_tag(self, node: Tag, parent_tags: set[str] | None = None) -> str:
        if node.name != "[document]" and node.name not in SUPPORTED:
            return str(node)
        return super().process_tag(node, parent_tags=parent_tags)

    def convert_pre(self, el: Tag, text: str, parent_tags: set[str]) -> str:
        code = el.find("code", recursive=False)
        language = ""
        literal = el.get_text()
        if isinstance(code, Tag):
            literal = code.get_text()
            for class_name in code.get("class", []):
                match = _LANGUAGE_CLASS.match(class_name)
                if match:
                    language = match.group(1)
                    break
        longest_backtick_run = max(
            (len(run) for run in re.findall(r"`+", literal)), default=0
        )
        fence = "`" * max(3, longest_backtick_run + 1)
        terminal_newline = "" if literal.endswith("\n") else "\n"
        return (
            f"\n\n{fence}{language}\n{literal}{terminal_newline}{fence}\n\n"
        )


def _rewrite_url(value: str) -> str:
    """Safely decode a URL and make exact same-site URLs root-relative."""
    parsed = urlparse(value)
    path = _decode_path(parsed.path)
    query = _decode_percent(parsed.query)
    fragment = _decode_percent(parsed.fragment)
    if parsed.scheme in {"http", "https"} and parsed.hostname == SITE_HOST:
        result = path or "/"
        if parsed.params:
            result += f";{_decode_percent(parsed.params)}"
        if query:
            result += f"?{query}"
        if fragment:
            result += f"#{fragment}"
        return result
    return parsed._replace(path=path, query=query, fragment=fragment).geturl()


def _decode_path(path: str) -> str:
    decoded_segments = []
    for segment in path.split("/"):
        decoded = _decode_percent(segment)
        decoded_segments.append(segment if decoded in {".", ".."} else decoded)
    return "/".join(decoded_segments)


def _decode_percent(value: str) -> str:
    """Decode unreserved ASCII and valid percent-encoded non-ASCII UTF-8."""
    result: list[str] = []
    index = 0
    while index < len(value):
        if not _is_escape(value, index):
            result.append(value[index])
            index += 1
            continue

        first = int(value[index + 1:index + 3], 16)
        if first < 0x80:
            character = chr(first)
            result.append(
                character
                if character in _UNRESERVED_ASCII
                else value[index:index + 3]
            )
            index += 3
            continue

        byte_count = _utf8_byte_count(first)
        escapes = [value[index:index + 3]]
        encoded = bytearray([first])
        cursor = index + 3
        for _ in range(byte_count - 1):
            if not _is_escape(value, cursor):
                break
            escapes.append(value[cursor:cursor + 3])
            encoded.append(int(value[cursor + 1:cursor + 3], 16))
            cursor += 3
        try:
            decoded = bytes(encoded).decode("utf-8")
        except UnicodeDecodeError:
            decoded = ""
        if len(encoded) == byte_count and decoded and not decoded.isascii():
            result.append(decoded)
            index = cursor
        else:
            result.append(escapes[0])
            index += 3
    return "".join(result)


def _is_escape(value: str, index: int) -> bool:
    return (
        index + 2 < len(value)
        and value[index] == "%"
        and value[index + 1] in _HEX_DIGITS
        and value[index + 2] in _HEX_DIGITS
    )


def _utf8_byte_count(first: int) -> int:
    if 0xC2 <= first <= 0xDF:
        return 2
    if 0xE0 <= first <= 0xEF:
        return 3
    if 0xF0 <= first <= 0xF4:
        return 4
    return 1


def _local_asset_path(value: str) -> str | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith("/") or not parsed.path:
        return None

    filesystem_path = unquote(parsed.path)
    validation_path = filesystem_path
    while True:
        path = PurePosixPath(validation_path)
        segments = validation_path.split("/")
        if path.is_absolute() or any(
            segment in {"", ".", ".."} for segment in segments
        ):
            return None
        decoded_again = unquote(validation_path)
        if decoded_again == validation_path:
            return str(PurePosixPath(filesystem_path))
        validation_path = decoded_again


def convert_content(content: Tag) -> MarkdownResult:
    """Convert an article section without changing the parsed source tree."""
    if content.name != "section":
        raise ValueError("content must be a section element")

    clone_soup = BeautifulSoup(str(content), "html.parser")
    clone = clone_soup.find("section")
    if not isinstance(clone, Tag):  # pragma: no cover - guarded by input check
        raise ValueError("content must be a section element")

    unsupported = {
        tag.name for tag in clone.find_all(True) if tag.name not in SUPPORTED
    }
    local_assets: set[str] = set()
    for tag in clone.find_all(True):
        for attribute in ("href", "src"):
            value = tag.get(attribute)
            if not isinstance(value, str):
                continue
            rewritten = _rewrite_url(value)
            tag[attribute] = rewritten
            if attribute == "src" and tag.name == "img":
                local_asset = _local_asset_path(rewritten)
                if local_asset is not None:
                    local_assets.add(local_asset)

    converter = RecoveryConverter(
        heading_style="ATX",
        bullets="-",
        strip=_STRIPPED_WRAPPERS,
        escape_asterisks=False,
        escape_underscores=False,
    )
    markdown = converter.convert(str(clone)).strip() + "\n"
    return MarkdownResult(
        markdown=markdown,
        local_assets=tuple(sorted(local_assets)),
        unsupported_elements=tuple(sorted(unsupported)),
    )
