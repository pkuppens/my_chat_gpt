# Ollama

## Run a local Ollama Docker container using all GPUs

`docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

### Finding and Exploring the API

Check if `Ollama is running`:
(http://localhost:11434/)[http://localhost:11434/]

And the version end point:

(http://localhost:11434/api/version)[http://localhost:11434/api/version]

The API documentation for exploring other routes:
(https://github.com/ollama/ollama/blob/main/docs/api.md)[https://github.com/ollama/ollama/blob/main/docs/api.md]

## Locally install new LLMs

### Root command to execute ollama command in docker:
`docker exec -it ollama` ...

### Example to list already present models:

`docker exec -it ollama ollama ls`

```
NAME                            ID              SIZE    MODIFIED
qwen2.5-coder:latest            87098ba7390d    4.7 GB  24 minutes ago
llama3.2:latest                 a80c4f17acd5    2.0 GB  28 minutes ago
deepseek-coder-v2:latest        63fb193b3a9b    8.9 GB  38 minutes ago
llama3.1:latest                 91ab477bec9d    4.7 GB  8 weeks ago
```

### Example to pull and run the deepseek-coder-v2 model

We need to append the ollama run command: `ollama run deepseek-coder-v2`

So combined:
`docker exec -it ollama ollama run deepseek-coder-v2`

### Library

Use this library to explore new language models:

[https://ollama.com/library](https://ollama.com/library)

### Alternative interesting models/commands:


docker exec -it ollama ollama run llama3.1
docker exec -it ollama ollama run llama3.2
ollama run llama3.2:1b
docker exec -it ollama ollama run qwen2.5-coder
ollama run qwen2.5-coder:1.5b

## Connecting to DSpy:

[ollama+DSPy using OpenAI APIs.](https://gist.github.com/jrknox1977/78c17e492b5a75ee5bbaf9673aee4641)

### Local Ollama

Note that this may not be the docker version you may expect?!

https://dspy-docs.vercel.app/api/local_language_model_clients/Ollama

This may be?!

https://dspy-docs.vercel.app/docs/deep-dive/language_model_clients/local_models/HFClientTGI

## Accessing via open-webui

Open Web UI is an elegant way to talk to the LLMs via a Web interface:

https://docs.openwebui.com/

Example to run a local docker containerize Open-WebUI:
After running the container, wait 10-15 seconds and find the web interface at: http://localhost:3000/

`docker run --hostname=10969117fc2f --user=0:0 --mac-address=02:42:ac:11:00:03 --env=PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=LANG=C.UTF-8 --env=GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D --env=PYTHON_VERSION=3.11.10 --env=ENV=prod --env=PORT=8080 --env=USE_OLLAMA_DOCKER=false --env=USE_CUDA_DOCKER=true --env=USE_CUDA_DOCKER_VER=cu121 --env=USE_EMBEDDING_MODEL_DOCKER=sentence-transformers/all-MiniLM-L6-v2 --env=USE_RERANKING_MODEL_DOCKER= --env=OLLAMA_BASE_URL=/ollama --env=OPENAI_API_BASE_URL= --env=OPENAI_API_KEY= --env=WEBUI_SECRET_KEY= --env=SCARF_NO_ANALYTICS=true --env=DO_NOT_TRACK=true --env=ANONYMIZED_TELEMETRY=false --env=WHISPER_MODEL=base --env=WHISPER_MODEL_DIR=/app/backend/data/cache/whisper/models --env=RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 --env=RAG_RERANKING_MODEL= --env=SENTENCE_TRANSFORMERS_HOME=/app/backend/data/cache/embedding/models --env=HF_HOME=/app/backend/data/cache/embedding/models --env=HOME=/root --env=WEBUI_BUILD_VERSION=1d225dd804575af9ae5981528dfdce695f7f7040 --env=DOCKER=true --volume=open-webui:/app/backend/data --network=bridge --workdir=/app/backend -p 3000:8080 --restart=always --label='org.opencontainers.image.created=2024-09-26T18:59:47.570Z' --label='org.opencontainers.image.description=User-friendly WebUI for AI (Formerly Ollama WebUI)' --label='org.opencontainers.image.licenses=MIT' --label='org.opencontainers.image.revision=1d225dd804575af9ae5981528dfdce695f7f7040' --label='org.opencontainers.image.source=https://github.com/open-webui/open-webui' --label='org.opencontainers.image.title=open-webui' --label='org.opencontainers.image.url=https://github.com/open-webui/open-webui' --label='org.opencontainers.image.version=main-cuda' --add-host host.docker.internal:host-gateway --runtime=runc -d ghcr.io/open-webui/open-webui:cuda`

# my_chat_gpt

Collection of ChatGPT experiments

## SuperPrompt

The prompt to improve all prompts.

## CollegeGPT

Apply ChatGPT to College:
1. Give recommendations for rewriting the college
2. Generate multiple-choice questions for the exam
