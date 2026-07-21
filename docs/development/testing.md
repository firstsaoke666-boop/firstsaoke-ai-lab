# Testing

Run all tests:

```bash
make test
```

Run a specific suite:

```bash
make test-unit
make test-integration
```

Unit tests belong in `tests/unit/`, integration tests in `tests/integration/`,
and sanitized shared test data in `tests/fixtures/`.
