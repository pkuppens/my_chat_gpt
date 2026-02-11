# GitHub Actions Workflow Documentation

This document describes the CI/CD workflow for the project.

## Overview

The workflow consists of three main jobs:

1. `setup`: Prepares the environment and installs dependencies
2. `lint`: Runs Ruff format and lint checks (independent, no venv)
3. `test`: Executes tests in parallel

## Caching Strategy

The workflow implements a two-level caching strategy:

### 1. UV Cache

- Caches UV's dependency resolution cache
- Location: `~/.cache/uv`
- Key: `uv-{date}-{requirements.txt-hash}`
- Purpose: Speeds up dependency resolution

### 2. Virtual Environment Cache

- Caches the Python virtual environment
- Location: `.venv`
- Key: `venv-{uv-cache-key}`
- Purpose: Prevents rebuilding venv for test job

**Note:** The `lint` job uses `uv tool run ruff` and does not need a venv or cache.

## Job Dependencies

```mermaid
graph TD
    A[setup] --> C[test]
    B[lint]
```

- `lint` runs independently (no venv or setup needed)
- `setup` must complete before `test` can start
- `lint` and `setup`/`test` can run in parallel

## Matrix Testing

The test job uses a matrix strategy to:

- Test against different Python versions
- Run tests in parallel
- Ensure consistent behavior across environments

## Reusable Actions

- **ruff**: Runs `ruff format --check` and `ruff check` via `uv tool run ruff`. No venv needed.
- **set-pythonpath**: Sets PYTHONPATH to include the workspace (for tests).

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [UV Documentation](https://github.com/astral-sh/uv)
- [actions/cache Documentation](https://github.com/actions/cache)
- [Matrix Strategy Documentation](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
