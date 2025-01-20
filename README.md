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
