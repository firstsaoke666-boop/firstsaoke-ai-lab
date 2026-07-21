# ADR 0003: Use Ruff and pytest

## Status

Accepted

## Context

The monorepo needs fast, consistent formatting, linting, and testing with a
small development dependency set.

## Decision

Use Ruff for formatting, import sorting, and linting. Use pytest for unit,
integration, and repository-level tests. Run format checks, lint checks, and
the complete test suite in GitHub Actions and through `make check` locally.

## Consequences

Contributors have one formatter and linter with centralized configuration, and
tests use a widely supported framework. Code must satisfy automated checks
before merging, and rule changes affect the entire repository.
