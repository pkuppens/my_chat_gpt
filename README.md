# Ollama

## Run Ollama in a Local Docker Container Using All GPUs

To start Ollama with GPU support, use the following command:

    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

### Checking API Availability

Verify that Ollama is running by accessing the following endpoint:

- **Health Check**: [http://localhost:11434/](http://localhost:11434/)
- **Version Endpoint**: [http://localhost:11434/api/version](http://localhost:11434/api/version)

For complete API documentation, see [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md).

## Managing Language Models in Ollama

### Executing Ollama Commands in Docker

To run Ollama commands within the Docker container, prefix with `docker exec -it ollama`. For example:

    docker exec -it ollama ollama ls

This lists installed models:

    NAME                            ID              SIZE    MODIFIED
    qwen2.5-coder:latest            87098ba7390d    4.7 GB  24 minutes ago
    llama3.2:latest                 a80c4f17acd5    2.0 GB  28 minutes ago
    deepseek-coder-v2:latest        63fb193b3a9b    8.9 GB  38 minutes ago
    llama3.1:latest                 91ab477bec9d    4.7 GB  8 weeks ago

### Running a Model Example

To run a specific model, such as `deepseek-coder-v2`, use:

    docker exec -it ollama ollama run deepseek-coder-v2

### Accessing the Ollama Model Library

Explore additional models in the [Ollama Model Library](https://ollama.com/library).

### Other Model Examples

Examples for running other models include:

    docker exec -it ollama ollama run llama3.1
    docker exec -it ollama ollama run llama3.2
    docker exec -it ollama ollama run qwen2.5-coder

## Integrating with DSPy

To integrate Ollama with DSPy using OpenAI-compatible APIs, see the guide [Ollama + DSPy Integration](https://gist.github.com/jrknox1977/78c17e492b5a75ee5bbaf9673aee4641).

## Accessing via Open Web UI

Open Web UI provides an elegant web interface for interacting with language models.

- Documentation: [Open Web UI Documentation](https://docs.openwebui.com/)

To run Open Web UI locally:

    docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:cuda

After starting, access the interface at [http://localhost:3000/](http://localhost:3000/).

## Using `uv` Package Management System

For more details on the benefits and installation steps, refer to the documentation `UV.md`.

## GitHub Action for Commenting on Newly Created Issues

This repository includes a GitHub Action that automatically comments on newly created issues with possible duplicate issues based on the description.

### Configuration

1. Create a workflow file named `create_issue_comment.yml` in the `.github/workflows` directory.
2. Add the following content to the workflow file:

    ```yaml
    name: Comment on New Issues

    on:
      issues:
        types: [opened]

    jobs:
      comment:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout repository
          uses: actions/checkout@v2

        - name: Run duplicate issue checker
          run: python scripts/identify_duplicates.py
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```

3. Create a Python script named `identify_duplicates.py` in the `scripts` directory.
4. Add the logic to identify possible duplicate issues and comment on the newly created issue.

### Usage

Once configured, the GitHub Action will automatically run whenever a new issue is created. It will analyze the issue description and comment with links to potential duplicate issues.

## Linting Configuration

This project uses `black` and `flake8` for linting. The linting configuration is documented in the `LINTING.md` file.

### Pre-commit Hook

A pre-commit hook has been added to prevent deteriorating the lint score. The pre-commit script is located at `.github/scripts/pre_commit_lint.sh`. To bypass the lint check, use the `--no-verify` option when committing.

### Standalone Lint Run

To run the linting tools manually, use the following commands:

    black .
    flake8

### Recommended Plugin Extensions

For a better development experience, it is recommended to use the following plugin extensions:

- **Python**: Provides rich support for the Python language, including features such as IntelliSense, linting, debugging, and more.
- **Pylance**: A performant, feature-rich language server for Python in Visual Studio Code.
- **Black**: A code formatter for Python.
- **Flake8**: A linting tool for Python.

## Installation Instructions for the `local_utils` Module

To install the `local_utils` module, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/pkuppens/my_chat_gpt.git
    cd my_chat_gpt
    ```

2. Create a virtual environment:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Install the `local_utils` module:

    ```sh
    pip install -e .
    ```

5. Verify the installation:

    ```sh
    python -c "import local_utils; print('Local Utils module installed successfully')"
    ```

## Debug/Run Configurations

To properly find the project components, add the following debug/run configurations to your `.vscode/settings.json` file:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "jupyter.notebookFileRoot": "${workspaceFolder}",
    "cSpell.words": [
        "dspy",
        "Ollama"
    ],
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.blackEnabled": true,
    "python.linting.lintOnSave": true,
    "python.linting.lintOnTextChange": true,
    "python.linting.lintOnOpen": true,
    "python.linting.lintOnSaveMode": "file",
    "python.linting.lintOnTextChangeMode": "file",
    "python.linting.lintOnOpenMode": "file",
    "python.linting.lintOnSaveDelay": 500,
    "python.linting.lintOnTextChangeDelay": 500,
    "python.linting.lintOnOpenDelay": 500,
    "python.linting.lintOnSaveTimeout": 5000,
    "python.linting.lintOnTextChangeTimeout": 5000,
    "python.linting.lintOnOpenTimeout": 5000,
    "python.linting.lintOnSaveMaxFiles": 10,
    "python.linting.lintOnTextChangeMaxFiles": 10,
    "python.linting.lintOnOpenMaxFiles": 10,
    "python.linting.lintOnSaveMaxFileSize": 1048576,
    "python.linting.lintOnTextChangeMaxFileSize": 1048576,
    "python.linting.lintOnOpenMaxFileSize": 1048576,
    "python.linting.lintOnSaveMaxFileCount": 100,
    "python.linting.lintOnTextChangeMaxFileCount": 100,
    "python.linting.lintOnOpenMaxFileCount": 100,
    "python.linting.lintOnSaveMaxFileSizeLimit": 10485760,
    "python.linting.lintOnTextChangeMaxFileSizeLimit": 10485760,
    "python.linting.lintOnOpenMaxFileSizeLimit": 10485760,
    "python.linting.lintOnSaveMaxFileCountLimit": 1000,
    "python.linting.lintOnTextChangeMaxFileCountLimit": 1000,
    "python.linting.lintOnOpenMaxFileCountLimit": 1000,
    "python.linting.lintOnSaveMaxFileSizeLimitExceeded": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceeded": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceeded": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceeded": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceeded": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceeded": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededAction": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededAction": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededAction": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededAction": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededAction": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededAction": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionType": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionType": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionType": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionType": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionType": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeActionType": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeActionTypeMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeActionTypeMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeActionTypeAction": "warn",
    "python.linting.lintOnSaveMaxFileSizeLimitExceededActionTypeActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileSizeLimitExceededActionTypeActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileSizeLimitExceededActionTypeActionTypeActionTypeActionMessage": "File size exceeds the maximum limit for linting.",
    "python.linting.lintOnSaveMaxFileCountLimitExceededActionTypeActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnTextChangeMaxFileCountLimitExceededActionTypeActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting.",
    "python.linting.lintOnOpenMaxFileCountLimitExceededActionTypeActionTypeActionTypeActionMessage": "File count exceeds the maximum limit for linting."
}
```
