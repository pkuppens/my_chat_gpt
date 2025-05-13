# Project Management MDC Rules

## Version Control

### Git Commit Messages

```
type(scope): subject

body

footer
```

Types:

- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test changes
- chore: Maintenance tasks

Example:

```
feat(pdf): add form field extraction

- Implement PDF form field detection
- Add field value extraction
- Include basic validation

Closes #42
```

## Project Structure

### Directory Organization

```
project/
├── src/                    # Source code
│   ├── module1/           # Feature module
│   │   ├── __init__.py
│   │   ├── core.py       # Core functionality
│   │   └── utils.py      # Module utilities
│   └── module2/           # Another feature module
├── tests/                 # Test suite
│   ├── module1/          # Module tests
│   └── module2/          # Module tests
├── docs/                  # Documentation
│   ├── api/              # API documentation
│   └── guides/           # User guides
└── scripts/              # Utility scripts
```

## Documentation

### API Documentation

````markdown
# Module Name

## Overview

Brief description of the module's purpose and functionality.

## Classes

### ClassName

Description of the class.

#### Methods

##### method_name(param1: type, param2: type) -> return_type

Description of the method.

**Parameters:**

- param1: Description
- param2: Description

**Returns:**
Description of return value

**Example:**

```python
instance = ClassName()
result = instance.method_name(value1, value2)
```
````

````

### Architecture Documentation
```markdown
# System Architecture

## Overview
High-level description of the system architecture.

## Components

### Component 1
- Purpose
- Responsibilities
- Dependencies

### Component 2
- Purpose
- Responsibilities
- Dependencies

## Data Flow
Description of how data flows through the system.

## Security
Security considerations and measures.
````

## Development Workflow

### Feature Development

1. Create feature branch
2. Implement changes
3. Write tests
4. Update documentation
5. Create pull request
6. Code review
7. Merge to main

### Bug Fixes

1. Create bug fix branch
2. Write failing test
3. Fix the bug
4. Update documentation
5. Create pull request
6. Code review
7. Merge to main

## Configuration Management

### Environment Variables

```bash
# Application
WBSO_ENV=development
WBSO_DEBUG=true

# API Keys
WBSO_OPENAI_API_KEY=sk-...
WBSO_ANTHROPIC_API_KEY=sk-...

# Model Settings
WBSO_MODEL_NAME=gpt-4
WBSO_TEMPERATURE=0.7
```

### Configuration Files

```yaml
# config.yaml
app:
  name: WBSO AI Agent
  version: 0.1.0
  environment: development

api:
  openai:
    model: gpt-4
    temperature: 0.7
    max_tokens: 2000

pdf:
  max_file_size: 10485760 # 10MB
  allowed_types:
    - application/pdf
```

## Testing Strategy

### Test Categories

1. Unit Tests

   - Test individual components
   - Mock external dependencies
   - Focus on edge cases

2. Integration Tests

   - Test component interactions
   - Use test databases
   - Verify data flow

3. End-to-End Tests
   - Test complete workflows
   - Use real dependencies
   - Verify user scenarios

### Test Organization

```
tests/
├── unit/
│   ├── test_module1.py
│   └── test_module2.py
├── integration/
│   ├── test_workflow1.py
│   └── test_workflow2.py
└── e2e/
    ├── test_scenario1.py
    └── test_scenario2.py
```

## Deployment

### Deployment Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Environment variables set
- [ ] Dependencies updated
- [ ] Security review completed
- [ ] Performance tested
- [ ] Backup strategy in place

### Release Process

1. Version bump
2. Update changelog
3. Create release branch
4. Run full test suite
5. Build artifacts
6. Deploy to staging
7. Verify functionality
8. Deploy to production
9. Monitor for issues
