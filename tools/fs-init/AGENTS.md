# fs-init Contributor Guide

- Keep implementation in `src/fs_init`; keep CLI parsing separate from file and process operations.
- Use only the Python standard library at runtime and use `pathlib` for paths.
- Preserve atomic creation, marker validation, and path-traversal protections.
- Never follow or copy ignored template directories (`.git`, `.venv`, `__pycache__`, `node_modules`).
- Add or update focused pytest coverage for every behavior change.
- Run `uv run pytest` and `uv run fs-init --help` before handing off changes.
- Do not modify directories under `project-template` as part of CLI maintenance unless explicitly requested.
