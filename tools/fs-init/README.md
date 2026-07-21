# fs-init

`fs-init` creates a project by layering `project-template/common` first and one selected template second. The selected template wins when both layers contain the same file.

## Requirements

- Python 3.12 or newer (tested with Python 3.14)
- `uv` for development and optional Python dependency synchronization
- `git` for default repository initialization

Runtime code uses only the Python standard library.

## Development setup

Run these commands in a WSL Terminal:

```bash
cd /home/m_666/workspaces/firstsaoke-ai-lab/tools/fs-init
uv sync
uv run pytest
```

## Usage

```bash
uv run fs-init PROJECT_NAME
uv run fs-init PROJECT_NAME --template python
uv run fs-init PROJECT_NAME --template telegram-bot
uv run fs-init PROJECT_NAME --template mcp-server
uv run fs-init PROJECT_NAME --template nextjs
```

Options:

- `--template`, `-t`: template name; defaults to `python`
- `--output-dir`, `-o`: existing parent directory; defaults to the current directory
- `--force`: replace only a directory with a matching valid `.fs-init.json` marker
- `--no-git`: skip `git init`
- `--no-sync`: skip `uv sync`
- `--version`: print the installed version

Project names may contain only English letters, numbers, hyphens, and underscores. Absolute paths, separators, `.` and `..` are rejected.

## Creation behavior

Files are assembled in a temporary sibling directory, placeholders are replaced in known text files, and the result is renamed into place. Generated projects contain `.fs-init.json`. On `--force`, the old project is moved aside immediately before the new project is installed; it is restored if installation fails.

The supported placeholders are `{{ project_name }}`, `{{ package_name }}`, and `{{ template_name }}`. Hyphens become underscores in `package_name`. Binary files are copied unchanged.

After creation, `git init` runs by default. `uv sync` runs for `python`, `telegram-bot`, and `mcp-server` only when the generated project has `pyproject.toml`. Next.js dependencies are never installed automatically. A failed external command prints a warning and keeps the created project.

The source checkout locates templates at the workspace-level `project-template` directory. Set `FS_INIT_TEMPLATE_ROOT` to an alternative absolute or relative template root when running the package outside this workspace layout.
