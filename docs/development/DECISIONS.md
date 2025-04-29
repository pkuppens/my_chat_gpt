# Development Tool Decisions

## Package Management: UV

**Decision**: Use `uv` as the primary package manager for Python projects.

**Rationale**:

- Significantly faster than pip and poetry
- Built in Rust for better performance
- Modern features like advanced caching and lockfile support
- Maintains compatibility with existing tools
- Single tool for multiple package management needs

**References**:

- [Real Python UV Guide](https://realpython.com/python-uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)

## Linting: Ruff

**Decision**: Use `ruff` as the primary linter and formatter.

**Rationale**:

- 10-100x faster than traditional tools (flake8, black, isort)
- Single tool replaces multiple tools (flake8, black, isort)
- Better support for modern Python features
- Active development and maintenance
- Comprehensive rule set

**References**:

- [Real Python Ruff Guide](https://realpython.com/ruff-python/)
- [Ruff GitHub Repository](https://github.com/astral-sh/ruff)

## Implementation Notes

- Remove flake8 and black configurations
- Update pre-commit hooks to use ruff
- Update GitHub Actions to use uv and ruff
- Set Python 3.12 as default version
