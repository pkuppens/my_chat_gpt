# Llama Integration

This directory contains tools and utilities for working with Llama models and Ollama integration. The documentation is split into several sections:

- [Setup Guide](setup.md) - Installation and configuration instructions for Ollama
- [Usage Guide](usage.md) - How to use Ollama with different interfaces and tools
- [Integration Guide](integration.md) - Connecting Ollama with other tools and frameworks
- [Examples](examples/) - Code examples and notebooks demonstrating Ollama usage

## Project Structure

- `setup.md` - Installation and configuration instructions
- `usage.md` - Usage instructions for different interfaces
- `integration.md` - Integration with other tools
- `examples/` - Code examples and notebooks
- `utils/` - Utility functions for Ollama integration

## Quick Start

1. Choose your preferred installation method:
   - [Docker Installation](setup.md#docker-installation)
   - [Windows Installation](setup.md#windows-installation)

2. Select your preferred interface:
   - [Command Line](usage.md#command-line-interface)
   - [Open Web UI](usage.md#open-web-ui)
   - [Visual Studio Code / Cursor](usage.md#visual-studio-code--cursor)

3. Explore examples in the `examples/` directory:
   - Python utilities
   - Jupyter notebooks
   - Integration examples

## Running Ollama in a Local Docker Container

To start Ollama with GPU support:

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### API Endpoints

- Health Check: [http://localhost:11434/](http://localhost:11434/)
- Version Endpoint: [http://localhost:11434/api/version](http://localhost:11434/api/version)

For complete API documentation, see [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md).

## Managing Language Models

### Docker Commands

To run Ollama commands within the Docker container, prefix with `docker exec -it ollama`. For example:

```bash
docker exec -it ollama ollama ls
```

This lists installed models:

```
NAME                            ID              SIZE    MODIFIED
qwen2.5-coder:latest            87098ba7390d    4.7 GB  24 minutes ago
llama3.2:latest                 a80c4f17acd5    2.0 GB  28 minutes ago
deepseek-coder-v2:latest        63fb193b3a9b    8.9 GB  38 minutes ago
llama3.1:latest                 91ab477bec9d    4.7 GB  8 weeks ago
```

### Running Models

To run a specific model:

```bash
docker exec -it ollama ollama run deepseek-coder-v2
```

Explore additional models in the [Ollama Model Library](https://ollama.com/library).

## Integration with DSPy

To integrate Ollama with DSPy using OpenAI-compatible APIs, see the guide [Ollama + DSPy Integration](https://gist.github.com/jrknox1977/78c17e492b5a75ee5bbaf9673aee4641).

## Web Interface

Open Web UI provides an elegant web interface for interacting with language models.

- Documentation: [Open Web UI Documentation](https://docs.openwebui.com/)

To run Open Web UI locally:

```bash
docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:cuda
```

Access the interface at [http://localhost:3000/](http://localhost:3000/).
