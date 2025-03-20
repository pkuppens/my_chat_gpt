# Testing Strategy

## Overview
This document outlines the testing strategy for the MyChatGPT project, including core principles, test levels, implementation guidelines, and practical setup instructions.

## Core Principles

1. **Test Business Logic, Not Implementation Details**
   - Focus on validating required functionality and behavior
   - Avoid testing implementation specifics (e.g., class instance comparisons)
   - Verify that components provide necessary interfaces and capabilities
   - Test one behavior at a time

2. **Smart Environment Handling**
   - Detect and adapt to different environments (local development, CI/CD, GitHub integration)
   - Use appropriate environment variables and configurations per context
   - Avoid mocking environment-specific functionality unless absolutely necessary
   - Handle environment setup in fixtures, not in individual tests

3. **Test Setup and Configuration**
   - Centralize environment setup in fixtures and configuration
   - Use environment-specific test configurations
   - Maintain clear separation between test setup and test logic
   - Handle environment variables and file loading consistently

## Test Environment Setup

### Prerequisites
1. Python 3.11 or later installed
2. Git for version control
3. Access to GitHub repository

### Local Development Setup
1. Create a new virtual environment for testing:
   ```bash
   python -m venv .venv_test
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .venv_test\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv_test/bin/activate
     ```

3. Install test dependencies:
   ```bash
   pip install pytest pytest-cov pytest-mock
   ```

4. Install the project package in development mode:
   ```bash
   pip install -e .
   ```

### Configuration Files
1. `pytest.ini`: Contains pytest configuration
2. `.vscode/settings.json`: VS Code settings for test discovery
3. `.env.test`: Test environment variables (create from `.env.test.example`)

## Test Levels

### 1. Unit Tests
Located in `tests/unit/`:
- `github_utils/`: GitHub API interaction tests
- `openai_utils/`: OpenAI API interaction tests
- `prompts/`: Prompt generation tests

**Purpose**:
- Test individual components in isolation
- Verify internal logic and edge cases
- Ensure components work as expected without external dependencies
- Fast execution for quick feedback during development

**Characteristics**:
- Mock all external dependencies (GitHub, OpenAI)
- Focus on component-specific logic
- Test edge cases and error conditions
- Should be deterministic and fast

### 2. Integration Tests
Located in `tests/integration/`:
- `github_workflow/`: GitHub Actions workflow tests
- `openai_integration/`: OpenAI API integration tests

**Purpose**:
- Verify components work together correctly
- Test the complete flow of operations
- Ensure external interfaces behave as expected
- Validate business logic across components

**Characteristics**:
- Mock external services (GitHub, OpenAI) at the API level
- Test complete workflows
- Verify data flow between components
- Should reflect real-world usage patterns

### 3. End-to-End Tests
Located in `tests/e2e/`:
- `issue_analysis/`: Complete issue analysis workflow tests

## Known Issues and Solutions

### GitHub Utils Tests
1. `GithubClientFactory.create_client()` issues:
   - Error: Method takes no arguments but token is provided
   - Solution: Update the factory method to accept token parameter
   ```python
   @staticmethod
   def create_client(token: str, test_mode: bool = False) -> Github:
   ```

2. `IssueRetriever.get_recent_issues()` issues:
   - Error: Unexpected keyword argument 'days_back'
   - Solution: Update method signature to include the parameter
   ```python
   def get_recent_issues(self, days_back: int = 30, state: str = "open") -> List[Issue]:
   ```

3. `IssueSimilarityAnalyzer.compute_similarities()` issues:
   - Error: Unexpected keyword argument 'threshold'
   - Solution: Update method signature to include the parameter
   ```python
   def compute_similarities(self, target_issue: Issue, existing_issues: List[Issue], threshold: float = 0.8) -> List[Tuple[Issue, float]]:
   ```

### Test Coverage
Current coverage: 59%
Areas needing improvement:
1. `ai_doc_writer.py`: 0% coverage
2. `openai_utils.py`: 41% coverage
3. `prompts.py`: 42% coverage
4. `github_utils.py`: 66% coverage

## Running Tests

### Command Line
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=my_chat_gpt_utils

# Run specific test file
pytest tests/unit/github_utils/test_github_client.py

# Run tests with verbose output
pytest -v
```

### VS Code Test Explorer
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Python: Configure Tests"
3. Select "pytest" as test framework
4. Select "tests" directory as test location
5. Reload window if tests are not discovered

## Test Data Management

### Mock Data
- Located in `tests/fixtures/`
- Used for consistent test data across test runs
- Includes sample issues, responses, and configurations

### Environment Variables
Required for tests:
- `GITHUB_TOKEN`: GitHub API token
- `OPENAI_API_KEY`: OpenAI API key
- `TEST_MODE`: Set to "true" for test environment

## Best Practices

1. **Test Naming**
   - Use descriptive names
   - Follow pattern: `test_<functionality>_<scenario>`
   - Example: `test_analyze_issue_with_invalid_data`

2. **Test Organization**
   - Group related tests in classes
   - Use fixtures for common setup
   - Keep tests independent

3. **Mocking**
   - Mock external API calls
   - Use `unittest.mock` or `pytest-mock`
   - Document mock behavior

4. **Assertions**
   - Use specific assertions
   - Include meaningful error messages
   - Test edge cases

## Continuous Integration

### GitHub Actions
Tests run on:
- Pull requests
- Push to main branch
- Manual workflow dispatch

### Coverage Requirements
- Minimum coverage: 80%
- Coverage reports uploaded as artifacts
- Coverage badge updated on README.md

## Troubleshooting

### Common Issues
1. Test Discovery Failures
   - Ensure virtual environment is activated
   - Check Python interpreter path in VS Code
   - Verify pytest installation

2. Import Errors
   - Check PYTHONPATH
   - Verify package installation
   - Check for circular imports

3. Mock Issues
   - Verify mock setup
   - Check mock call counts
   - Ensure correct mock scope

### Debugging Tips
1. Use `pytest -v` for verbose output
2. Add `breakpoint()` in test code
3. Use VS Code debugger with pytest
4. Check test logs in `.pytest_cache/`

## Continuous Improvement

1. **Regular Review**
   - Review test coverage
   - Identify redundant tests
   - Update test strategy based on findings
   - Monitor environment-specific issues

2. **Documentation**
   - Keep test documentation up to date
   - Document environment requirements
   - Maintain clear setup instructions
   - Document environment-specific considerations

3. **Feedback Loop**
   - Gather feedback from developers
   - Update strategy based on team input
   - Regular strategy review meetings
   - Monitor environment-related issues 