# Ollama Stack: Enhanced Local AI Development Environment

## Overview

This stack provides a modular, customizable local environment for experimenting with LLMs using:

- **Ollama**: Fast local inference with open models (GPU-accelerated)
- **Open WebUI**: Chat-like UI for easy use (GPU-accelerated, based on [official documentation](https://docs.openwebui.com/getting-started/quick-start/))
- **LangFlow**: Visual agent/chain builder
- **Extra tools**: Vim, zsh/csh, htop, git
- **Self-updating**: Via Watchtower or `update.sh`

## Development Mode with Shared Volumes

### Purpose

The stack is configured to use a shared Ollama volume, which means:

- Models downloaded in one instance are available to all Ollama installations
- No duplicate model storage across different installations
- Persistent model storage even when containers are stopped/removed
- Faster development workflow with shared resources

### Setup Steps

1. **Create the shared volume** (if it doesn't exist):

   ```bash
   docker volume create ollama
   ```

2. **Verify the volume exists**:

   ```bash
   docker volume inspect ollama
   ```

3. **Start the stack**:
   ```bash
   docker-compose up -d
   ```

The stack will automatically use the shared volume because of the volume configuration in `docker-compose.yml`:

```yaml
volumes:
  ollama:
    external: true # Use existing volume instead of creating new one
    name: ollama # Explicit name to ensure consistency
```

### Benefits

- **Storage Efficiency**: Models are stored once and shared across instances
- **Development Speed**: No need to re-download models for different projects
- **Consistency**: All instances use the same model versions
- **Persistence**: Models remain available even after container removal

### Important Notes

- The shared volume is mounted at `/root/.ollama` in the container
- Model downloads through Open WebUI or direct API calls will use this shared storage
- Other Ollama installations can use the same volume by configuring their `docker-compose.yml` similarly

## ⚠️ Production Use Warning

This configuration is optimized for local development and experimentation. For production use, you should:

1. **Volume Configuration**:

   - Remove the `external: true` and `name: ollama` from the volume configuration
   - Let Docker Compose manage volumes with project-specific names
   - This prevents potential conflicts and security issues in multi-tenant environments

2. **Security**:

   - Enable authentication in Open WebUI (`WEBUI_AUTH=true`)
   - Restrict network access to necessary ports only
   - Use proper secrets management for API keys and credentials
   - Implement proper access controls and rate limiting

3. **Resource Management**:

   - Set explicit resource limits for containers
   - Implement proper monitoring and logging
   - Use production-grade orchestration (e.g., Kubernetes) for scaling

4. **Data Persistence**:
   - Implement proper backup strategies
   - Use production-grade storage solutions
   - Consider data encryption at rest

## Prerequisites

- Docker with NVIDIA Container Toolkit installed
- NVIDIA GPU with CUDA support
- NVIDIA drivers installed on the host system

## Folder Structure

```
ollama-stack/
├── docker-compose.yml
├── ollama-plus/
│   └── Dockerfile
├── code/               # Your Python or LangChain code (mounted volume)
├── data/               # Local experiments, logs, outputs
├── update.sh           # Manual rebuild/update script
└── README.md
```

## Volumes Explained

| Volume       | Purpose                                  | Notes                                                |
| ------------ | ---------------------------------------- | ---------------------------------------------------- |
| `ollama`     | Cache of downloaded Ollama models        | **⚠️ Shared with other Ollama installations**        |
| `open-webui` | Persistent storage for Open WebUI data   | Prevents data loss between container restarts        |
| `./code`     | Source code mounted from host            | Enables live editing and version control             |
| `./data`     | Save experimental results, prompts, logs | Keep persistent output without baking into container |

### ✅ This design lets you:

- Update code without rebuilding
- Use the same model files across containers
- Keep your experimental data persistent and organized
- Maintain Open WebUI settings and data between restarts
- Leverage GPU acceleration for faster inference

> Challenge: You could combine models/data/code into one volume, but separation improves clarity, git workflow, and portability.

## Usage

### 1. Start the full stack

```bash
docker-compose up -d
```

### 2. Rebuild manually (optional)

```bash
./update.sh
```

### 3. Auto-update (optional)

Watchtower will check every hour for updated images.

## Accessing Tools

- **Ollama API**: http://localhost:11434
- **Open WebUI**: http://localhost:3000 (based on [official documentation](https://docs.openwebui.com/getting-started/quick-start/))
- **LangFlow**: http://localhost:7860

### Open WebUI Configuration

The Open WebUI service is configured according to the [official documentation](https://docs.openwebui.com/getting-started/quick-start/):

- Port mapping: 3000:8080 (host:container)
- Persistent storage: `/app/backend/data`
- Authentication disabled for local development
- Connected to Ollama service via internal network
- GPU acceleration enabled using CUDA image

---

## GPU Support

Both Ollama and Open WebUI are configured for GPU acceleration:

- Uses NVIDIA Container Toolkit for GPU access
- CUDA-enabled Open WebUI image
- Automatic GPU device allocation
- Shared GPU resources between containers

> Note: Ensure your system meets the prerequisites for GPU support.
