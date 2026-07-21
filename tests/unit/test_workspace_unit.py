"""Unit-level checks for the workspace foundation."""

import firstsaoke_core


def test_core_package_is_importable() -> None:
    """The core workspace package is available to unit tests."""
    assert firstsaoke_core.__name__ == "firstsaoke_core"
