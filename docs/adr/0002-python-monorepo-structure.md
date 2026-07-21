# ADR 0002: Adopt a Python monorepo structure

## Status

Accepted

## Context

Applications, services, shared Python capabilities, documentation, tests, and
AI-assisted development artifacts need clear ownership boundaries without
splitting related work across repositories.

## Decision

Use `apps/` for deployable applications, `services/` for long-running
components, and `packages/` for independently importable shared libraries.
Each Python package uses a `src` layout and a unique `firstsaoke_*` import name.
Keep repository-wide tests in `tests/`, separated into unit and integration
suites.

## Consequences

Related changes can be reviewed atomically and shared tooling remains
consistent. Boundaries must be maintained deliberately, and package
dependencies must remain explicit to prevent accidental coupling.
