# Test Strategy

## Overview
This document outlines the testing strategy for the MyChatGPT project, including unit tests, integration tests, and end-to-end tests.

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

## Test Structure

### Unit Tests
Located in `tests/unit/`:
- `github_utils/`: GitHub API interaction tests
- `openai_utils/`: OpenAI API interaction tests
- `prompts/`: Prompt generation tests

### Integration Tests
Located in `tests/integration/`:
- `github_workflow/`: GitHub Actions workflow tests
- `openai_integration/`: OpenAI API integration tests

### End-to-End Tests
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

## Best Practices

1. Test Naming
   - Use descriptive names
   - Follow pattern: `test_<functionality>_<scenario>`
   - Example: `test_analyze_issue_with_invalid_data`

2. Test Organization
   - Group related tests in classes
   - Use fixtures for common setup
   - Keep tests independent

3. Mocking
   - Mock external API calls
   - Use `unittest.mock` or `pytest-mock`
   - Document mock behavior

4. Assertions
   - Use specific assertions
   - Include meaningful error messages
   - Test edge cases

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