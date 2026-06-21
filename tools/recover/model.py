"""Data models for recovered Hugo articles."""

from __future__ import annotations

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
