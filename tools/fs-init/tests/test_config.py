"""Tests for project name validation."""

import pytest

from fs_init.config import validate_project_name


@pytest.mark.parametrize("name", ["demo", "Demo_2", "demo-project", "123"])
def test_valid_project_names(name: str) -> None:
    validate_project_name(name)


@pytest.mark.parametrize(
    "name", ["", ".", "..", "../demo", "/tmp/demo", "a/b", "a\\b", "has space", "项目"]
)
def test_invalid_project_names(name: str) -> None:
    with pytest.raises(ValueError):
        validate_project_name(name)
