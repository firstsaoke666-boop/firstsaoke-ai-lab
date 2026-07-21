# ADR 0001: Use a uv workspace

## Status

Accepted

## Context

The repository contains multiple Python packages that need consistent Python
and dependency resolution while remaining independently installable.

## Decision

Use a single `uv` workspace rooted at `pyproject.toml`. Commit `uv.lock`, manage
development dependencies at the root, and declare package dependencies in each
workspace member.

## Consequences

Developers and CI use one fast, reproducible workflow. Workspace packages can
depend on one another explicitly. Contributors must use `uv` and keep the lock
file synchronized when dependency declarations change.
