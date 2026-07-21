"""CLI behavior tests."""

from pathlib import Path
from unittest.mock import patch

from fs_init.cli import main
from fs_init.external import PostCreateResult


@patch("fs_init.cli.run_post_create")
@patch("fs_init.cli.default_template_root")
def test_cli_defaults_to_python(
    template_root: object, post_create: object, tmp_path: Path, monkeypatch: object
) -> None:
    root = tmp_path / "templates"
    (root / "common").mkdir(parents=True)
    (root / "python").mkdir()
    template_root.return_value = root  # type: ignore[attr-defined]
    post_create.return_value = PostCreateResult("skipped", "skipped")  # type: ignore[attr-defined]
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]
    assert main(["demo", "--no-git", "--no-sync"]) == 0
    assert (tmp_path / "demo" / ".fs-init.json").is_file()
    assert post_create.call_args.args[1] == "python"  # type: ignore[attr-defined]
