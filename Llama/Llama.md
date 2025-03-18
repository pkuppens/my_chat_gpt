# Exploratory Project: Learning Ollama and LlamaIndex

## Overview
This project aims to explore the use of local large language models (LLMs) through Ollama and
LlamaIndex for various software engineering tasks. The goal is to build a proof-of-concept that
utilizes LLMs in areas such as requirements engineering, software architecture, code generation,
and code review.
The project will be broken down into key phases, including setup, model exploration, integration,
and testing, with milestones, demos, and tests to track progress.

## Project Plan

### 1. Setup Environment
- **Goal:** Set up the local development environment using Ollama and Docker.
- **Steps:**
  1. Run an Ollama Docker container using all available GPUs:
     ```bash
     docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
     ```
  2. Verify that Ollama is running by checking the local endpoint:
     - [http://localhost:11434/](http://localhost:11434/)
     - [http://localhost:11434/api/version](http://localhost:11434/api/version)

- **Milestone:** Ollama container running and accessible via local API.

### 2. Integrate with Open-WebUI
- **Goal:** Add a web interface for easier interaction with LLMs.
- **Steps:**
  1. Set up a local Docker container for Open-WebUI:
     ```bash
     docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:cuda
     ```
  2. Access Open-WebUI via [http://localhost:3000/](http://localhost:3000/).
  3. Test running models through the web interface.

- **Milestone:** Open-WebUI running with access to Ollama models.

### 3. Model Exploration
- **Goal:** Discover and test local models with Ollama.
- **Steps:**
  1. List the available models:
     ```bash
     docker exec -it ollama ollama ls
     ```
     Example output:
     ```text
     NAME                            ID              SIZE    MODIFIED
     qwen2.5-coder:latest            87098ba7390d    4.7 GB  24 minutes ago
     llama3.2:latest                 a80c4f17acd5    2.0 GB  28 minutes ago
     deepseek-coder-v2:latest        63fb193b3a9b    8.9 GB  38 minutes ago
     llama3.1:latest                 91ab477bec9d    4.7 GB  8 weeks ago
     ```
  2. Pull and run a specific model, for example, Deepseek Coder:
     ```bash
     docker exec -it ollama ollama run deepseek-coder-v2
     ```
  3. Explore other models such as `llama3.1` and `qwen2.5-coder`.

- **Milestone:** Successfully run and test models locally.

### 4. Integrate LlamaIndex
LlamaIndex is a framework that helps organize and manage data when querying LLMs, making it an ideal tool for structured tasks such as document retrieval, query answering, and knowledge extraction. We'll be creating a separate detailed project breakdown for LlamaIndex in a new document: **LlamaIndex.md**.

- **Link:** [LlamaIndex.md](./LlamaIndex.md)

The LlamaIndex component will cover:
1. **What LlamaIndex is:** A high-level introduction to LlamaIndex, explaining how it facilitates the use of LLMs by acting as a data connector.
2. **How LlamaIndex can be used:** Examples of practical applications such as retrieval-augmented generation (RAG), document indexing, and automated Q&A.

We will break down the LlamaIndex setup into easy-to-follow steps with Jupyter Notebooks for demo-ready tasks, such as:
- Loading and indexing documents
- Running queries
- Using RAG for enhanced responses

We will reference some of the best LlamaIndex tutorials, including:
- [LlamaIndex: An Overview and Tutorials](https://gpt-index.readthedocs.io/en/latest/)
- [Integrating LlamaIndex with Local Models](https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/)
- [Example Notebooks](https://github.com/jerryjliu/gpt_index/tree/main/examples/notebooks)

- **Milestone:** LlamaIndex integrated with Ollama, with demo-ready notebooks for testing and validation.

---

## Timeline and Milestones
1. **Step 1-2:** Set up environment and explore models.
2. **Step 3-4:** Integrate Open-WebUI and LlamaIndex.
3. **Step 5:** Write and run test cases.
4. **Step 6:** Present demo and gather feedback.
