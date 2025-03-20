# Testing Strategy

This document outlines the testing strategy for the MyChatGPT project, including core principles, test levels, and implementation guidelines.

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

## Test Levels

### 1. Unit Tests
Located in `tests/my_chat_gpt_utils/`

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

**Example Components**:
- GitHub client configuration
- Issue analysis logic
- Label management
- Response formatting

### 2. Integration Tests
Located in `tests/integration/`

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

**Example Flows**:
- Issue analysis workflow:
  1. Get GitHub issue
  2. Analyze with OpenAI
  3. Update GitHub with tags and comments
- Label management workflow
- Response formatting and posting

## Environment Handling

### Environment Detection
- Detect environment type (local, CI/CD, GitHub integration)
- Use appropriate configuration based on environment
- Avoid hardcoding environment-specific values
- Provide clear fallbacks for missing environment variables

### Environment Variables
- Use `.env` files for local development
- Use GitHub Actions secrets for CI/CD
- Use environment variables for runtime configuration
- Mock environment variables consistently in tests

## Test Validation

### What to Test
- Required functionality and interfaces
- Business logic and behavior
- Error handling and edge cases
- Integration points between components
- Environment-specific behavior

### What Not to Test
- Implementation details
- Internal state unless critical
- Framework-specific behavior
- Mock object comparisons
- Environment setup mechanics

## Test Structure

### Setup
```python
@pytest.fixture(scope="session")
def test_environment():
    """Configure test environment based on context."""
    env_type = detect_environment_type()
    return configure_test_environment(env_type)

@pytest.fixture
def github_client(test_environment):
    """Create GitHub client with appropriate configuration."""
    return create_github_client(test_environment)
```

### Test Cases
```python
def test_github_client_functionality(github_client):
    """Test required GitHub client functionality."""
    # Test business logic
    assert github_client.can_access_repository("owner/repo")
    assert github_client.can_create_issue()

    # Test error handling
    with pytest.raises(ValueError):
        github_client.create_issue("invalid/repo", "title", "body")
```

## Best Practices

1. **Environment Configuration**
   - Use environment-specific configuration files
   - Centralize environment setup
   - Avoid environment-specific code in tests
   - Handle missing environment variables gracefully

2. **Test Validation**
   - Focus on behavior and functionality
   - Use appropriate assertions
   - Avoid implementation-specific checks
   - Test error handling comprehensively
   - One concept per test
   - Clear, descriptive assertions

3. **Mock Usage**
   - Mock external dependencies only
   - Avoid mocking internal functionality
   - Use appropriate mock levels (function, class, module)
   - Mock environment consistently

4. **Test Organization**
   - Group related tests
   - Use descriptive test names
   - Maintain clear test structure
   - Separate environment setup from test logic
   - Follow AAA pattern (Arrange, Act, Assert)

5. **Test Independence**
   - Each test should be independent
   - No test should depend on another test's state
   - Use fixtures for common setup

6. **Performance**
   - Keep tests fast
   - Minimize external dependencies
   - Use appropriate mocking levels
   - Consider test parallelization

## Running Tests

### 1. Running All Tests
```bash
pytest -v
```

### 2. Running Specific Test Levels
```bash
# Unit tests only
pytest tests/my_chat_gpt_utils/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/integration/test_analyze_issue_integration.py -v
```

### 3. Test Coverage Report
```bash
pytest --cov=my_chat_gpt_utils tests/
```

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

## Troubleshooting

1. **Failing Tests**
   - Check test isolation
   - Verify mock setup
   - Review test data
   - Check for race conditions

2. **Slow Tests**
   - Review mocking strategy
   - Check for unnecessary setup
   - Optimize test data
   - Consider test parallelization

3. **Flaky Tests**
   - Review timing dependencies
   - Check for state leakage
   - Verify cleanup procedures
   - Consider test stability improvements
