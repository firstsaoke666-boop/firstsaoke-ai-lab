"""Integration checks for installed workspace members."""

import importlib.util


def test_all_workspace_packages_are_installed() -> None:
    """The synchronized environment contains every shared package."""
    module_names = (
        "firstsaoke_ai",
        "firstsaoke_config",
        "firstsaoke_core",
        "firstsaoke_utils",
    )

    assert all(importlib.util.find_spec(name) is not None for name in module_names)
