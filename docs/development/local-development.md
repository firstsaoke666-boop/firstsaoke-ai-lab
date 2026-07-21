# Local development

Use Python 3.12 and `uv` from a WSL Terminal at the repository root.

```bash
uv sync
uv run pre-commit install
make check
```

`uv sync` creates or updates `.venv` from `uv.lock`. Use `make help` to list
the supported workflow commands. Do not commit `.env` or local cache files.
