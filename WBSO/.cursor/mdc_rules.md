# Cursor MDC Rules for WBSO Project

## Python Files

### Module Documentation

```python
"""
Module: {module_name}
Description: {brief_description}

This module is part of the WBSO AI Agent project, following the AI-assisted coding approach.
Reference: https://docs.google.com/document/d/12ATcyjCEKh8T-MPDZ-VMiQ1XMa9FUvvk2QazrsKoiR8/edit?usp=sharing
"""

# Example for src/pdf/parser.py:
"""
Module: pdf.parser
Description: PDF parsing functionality for WBSO forms

This module handles the extraction and processing of PDF form fields,
following the AI-assisted development approach.
"""
```

### Function Documentation

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """Brief description of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Example:
        >>> function_name(value1, value2)
        expected_output
    """
```

## Markdown Files

### README.md Structure

```markdown
# Project Name

## 1. Project Overview

- Brief description
- Key features
- Main objectives

## 2. Project Structure

- Directory layout
- Key files and their purposes

## 3. Development Approach

- Development methodology
- AI-assisted coding practices
- Reference to documentation

## 4. Getting Started

- Installation steps
- Configuration
- Basic usage

## 5. Contributing

- Contribution guidelines
- Development workflow

## 6. License

- License information
- Usage restrictions
```

### Documentation Files

```markdown
# Document Title

## Overview

- Purpose of the document
- Target audience
- Key concepts

## Content Sections

- Main topics
- Implementation details
- Examples

## References

- Related documents
- External resources
```

## Project Management Files

### pyproject.toml

```toml
[project]
name = "wbso-ai-agent"
version = "0.1.0"
description = "AI Agent for WBSO form processing"
# ... other metadata

[project.optional-dependencies]
dev = [
    # Development dependencies
]

[tool.ruff]
# Linting configuration

[tool.pytest.ini_options]
# Test configuration
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      # Basic file hygiene

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.9
    hooks:
      # Code quality checks

  - repo: local
    hooks:
      # Custom project hooks
```

## AI-Assisted Development Guidelines

### Code Generation

- Use clear, specific prompts
- Include context and requirements
- Reference existing code patterns
- Request documentation and tests

### Code Review

- Check for consistency with project standards
- Verify documentation completeness
- Ensure test coverage
- Validate against requirements

### Documentation

- Keep documentation up-to-date
- Include examples and use cases
- Reference external resources
- Maintain clear structure

### Testing

- Write tests for new features
- Include edge cases
- Document test scenarios
- Maintain test coverage

## File Organization

### Source Code

- Group related functionality
- Maintain clear module structure
- Follow naming conventions
- Include type hints

### Documentation

- Keep README.md current
- Maintain API documentation
- Document architecture decisions
- Include usage examples

### Configuration

- Use standard formats
- Document settings
- Include comments
- Follow best practices
