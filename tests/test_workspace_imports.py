"""Smoke tests for workspace package installation."""

import firstsaoke_ai
import firstsaoke_config
import firstsaoke_core
import firstsaoke_utils


def test_workspace_packages_are_importable() -> None:
    """All shared packages can be imported independently."""
    assert all(
        package.__name__.startswith("firstsaoke_")
        for package in (
            firstsaoke_ai,
            firstsaoke_config,
            firstsaoke_core,
            firstsaoke_utils,
        )
    )
