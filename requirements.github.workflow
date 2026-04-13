# Minimal runtime dependencies for GitHub Actions workflows (issue analyzer, duplicate detection).
# Install with: pip install -r requirements.github.workflow && pip install --no-deps -e .
# The second line installs the package without pulling the full pyproject dependency tree.
openai>=1.58.1,<2
PyGithub>=2.1.1
PyYAML>=6.0.1
requests>=2.31.0
scikit-learn>=1.3.0
packaging>=24.0
python-dotenv>=1.0.0
