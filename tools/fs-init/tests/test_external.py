"""Tests for optional external commands."""

from pathlib import Path
from unittest.mock import Mock, patch

from fs_init.external import run_post_create


@patch("fs_init.external.subprocess.run")
def test_external_commands_can_be_mocked(run: Mock, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").touch()
    run.return_value.returncode = 0
    result = run_post_create(
        tmp_path, "python", initialize_git=True, sync_dependencies=True
    )
    assert [call.args[0] for call in run.call_args_list] == [["git", "init"], ["uv", "sync"]]
    assert all(call.kwargs["check"] is False for call in run.call_args_list)
    assert result.git_status == "yes"
    assert result.sync_status == "yes"


@patch("fs_init.external.subprocess.run")
def test_nextjs_never_installs_dependencies(run: Mock, tmp_path: Path) -> None:
    run.return_value.returncode = 0
    result = run_post_create(
        tmp_path, "nextjs", initialize_git=False, sync_dependencies=True
    )
    run.assert_not_called()
    assert result.sync_status == "not applicable"


@patch("fs_init.external.subprocess.run")
def test_external_failure_keeps_result_and_warns(
    run: Mock, tmp_path: Path, capsys: object
) -> None:
    run.return_value.returncode = 7
    result = run_post_create(
        tmp_path, "python", initialize_git=True, sync_dependencies=False
    )
    assert result.git_status == "failed (see warning)"
    assert "project was kept" in capsys.readouterr().err  # type: ignore[attr-defined]
