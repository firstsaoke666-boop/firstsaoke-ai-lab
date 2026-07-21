# ADR 0004: Standardize developer experience tooling

## Status

Accepted

## Context

The monorepo needs a discoverable local workflow and consistent contribution
quality without relying on machine-specific configuration.

## Decision

Standardize routine commands behind the Makefile. Use pre-commit for fast local
quality enforcement and commit shared VS Code settings, tasks, debugging, and
extension recommendations. Use GitHub pull request and issue templates to
capture scope, evidence, and security considerations. Use Dependabot for weekly
Python tooling and GitHub Actions maintenance.

## Consequences

Local and CI commands remain aligned, contributors receive consistent editor
defaults, and repository changes arrive with more complete context. Developers
must synchronize the environment and install the Git hook once. Shared tooling
updates generate automated pull requests that still require normal review and
CI validation.
