from pathlib import Path

import pytest

from tools.recover import io as recovery_io


def test_atomic_json_preserves_target_on_serialization_failure(
    tmp_path: Path,
) -> None:
    target = tmp_path / "report.json"
    original = b"existing report\n"
    target.write_bytes(original)

    with pytest.raises(TypeError):
        recovery_io.write_json_atomic(target, {"invalid": object()})

    assert target.read_bytes() == original
    assert list(tmp_path.glob("*.tmp")) == []


def test_atomic_json_preserves_target_on_fsync_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.json"
    original = b"existing report\n"
    target.write_bytes(original)
    monkeypatch.setattr(
        recovery_io.os, "fsync", lambda *_: (_ for _ in ()).throw(
            OSError("fsync failed")
        )
    )

    with pytest.raises(OSError, match="fsync failed"):
        recovery_io.write_json_atomic(target, {"valid": "한글"})

    assert target.read_bytes() == original
    assert list(tmp_path.glob("*.tmp")) == []


def test_atomic_json_fsyncs_parent_directory_after_replace_and_closes_fd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.json"
    directory_fd = 987654
    fsync_calls: list[int] = []
    close_calls: list[int] = []
    real_fsync = recovery_io.os.fsync
    real_open = recovery_io.os.open

    def track_fsync(fd: int) -> None:
        fsync_calls.append(fd)
        if fd != directory_fd:
            real_fsync(fd)

    def open_directory(path, flags: int, *args) -> int:
        if args:
            return real_open(path, flags, *args)
        assert Path(path) == tmp_path
        assert flags & recovery_io.os.O_RDONLY == recovery_io.os.O_RDONLY
        if hasattr(recovery_io.os, "O_DIRECTORY"):
            assert flags & recovery_io.os.O_DIRECTORY
        return directory_fd

    monkeypatch.setattr(recovery_io.os, "fsync", track_fsync)
    monkeypatch.setattr(recovery_io.os, "open", open_directory)
    monkeypatch.setattr(
        recovery_io.os, "close", lambda fd: close_calls.append(fd)
    )

    recovery_io.write_json_atomic(target, {"valid": True})

    assert len(fsync_calls) == 2
    assert fsync_calls[0] != directory_fd
    assert fsync_calls[1] == directory_fd
    assert close_calls == [directory_fd]


def test_atomic_json_propagates_directory_fsync_failure_after_replace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "report.json"
    target.write_text("old\n", encoding="utf-8")
    directory_fd = 987654
    real_fsync = recovery_io.os.fsync
    real_open = recovery_io.os.open
    closed: list[int] = []

    def fail_directory_fsync(fd: int) -> None:
        if fd == directory_fd:
            raise OSError("directory fsync failed after replacement")
        real_fsync(fd)

    monkeypatch.setattr(
        recovery_io.os,
        "open",
        lambda path, flags, *args: (
            real_open(path, flags, *args) if args else directory_fd
        ),
    )
    monkeypatch.setattr(recovery_io.os, "fsync", fail_directory_fsync)
    monkeypatch.setattr(recovery_io.os, "close", lambda fd: closed.append(fd))

    with pytest.raises(OSError, match="directory fsync failed after replacement"):
        recovery_io.write_json_atomic(target, {"new": True})

    assert target.read_text(encoding="utf-8").endswith('"new": true\n}\n')
    assert closed == [directory_fd]
