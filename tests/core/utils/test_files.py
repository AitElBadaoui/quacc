import os
from pathlib import Path

from quacc.utils.files import copy_decompress_files_from_dir, make_unique_dir


def test_make_unique_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    jobdir = make_unique_dir()
    assert os.path.exists(jobdir)

    jobdir = make_unique_dir(base_path="tmp_dir")
    assert os.path.exists("tmp_dir")
    assert "tmp_dir" in str(jobdir)
    assert os.path.exists(jobdir)


def test_copy_decompress_files_from_dir(tmp_path):
    src = tmp_path / "src"
    src.mkdir()

    dst = tmp_path / "dst"
    dst.mkdir()

    Path(src / "file1").touch()
    Path(src / "dir1").mkdir()
    Path(f"{str(src)}{'/nested' * 10}").mkdir(parents=True)
    Path(src / "dir1" / "file2").touch()
    Path(src / "dir1" / "symlink1").symlink_to(src)

    copy_decompress_files_from_dir(src, dst)

    assert (dst / "file1").exists()
    assert (dst / "dir1").exists()
    assert (dst / "dir1" / "file2").exists()
    assert Path(f"{str(dst)}{'/nested' * 10}").exists()
    assert not (dst / "dir1" / "symlink1").exists()