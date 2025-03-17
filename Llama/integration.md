# Ollama Integration Guide

This guide covers integrating Ollama with various tools and frameworks.

## DSPy Integration

### Setup

1. Install DSPy:
```bash
pip install dspy-ai
```

2. Configure DSPy to use Ollama:
```python
import dspy
from dspy.teleprompt import BootstrapFewShot

# Configure DSPy to use Ollama
dspy.configure(
    model='ollama/deepseek-coder-v2',
    api_base='http://localhost:11434'
)
```

### Example Usage

```python
# Example from examples/dspy_integration.py
from dspy import Module, InputField, OutputField

class CodeGenerator(Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought("input -> output")
    
    def forward(self, input):
        return self.generate(input=input)
```

## LlamaIndex Integration

### Setup

1. Install LlamaIndex:
```bash
pip install llama-index
```

2. Configure LlamaIndex:
```python
from llama_index.llms import Ollama
from llama_index.core import Settings

# Configure LlamaIndex to use Ollama
Settings.llm = Ollama(
    model="deepseek-coder-v2",
    base_url="http://localhost:11434"
)
```

### Example Usage

```python
# Example from examples/llamaindex_integration.py
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader('data').load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query the index
response = index.query("What are the main features?")
print(response)
```

## LangChain Integration

### Setup

1. Install LangChain:
```bash
pip install langchain
```

2. Configure LangChain:
```python
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager

# Create Ollama instance
llm = Ollama(
    base_url='http://localhost:11434',
    model="deepseek-coder-v2"
)
```

### Example Usage

```python
# Example from examples/langchain_integration.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question: {question}"
)

# Create chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run chain
response = chain.run("What is the capital of France?")
print(response)
```

## Custom Integration

### API Reference

Ollama provides a REST API for integration:

```python
import requests

def generate_response(prompt, model="llama2"):
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

### WebSocket API

For streaming responses:

```python
import websockets
import asyncio
import json

async def stream_response(prompt, model="llama2"):
    async with websockets.connect("ws://localhost:11434/api/generate") as websocket:
        await websocket.send(json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": True
        }))
        
        while True:
            response = await websocket.recv()
            if response == "[DONE]":
                break
            yield json.loads(response)["response"]
```

## Best Practices

1. **Error Handling**
   - Implement proper error handling
   - Handle API timeouts
   - Validate responses

2. **Performance**
   - Use streaming for long responses
   - Implement caching where appropriate
   - Monitor resource usage

3. **Security**
   - Secure API endpoints
   - Validate input data
   - Handle sensitive information

4. **Testing**
   - Write unit tests
   - Test error scenarios
   - Validate responses 