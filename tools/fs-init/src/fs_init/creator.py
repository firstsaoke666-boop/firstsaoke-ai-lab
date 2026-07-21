"""Safe template merging and atomic project creation."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

from fs_init import __version__
from fs_init.config import SUPPORTED_TEMPLATES, validate_project_name

MARKER_FILE = ".fs-init.json"
IGNORED_DIRECTORIES = {".git", ".venv", "__pycache__", "node_modules"}
IGNORED_FILES = {".DS_Store"}
TEXT_SUFFIXES = {
    ".cfg", ".css", ".env", ".gitignore", ".html", ".ini", ".js", ".json",
    ".jsx", ".md", ".mjs", ".py", ".rst", ".sh", ".toml", ".ts", ".tsx",
    ".txt", ".yaml", ".yml",
}


class FsInitError(Exception):
    """Raised for user-facing project creation errors."""


def default_template_root() -> Path:
    """Return the workspace template directory for this installation."""
    override = os.environ.get("FS_INIT_TEMPLATE_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[4] / "project-template"


def _is_ignored(path: Path) -> bool:
    return (
        any(part in IGNORED_DIRECTORIES for part in path.parts)
        or path.name in IGNORED_FILES
        or path.suffix == ".pyc"
    )


def _copy_template(source: Path, destination: Path) -> None:
    """Copy one template layer, allowing later layers to overwrite files."""
    for source_path in source.rglob("*"):
        relative_path = source_path.relative_to(source)
        if _is_ignored(relative_path) or source_path.is_symlink():
            continue
        destination_path = destination / relative_path
        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
        elif source_path.is_file():
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)


def _replace_variables(project_root: Path, variables: dict[str, str]) -> None:
    """Replace placeholders only in files with known text suffixes or names."""
    for path in project_root.rglob("*"):
        if not path.is_file() or path.name == MARKER_FILE:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Dockerfile", "Makefile"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for variable, value in variables.items():
            content = content.replace("{{ " + variable + " }}", value)
        path.write_text(content, encoding="utf-8")


def _write_marker(project_root: Path, project_name: str, template_name: str) -> None:
    marker = {
        "created_by": "fs-init",
        "fs_init_version": __version__,
        "project_name": project_name,
        "template": template_name,
    }
    (project_root / MARKER_FILE).write_text(
        json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _has_valid_marker(target: Path) -> bool:
    try:
        marker = json.loads((target / MARKER_FILE).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    return marker.get("created_by") == "fs-init" and marker.get("project_name") == target.name


def _assert_safe_force_target(target: Path, output_dir: Path) -> None:
    resolved_target = target.resolve()
    workspace_root = default_template_root().resolve().parent
    protected = {
        Path(resolved_target.anchor),
        Path.home().resolve(),
        output_dir.resolve(),
        workspace_root,
    }
    if resolved_target in protected:
        raise FsInitError(f"refusing to replace protected directory: {resolved_target}")
    if not target.is_dir() or target.is_symlink() or not _has_valid_marker(target):
        raise FsInitError("--force requires an existing directory with a valid .fs-init.json marker")


def create_project(
    project_name: str,
    template_name: str,
    output_dir: Path,
    template_root: Path,
    *,
    force: bool = False,
) -> Path:
    """Create a merged project via a sibling temporary directory."""
    try:
        validate_project_name(project_name)
    except ValueError as exc:
        raise FsInitError(str(exc)) from exc
    if template_name not in SUPPORTED_TEMPLATES:
        raise FsInitError(f"unknown template '{template_name}'")

    output_dir = output_dir.expanduser().resolve()
    template_root = template_root.resolve()
    common_source = template_root / "common"
    selected_source = template_root / template_name
    if not output_dir.is_dir():
        raise FsInitError(f"output directory does not exist: {output_dir}")
    if not common_source.is_dir() or not selected_source.is_dir():
        raise FsInitError(f"template directory is missing under: {template_root}")

    target = output_dir / project_name
    if target.exists():
        if not force:
            raise FsInitError(f"target already exists: {target}")
        _assert_safe_force_target(target, output_dir)

    temporary = Path(tempfile.mkdtemp(prefix=f".{project_name}.fs-init-", dir=output_dir))
    backup: Path | None = None
    try:
        _copy_template(common_source, temporary)
        _copy_template(selected_source, temporary)
        _replace_variables(
            temporary,
            {
                "project_name": project_name,
                "package_name": project_name.replace("-", "_"),
                "template_name": template_name,
            },
        )
        _write_marker(temporary, project_name, template_name)
        if target.exists():
            backup = Path(tempfile.mkdtemp(prefix=f".{project_name}.fs-init-backup-", dir=output_dir))
            backup.rmdir()
            target.replace(backup)
        temporary.replace(target)
        if backup is not None:
            shutil.rmtree(backup)
        return target.resolve()
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        if backup is not None and backup.exists():
            if target.exists():
                shutil.rmtree(target)
            backup.replace(target)
        raise
