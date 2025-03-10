# Linting Configuration and Tools

This document provides an overview of the linting configuration and tools used in this project.

## Linting Tools

We use the following linting tools in this project:

- **Black**: A code formatter for Python.
- **Flake8**: A linting tool for Python.

## Linting Configuration

### Black

The configuration for `black` is specified in the `pyproject.toml` file under the `[tool.black]` section. The settings are as follows:

- `line-length`: Set to 132 to allow longer lines.

### Flake8

The configuration for `flake8` is specified in the `.flake8` file. The settings are as follows:

- `max-line-length`: Set to 132 to allow longer lines.
- `ignore`: Ignore import order warnings.
- `select`: Be strict about syntax errors.

## Pre-commit Hook

A pre-commit hook has been added to prevent deteriorating the lint score. The pre-commit script is located at `.github/scripts/pre_commit_lint.sh`.

### Configuring the Pre-commit Hook

To configure the pre-commit hook, follow these steps:

1. Ensure you have `pre-commit` installed. You can install it using `pip`:

    ```sh
    pip install pre-commit
    ```

2. Create a `.pre-commit-config.yaml` file in the root directory with the following content:

    ```yaml
    repos:
      - repo: local
        hooks:
          - id: pre-commit-lint
            name: Pre-commit Lint
            entry: .github/scripts/pre_commit_lint.sh
            language: system
            stages: [commit]
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
black .
flake8
```

## Recommended Plugin Extensions

For a better development experience, it is recommended to use the following plugin extensions:

- **Python**: Provides rich support for the Python language, including features such as IntelliSense, linting, debugging, and more.
- **Pylance**: A performant, feature-rich language server for Python in Visual Studio Code.
- **Black**: A code formatter for Python.
- **Flake8**: A linting tool for Python.
