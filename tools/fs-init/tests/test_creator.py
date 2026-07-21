"""Tests for safe project creation and template merging."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fs_init.creator import FsInitError, create_project


@pytest.fixture
def template_root(tmp_path: Path) -> Path:
    root = tmp_path / "templates"
    for name in ("common", "python", "telegram-bot", "mcp-server", "nextjs"):
        (root / name).mkdir(parents=True)
    return root


def create(template_root: Path, output: Path, **kwargs: object) -> Path:
    return create_project(
        project_name=str(kwargs.pop("project_name", "demo-project")),
        template_name=str(kwargs.pop("template_name", "python")),
        output_dir=output,
        template_root=template_root,
        force=bool(kwargs.pop("force", False)),
    )


def test_default_python_template_content_is_used(template_root: Path, tmp_path: Path) -> None:
    (template_root / "python" / "python.txt").write_text("python", encoding="utf-8")
    project = create(template_root, tmp_path)
    assert (project / "python.txt").read_text(encoding="utf-8") == "python"


def test_unknown_template_is_rejected(template_root: Path, tmp_path: Path) -> None:
    with pytest.raises(FsInitError, match="unknown template"):
        create(template_root, tmp_path, template_name="missing")


def test_existing_target_is_rejected(template_root: Path, tmp_path: Path) -> None:
    (tmp_path / "demo-project").mkdir()
    with pytest.raises(FsInitError, match="already exists"):
        create(template_root, tmp_path)


def test_common_and_template_are_merged_with_template_precedence(
    template_root: Path, tmp_path: Path
) -> None:
    (template_root / "common" / "common.txt").write_text("common", encoding="utf-8")
    (template_root / "common" / "shared.txt").write_text("common", encoding="utf-8")
    (template_root / "python" / "specific.txt").write_text("specific", encoding="utf-8")
    (template_root / "python" / "shared.txt").write_text("python", encoding="utf-8")
    project = create(template_root, tmp_path)
    assert (project / "common.txt").is_file()
    assert (project / "specific.txt").is_file()
    assert (project / "shared.txt").read_text(encoding="utf-8") == "python"


def test_variables_are_replaced(template_root: Path, tmp_path: Path) -> None:
    (template_root / "common" / "README.md").write_text(
        "{{ project_name }}|{{ package_name }}|{{ template_name }}", encoding="utf-8"
    )
    project = create(template_root, tmp_path)
    assert (project / "README.md").read_text(encoding="utf-8") == (
        "demo-project|demo_project|python"
    )


def test_binary_file_is_copied_without_decoding(template_root: Path, tmp_path: Path) -> None:
    payload = b"\x00\xff{{ project_name }}"
    (template_root / "common" / "image.bin").write_bytes(payload)
    project = create(template_root, tmp_path)
    assert (project / "image.bin").read_bytes() == payload


@pytest.mark.parametrize("name", ["../escape", "/absolute", "nested/name", "nested\\name"])
def test_path_traversal_is_rejected(template_root: Path, tmp_path: Path, name: str) -> None:
    with pytest.raises(FsInitError):
        create(template_root, tmp_path, project_name=name)


def test_force_requires_and_validates_marker(template_root: Path, tmp_path: Path) -> None:
    target = tmp_path / "demo-project"
    target.mkdir()
    (target / "keep.txt").write_text("user data", encoding="utf-8")
    with pytest.raises(FsInitError, match="valid .fs-init.json"):
        create(template_root, tmp_path, force=True)
    assert (target / "keep.txt").read_text(encoding="utf-8") == "user data"

    (target / ".fs-init.json").write_text(
        json.dumps({"created_by": "fs-init", "project_name": "different"}), encoding="utf-8"
    )
    with pytest.raises(FsInitError, match="valid .fs-init.json"):
        create(template_root, tmp_path, force=True)


def test_force_replaces_an_fs_init_project(template_root: Path, tmp_path: Path) -> None:
    first = create(template_root, tmp_path)
    (first / "old.txt").write_text("old", encoding="utf-8")
    (template_root / "python" / "new.txt").write_text("new", encoding="utf-8")
    replaced = create(template_root, tmp_path, force=True)
    assert not (replaced / "old.txt").exists()
    assert (replaced / "new.txt").is_file()


def test_ignored_template_artifacts_are_not_copied(template_root: Path, tmp_path: Path) -> None:
    (template_root / "common" / ".git").mkdir()
    (template_root / "common" / ".git" / "config").write_text("x", encoding="utf-8")
    (template_root / "python" / "cache.pyc").write_bytes(b"x")
    project = create(template_root, tmp_path)
    assert not (project / ".git").exists()
    assert not (project / "cache.pyc").exists()
