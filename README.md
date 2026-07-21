# firstsaoke-ai-lab

A production-oriented Python monorepo for shared libraries, applications, and
services. The repository uses a single
[`uv` workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) for
fast, reproducible dependency management.

## Requirements

- Python 3.12
- `uv`

## Getting started

Run these commands in a **WSL Terminal** from the repository root:

```bash
uv sync
uv run ruff check .
uv run pytest
```

`uv sync` creates the local `.venv`, installs the four workspace packages, and
installs the development tools declared in `pyproject.toml`.

## Repository layout

```text
.ai/                 AI context, prompts, specifications, and task notes
.github/workflows/   Continuous integration workflows
apps/                Deployable applications
docs/                Project documentation
packages/            Independently importable shared Python packages
services/            Long-running services and APIs
scripts/             Repository automation scripts
tests/               Repository-level tests
```

The shared packages use a `src` layout:

| Workspace member | Python import |
| --- | --- |
| `packages/core` | `firstsaoke_core` |
| `packages/config` | `firstsaoke_config` |
| `packages/ai` | `firstsaoke_ai` |
| `packages/utils` | `firstsaoke_utils` |

## Development

Add reusable code to the appropriate package and product-specific code to an
application or service. Keep package dependencies explicit in each member's
`pyproject.toml`.

Developer guides:

- [Local development](docs/development/local-development.md)
- [Testing](docs/development/testing.md)
- [Code quality](docs/development/code-quality.md)
- [VS Code](docs/development/vscode.md)

Before opening a pull request, run:

```bash
make check
make pre-commit-run
```

GitHub Actions performs the same checks on every push and pull request.
