# Code quality

Format Python files and apply safe Ruff fixes:

```bash
make format
```

Run non-modifying quality checks and the full test suite:

```bash
make lint
make check
make pre-commit-run
```

Run `make check` and `make pre-commit-run` before opening a pull request.
