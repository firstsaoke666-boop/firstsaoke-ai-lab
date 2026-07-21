"""Command-line interface for fs-init."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from fs_init import __version__
from fs_init.config import SUPPORTED_TEMPLATES
from fs_init.creator import FsInitError, create_project, default_template_root
from fs_init.external import run_post_create


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="fs-init",
        description="Create a project from a Firstsaoke template.",
    )
    parser.add_argument("project_name", nargs="?", help="Project directory name.")
    parser.add_argument(
        "-t",
        "--template",
        default="python",
        help=f"Template to use (default: python; choices: {', '.join(SUPPORTED_TEMPLATES)}).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Parent directory for the project (default: current directory).",
    )
    parser.add_argument("--force", action="store_true", help="Replace a project previously created by fs-init.")
    parser.add_argument("--no-git", action="store_true", help="Do not run git init.")
    parser.add_argument("--no-sync", action="store_true", help="Do not run uv sync.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run fs-init and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.project_name is None:
        parser.error("PROJECT_NAME is required")

    try:
        project_path = create_project(
            project_name=args.project_name,
            template_name=args.template,
            output_dir=args.output_dir,
            template_root=default_template_root(),
            force=args.force,
        )
    except FsInitError as exc:
        parser.exit(2, f"fs-init: error: {exc}\n")

    post_create = run_post_create(
        project_path,
        args.template,
        initialize_git=not args.no_git,
        sync_dependencies=not args.no_sync,
    )
    print(f"Project: {project_path}")
    print(f"Template: {args.template}")
    print(f"Git initialized: {post_create.git_status}")
    print(f"Dependencies synchronized: {post_create.sync_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
