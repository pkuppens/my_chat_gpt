# Linting Configuration and Tools

This document provides an overview of the linting configuration and tools used in this project.

## Linting Tool

We use **Ruff** as our primary linting and formatting tool. Ruff is a fast Python linter and formatter written in Rust.

## Linting Configuration

The configuration for `ruff` is specified in the `pyproject.toml` file under the `[tool.ruff]` section. The settings are as follows:

- `line-length`: Set to 132 to allow longer lines
- `target-version`: Set to "py312" for Python 3.12 compatibility
- `select`: Includes common rules for code quality
- `ignore`: Specifies rules to ignore

## Pre-commit Hook

A pre-commit hook has been added to prevent deteriorating the lint score. The pre-commit script is located at `.github/scripts/pre_commit_lint.sh`.

### Configuring the Pre-commit Hook

To configure the pre-commit hook, follow these steps:

1. Ensure you have `pre-commit` installed. You can install it using `uv`:

   ```sh
   uv pip install pre-commit
   ```

2. Create a `.pre-commit-config.yaml` file in the root directory with the following content:

   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.3.0
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
   ```

3. Install the pre-commit hook:

   ```sh
   pre-commit install
   ```

### Bypassing the Pre-commit Hook

To bypass the lint check, use the `--no-verify` option when committing:

```sh
git commit -m "Your commit message" --no-verify
```

**Recommendation**: It is recommended to avoid using the bypass option to ensure code quality.

## Standalone Lint Run

To run the linting tools manually, use the following commands:

```sh
ruff check .
ruff format .
```

## Recommended Plugin Extensions

For a better development experience, it is recommended to use the following plugin extensions:

- **Python**: Provides rich support for the Python language
- **Pylance**: A performant language server for Python in Visual Studio Code
- **Ruff**: Official VS Code extension for Ruff
