"""Shared configuration and validation rules."""

from __future__ import annotations

import re

SUPPORTED_TEMPLATES = ("python", "telegram-bot", "mcp-server", "nextjs")
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_project_name(project_name: str) -> None:
    """Reject names that could escape or ambiguously address a project path."""
    if not project_name or not PROJECT_NAME_PATTERN.fullmatch(project_name):
        raise ValueError(
            "project name may contain only English letters, numbers, hyphens, and underscores"
        )
    if project_name in {".", ".."}:
        raise ValueError("project name cannot be '.' or '..'")
