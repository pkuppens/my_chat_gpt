# Test Strategy

## Test Environment Setup

### Cursor Test Explorer Configuration

To set up the test explorer in Cursor:

1. Ensure you have Python 3.11 or later installed:
   ```bash
   python --version
   ```

2. Create a new virtual environment for testing:
   ```bash
   python -m venv .venv_test
   ```

3. Activate the virtual environment:
   - Windows: `.venv_test\Scripts\activate`
   - Unix/MacOS: `source .venv_test/bin/activate`

4. Install test dependencies:
   ```bash
   pip install pytest pytest-cov pytest-mock
   ```

5. The repository includes configuration files:
   - `pytest.ini`: Configures pytest behavior
   - `.vscode/settings.json`: Configures Cursor's Python test explorer

6. If the test explorer doesn't detect tests:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Python: Configure Tests"
   - Select "pytest" as the test framework
   - Select the "tests" directory as the test location

7. Reload the Cursor window:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Developer: Reload Window"

The test explorer should now show all tests in the project. You can run tests by:
- Clicking the "Run Test" button above a test function
- Using the test explorer panel to run individual tests or test suites
- Using the command palette to run all tests

Note: This project uses a separate virtual environment (`.venv_test`) for testing to avoid conflicts with the main project dependencies. The main project dependencies are managed by `uv` in the `.venv` directory.

The test explorer should now show all tests in the project. You can run tests by:
- Clicking the "Run Test" button above a test function
- Using the test explorer panel to run individual tests or test suites
- Using the command palette to run all tests 