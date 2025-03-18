# Ollama Usage Guide

This guide covers different ways to interact with Ollama and its models.

## Command Line Interface

### Basic Commands

1. List available models:
```bash
docker exec -it ollama ollama ls
```

2. Run a model:
```bash
docker exec -it ollama ollama run deepseek-coder-v2
```

3. Pull a new model:
```bash
docker exec -it ollama ollama pull llama2
```

4. Remove a model:
```bash
docker exec -it ollama ollama rm llama2
```

### Advanced Usage

1. Run with specific parameters:
```bash
docker exec -it ollama ollama run llama2 --temperature 0.7 --top-p 0.9
```

2. Stream responses:
```bash
docker exec -it ollama ollama run llama2 --stream
```

## Open Web UI

### Setup

1. Run Open Web UI container:
```bash
docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:cuda
```

2. Access the interface at [http://localhost:3000/](http://localhost:3000/)

### Configuration

1. Connect to Ollama:
   - Go to Settings
   - Set Ollama API URL to `http://ollama:11434`
   - Save settings

2. Configure Models:
   - Go to Models section
   - Click "Add Model"
   - Select from available models
   - Configure parameters

### Features

- Chat interface
- Model management
- Parameter configuration
- Response streaming
- History management
- Export conversations

## Visual Studio Code / Cursor

### Setup

1. Install the "Continue Dev" extension
2. Configure settings:
```json
{
    "continue.model": "ollama/deepseek-coder-v2",
    "continue.apiBase": "http://localhost:11434"
}
```

### Usage

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Continue" to see available commands
3. Select "Continue: Chat" to start a conversation

### Features

- Inline code completion
- Chat interface
- Code explanation
- Refactoring suggestions
- Documentation generation

## Python Integration

### Basic Usage

```python
import requests

def query_ollama(prompt, model="llama2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
```

### Example Usage

```python
# Example from examples/basic_usage.py
from ollama import Client

client = Client()
response = client.chat(model='llama2', messages=[
    {
        'role': 'user',
        'content': 'Hello, how are you?'
    }
])
print(response['message']['content'])
```

## Jupyter Notebooks

Check the `examples/notebooks/` directory for:
- Basic model interaction
- RAG implementation
- Code generation
- Document analysis

## Best Practices

1. **Model Selection**
   - Use appropriate models for specific tasks
   - Consider model size vs. performance
   - Test different models for your use case

2. **Performance Optimization**
   - Use streaming for long responses
   - Adjust temperature and top_p parameters
   - Monitor GPU memory usage

3. **Error Handling**
   - Implement proper error handling
   - Check API response status
   - Handle timeouts appropriately

4. **Security**
   - Keep models updated
   - Monitor API access
   - Secure sensitive data
