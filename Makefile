.DEFAULT_GOAL := help

.PHONY: help sync format lint test test-unit test-integration pre-commit-install pre-commit-run check clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "; printf "Available targets:\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Install and synchronize workspace dependencies
	uv sync

format: ## Format code and apply safe lint fixes
	uv run ruff format .
	uv run ruff check . --fix

lint: ## Check formatting and lint the repository
	uv run ruff format --check .
	uv run ruff check .

test: ## Run all tests
	uv run pytest

test-unit: ## Run unit tests
	uv run pytest tests/unit

test-integration: ## Run integration tests
	uv run pytest tests/integration

pre-commit-install: ## Install the Git pre-commit hook
	uv run pre-commit install

pre-commit-run: ## Run pre-commit hooks against all files
	uv run pre-commit run --all-files

check: lint test ## Run all required local quality checks

clean: ## Remove generated caches and build artifacts (keeps .venv and uv.lock)
	find apps packages services scripts tests -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov build dist
	rm -f .coverage .coverage.*
	find packages -type d -name '*.egg-info' -prune -exec rm -rf {} +
