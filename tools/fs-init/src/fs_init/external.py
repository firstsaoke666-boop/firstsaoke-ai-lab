"""Post-creation external command handling."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PYTHON_TEMPLATES = {"python", "telegram-bot", "mcp-server"}


@dataclass(frozen=True)
class PostCreateResult:
    """Human-readable outcomes for optional post-creation steps."""

    git_status: str
    sync_status: str


def _run(command: list[str], project_path: Path) -> bool:
    """Run one command without a shell and preserve its stderr output."""
    try:
        completed = subprocess.run(command, cwd=project_path, check=False)
    except OSError as exc:
        print(f"Warning: could not run {' '.join(command)}: {exc}", file=sys.stderr)
        return False
    if completed.returncode != 0:
        print(
            f"Warning: {' '.join(command)} failed with exit code {completed.returncode}; project was kept.",
            file=sys.stderr,
        )
        return False
    return True


def run_post_create(
    project_path: Path,
    template_name: str,
    *,
    initialize_git: bool,
    sync_dependencies: bool,
) -> PostCreateResult:
    """Initialize Git and synchronize Python dependencies when applicable."""
    git_status = "skipped (--no-git)"
    if initialize_git:
        git_status = "yes" if _run(["git", "init"], project_path) else "failed (see warning)"

    should_sync = template_name in PYTHON_TEMPLATES and (project_path / "pyproject.toml").is_file()
    if not sync_dependencies:
        sync_status = "skipped (--no-sync)"
    elif not should_sync:
        sync_status = "not applicable"
    else:
        sync_status = "yes" if _run(["uv", "sync"], project_path) else "failed (see warning)"
    return PostCreateResult(git_status=git_status, sync_status=sync_status)
