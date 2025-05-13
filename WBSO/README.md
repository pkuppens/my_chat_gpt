# WBSO AI Agent

This project implements an AI Agent to assist with filling out WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) development project software application forms.

## 1. Project Overview

The WBSO AI Agent is designed to:

- Parse PDF forms to identify input fields
- Match input fields to question text blocks and context
- Determine input data types and constraints
- Extract structured output using LLM
- Generate specific prompts for form questions
- Integrate with local LLM

## 2. Project Structure

```
WBSO/
├── README.md                 # This file
├── pyproject.toml           # Project configuration and dependencies
├── LICENSE                  # License file
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── src/                      # Source code
│   ├── __init__.py
│   ├── pdf/                  # PDF processing modules
│   │   ├── __init__.py
│   │   ├── parser.py        # PDF parsing functionality
│   │   └── matcher.py       # Field matching logic
│   ├── llm/                  # LLM integration
│   │   ├── __init__.py
│   │   ├── client.py        # LLM client implementation
│   │   └── prompts.py       # Prompt templates
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── validators.py    # Input validation
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_matcher.py
│   └── test_llm.py
└── docs/                    # Documentation
    ├── architecture.md      # System architecture
    └── api.md              # API documentation
```

## 3. Development Approach

This project follows the AI-assisted coding approach as outlined in [Full Process for Coding with AI Coding Assistants](https://docs.google.com/document/d/12ATcyjCEKh8T-MPDZ-VMiQ1XMa9FUvvk2QazrsKoiR8/edit?usp=sharing).

Key aspects of the development process:

1. Clear problem definition and requirements gathering
2. Incremental development with AI assistance
3. Regular testing and validation
4. Documentation-driven development
5. Continuous integration and deployment

## 4. Getting Started

1. Clone the repository
2. Install uv package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync  # for initial setup
   uv pip install -e ".[dev]"  # Install package in editable mode with dev dependencies
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

## 5. Contributing

TODO: Contributing guidelines will be added in CONTRIBUTING.md. For now, please contact the project maintainer for contribution guidelines.

## 6. License

This project is licensed under the MIT License with commercial use restrictions. See the [LICENSE](LICENSE) file for details.

Commercial use of this software requires explicit approval from the author. For commercial licensing inquiries, please contact the project maintainer.
