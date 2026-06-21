"""Durable JSON output shared by recovery commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from typing import Any, TextIO


def write_json_atomic(path: str | Path, value: Any) -> None:
    """Atomically replace *path* with durable UTF-8 JSON.

    A directory-fsync failure is propagated after the target has been replaced;
    callers must therefore treat that error as uncertain durability, not as an
    indication that the old target remains installed.
    """
    path = Path(path)
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f"{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary = Path(file.name)
            _write_and_sync(file, content)
        os.replace(temporary, path)
        temporary = None
        _fsync_directory(path.parent)
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def _write_and_sync(file: TextIO, content: str) -> None:
    file.write(content)
    file.flush()
    os.fsync(file.fileno())


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
