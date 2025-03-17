# Ollama Setup Guide

This guide provides detailed instructions for setting up Ollama using different installation methods.

## Docker Installation

### Initial Setup

1. Start Ollama with GPU support:
```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

2. Verify the installation:
- Health Check: [http://localhost:11434/](http://localhost:11434/)
- Version Endpoint: [http://localhost:11434/api/version](http://localhost:11434/api/version)

### Updating Ollama

To update Ollama to the latest version:

1. Stop and remove the existing container:
```bash
docker stop ollama
docker rm ollama
```

2. Pull the latest image:
```bash
docker pull ollama/ollama
```

3. Run the new container:
```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Windows Installation

### Prerequisites

1. Windows 10 or later
2. WSL2 (Windows Subsystem for Linux) installed
3. Docker Desktop for Windows installed

### Installation Steps

1. Install WSL2 if not already installed:
```powershell
wsl --install
```

2. Install Docker Desktop for Windows:
- Download from [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Run the installer
- Enable WSL2 integration in Docker Desktop settings

3. Install Ollama using WSL2:
```bash
curl https://ollama.ai/install.sh | sh
```

4. Start Ollama service:
```bash
ollama serve
```

### Verifying Installation

1. Open a new terminal and check Ollama status:
```bash
ollama list
```

2. Test with a simple model:
```bash
ollama run llama2
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Set to `http://localhost:11434` for local access
- `OLLAMA_MODELS`: Path to store downloaded models (default: `~/.ollama/models`)

### GPU Support

For GPU support:
- NVIDIA GPU with CUDA support
- Latest NVIDIA drivers installed, prefer Studio version over Game version
- CUDA toolkit installed (for development)

## Troubleshooting

### Common Issues

1. **Docker Container Won't Start**
   - Check if ports are available
   - Verify GPU support configuration
   - Check Docker logs: `docker logs ollama`

2. **Windows WSL2 Issues**
   - Update WSL2: `wsl --update`
   - Reset WSL2: `wsl --shutdown`
   - Check WSL2 status: `wsl --status`

3. **GPU Not Detected**
   - Verify NVIDIA drivers
   - Check CUDA installation
   - Ensure Docker has GPU access 