# Contributing

Thank you for improving `firstsaoke-ai-lab`. Keep changes focused, tested, and
free of unrelated refactoring.

## Environment requirements

- WSL or another Linux environment
- Python 3.12, as declared in `.python-version`
- `uv`
- Git

## Setup

Run from the repository root in a **WSL Terminal**:

```bash
uv sync
uv run pytest
```

Install the repository's pre-commit hook after synchronization:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Development workflow

1. Create a focused branch from the current default branch.
2. Synchronize dependencies with `make sync`.
3. Make the smallest change that satisfies the requirement.
4. Add or update tests at the appropriate test level.
5. Run `make check` before submitting a pull request.
6. Update documentation when behavior, configuration, or architecture changes.

Do not add business logic to shared infrastructure files. Keep dependencies
minimal and declare package-specific dependencies in the relevant workspace
member.

## Testing

```bash
make test
make test-unit
make test-integration
```

- Unit tests belong in `tests/unit/`.
- Integration tests belong in `tests/integration/`.
- Shared test data belongs in `tests/fixtures/`.

## Linting and formatting

```bash
make format
make lint
make check
make pre-commit-run
```

`make format` modifies files. `make lint` and `make check` are suitable for
verification before a commit.

## Commit convention

Use Conventional Commit-style messages:

```text
<type>(optional-scope): concise imperative summary
```

Common types are `feat`, `fix`, `docs`, `test`, `refactor`, `build`, and
`chore`. Keep each commit limited to one logical change.

## Pull request checklist

- [ ] The change is focused and contains no unrelated cleanup.
- [ ] Tests cover the change at the appropriate level.
- [ ] `make check` passes locally.
- [ ] Documentation is updated where needed.
- [ ] No credentials, `.env` files, generated caches, or build artifacts are included.
- [ ] New dependencies are necessary and documented.
- [ ] Breaking or architectural decisions include an ADR.
