# My ChatGPT Utils

A collection of utilities and tools for working with ChatGPT and related AI technologies.

## Project Structure

- `my_chat_gpt_utils/` - Core utility functions and modules for ChatGPT integration
- `tests/` - Test suite for the project
- `scripts/` - Utility scripts for development and automation
- `notebooks/` - Jupyter notebooks for experimentation and analysis
- `SuperPrompt/` - Tools, utilities, and examples for working with super prompts
- `SoftwareFactorAI/` - AI-powered software development tools
- `CollegeGPT/` - Educational AI tools and resources
- `Llama/` - Llama local model integration and utilities
- `DeveloGPT/` - Development-focused AI tools
- `Hackathon/` - Project-specific hackathon resources
- `dspyui/` - DSPy UI components and utilities
- `history_download/` - Tools for downloading and processing chat history
- `src/` - Source code for additional components

## Development Setup

1. Install dependencies using UV package manager (see `docs/package_management/UV.md`)
2. Configure linting (see `docs/development/LINTING.md`)
3. Set up pre-commit hooks for code quality
4. Set up testing environment (see `docs/testing/TEST-STRATEGY.md`)

## Documentation

- Package Management: `docs/package_management/`
- Development Guidelines: `docs/development/`
  - [Issue Best Practices](docs/development/ISSUE_BEST_PRACTICES.md) - How to write high-quality issues
  - [Issue Review Workflow](docs/development/ISSUE_REVIEW_WORKFLOW.md) - AI-powered issue review system
  - [Linting](docs/development/LINTING.md) - Code quality guidelines
- Testing Strategy: `docs/testing/`
- AI Resources: `docs/ai_resources/`
- Examples: `docs/examples/` - Example issues and templates
- Project-specific docs: See individual directory READMEs

## Features

### OpenAI Agent SDK with Guardrails

A modular agent system with swappable LLM providers and guardrails.

**Key Features:**
- ✅ Swappable LLM providers (OpenAI, Ollama, custom)
- ✅ Swappable guardrail providers (OpenAI, Gemini, Local)
- ✅ Agent creation from SuperPrompt templates
- ✅ Multi-agent orchestration and delegation
- ✅ File operations and custom tools
- ✅ Prompt composition and reuse

**Quick Start:**
```bash
# Run the example script
python notebooks/quick_start_example.py

# Or explore the Jupyter notebook
jupyter notebook notebooks/OpenAI_Agents_SDK_with_Guardrails.ipynb
```

**Learn More:** See [notebooks/README_OpenAI_Agents.md](notebooks/README_OpenAI_Agents.md)

### AI-Powered Issue Review

This project includes an automated AI-powered workflow that reviews all newly opened GitHub issues. The workflow:

- ✅ Analyzes issue title clarity
- ✅ Checks title and description alignment
- ✅ Evaluates SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
- ✅ Suggests improvements and next steps
- ✅ Automatically adds relevant labels (Type, Priority, Complexity)
- ✅ Posts detailed review feedback as a comment
- ✅ Uses best practices embedded in the review prompt

**Learn more**:
- [Issue Review Workflow Documentation](docs/development/ISSUE_REVIEW_WORKFLOW.md)
- [Workflow Configuration Guide](docs/development/WORKFLOW_CONFIGURATION.md) - Setup instructions and secrets management

## License

See LICENSE file for details.
