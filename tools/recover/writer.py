"""Write recovered articles as Hugo page bundles."""

from __future__ import annotations

import ctypes
import errno
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
from tempfile import mkdtemp

import yaml

from tools.recover.markdown import MarkdownResult
from tools.recover.model import Article


_SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class AtomicExchangeError(OSError):
    """Raised when a live bundle could not be atomically exchanged."""


def write_bundle(
    article: Article, converted: MarkdownResult, posts_root: Path
) -> tuple[str, ...]:
    """Stage and atomically install one recovered Hugo page bundle."""
    posts_root.mkdir(parents=True, exist_ok=True)
    slug = _safe_slug(article.slug)
    root = posts_root.resolve()
    destination = posts_root / slug
    copied: list[str] = []
    _recover_previous(destination)

    staged = Path(mkdtemp(dir=posts_root, prefix=f".staged-{slug}-"))
    installed = False
    try:
        front_matter = yaml.safe_dump(
            {
                "title": article.title,
                "date": article.date,
                "lastmod": article.lastmod,
                "slug": article.slug,
                "categories": list(article.categories),
                "tags": list(article.tags),
                "draft": False,
            },
            allow_unicode=True,
            sort_keys=False,
        )
        (staged / "index.md").write_text(
            f"---\n{front_matter}---\n{converted.markdown}", encoding="utf-8"
        )

        source_root = article.source_path.parent.resolve()
        for asset in sorted(converted.local_assets):
            relative = _safe_asset_path(asset)
            source = article.source_path.parent / relative
            if not source.exists():
                continue
            resolved_source = source.resolve()
            if (
                not resolved_source.is_relative_to(source_root)
                or not source.is_file()
            ):
                raise ValueError(f"unsafe asset path: {asset}")
            target = staged.joinpath(*relative.parts)
            resolved_parent = target.parent.resolve()
            if not resolved_parent.is_relative_to(staged.resolve()):
                raise ValueError(f"unsafe asset path: {asset}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(asset)

        if destination.parent.resolve() != root:
            raise ValueError(f"unsafe slug: {article.slug}")
        if destination.exists() or destination.is_symlink():
            try:
                _atomic_exchange(staged, destination)
            except Exception as error:
                raise AtomicExchangeError(str(error)) from error
            installed = True
            try:
                _remove_staged(staged)
            except Exception:
                pass
        else:
            os.replace(staged, destination)
            installed = True
    except BaseException:
        if not installed:
            try:
                _remove_staged(staged)
            except Exception:
                pass
        raise

    return tuple(copied)


def _safe_slug(slug: str) -> str:
    if _SLUG.fullmatch(slug) is None:
        raise ValueError(f"unsafe slug: {slug}")
    return slug


def _safe_asset_path(asset: str) -> PurePosixPath:
    path = PurePosixPath(asset)
    if (
        not asset
        or "\\" in asset
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"unsafe asset path: {asset}")
    return path


def _atomic_exchange(staged: Path, destination: Path) -> None:
    """Atomically exchange two directories without a visibility gap."""
    if sys.platform == "darwin":
        _libc_exchange("renameatx_np", -2, staged, destination)
    elif sys.platform.startswith("linux"):
        _libc_exchange("renameat2", -100, staged, destination)
    else:
        raise OSError(errno.ENOTSUP, "atomic directory exchange unavailable")


def _libc_exchange(
    function_name: str, at_fdcwd: int, staged: Path, destination: Path
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        exchange = getattr(libc, function_name)
    except AttributeError as error:
        raise OSError(
            errno.ENOTSUP, "atomic directory exchange unavailable"
        ) from error
    exchange.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    exchange.restype = ctypes.c_int
    result = exchange(
        at_fdcwd,
        os.fsencode(staged),
        at_fdcwd,
        os.fsencode(destination),
        2,
    )
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number))


def _recover_previous(destination: Path) -> None:
    prefix = f".previous-{destination.name}-"
    previous_paths = sorted(
        entry
        for entry in destination.parent.iterdir()
        if entry.name.startswith(prefix)
    )
    if (
        not destination.exists()
        and not destination.is_symlink()
        and previous_paths
    ):
        os.replace(previous_paths.pop(0), destination)
    for previous in previous_paths:
        try:
            _remove_staged(previous)
        except Exception:
            pass


def _remove_staged(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)
