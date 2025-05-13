# Cursor Rules for WBSO Project

This document outlines the Cursor rules and best practices for the WBSO AI Agent project. It combines official Cursor guidelines with project-specific recommendations.

## Official Cursor Rules

For the complete official Cursor rules documentation, visit: [Cursor Rules Documentation](https://docs.cursor.com/context/rules)

## Project Rules Structure

The WBSO project uses Cursor rules to maintain consistent coding standards and best practices. The rules are stored in the `.cursor/rules` directory and are automatically applied based on their configuration.

### Rule Types

1. **Project-wide Rules** (`project-standards.mdc`)

   - Applied to all files in the project
   - Defines general project standards
   - Includes documentation, version control, and workflow guidelines

2. **Language-specific Rules** (`python-standards.mdc`)
   - Applied to Python files only
   - Defines Python-specific coding standards
   - Includes module structure, documentation, and testing guidelines

### How Rules Are Applied

1. **Automatic Application**

   - Rules are automatically applied based on file patterns
   - Project-wide rules apply to all files
   - Language-specific rules apply to matching file types

2. **Rule Priority**

   - More specific rules take precedence over general rules
   - Language-specific rules override project-wide rules for matching files

3. **Rule Updates**
   - Rules can be updated by modifying the MDC files
   - Changes take effect immediately
   - All team members should be notified of rule changes

## Rule Categories

### Project Standards

- Project structure and organization
- Documentation requirements
- Version control practices
- Development workflow
- Code quality standards
- Security guidelines
- Performance requirements
- Accessibility standards
- Internationalization support

### Python Standards

- Module structure and imports
- Documentation format
- Error handling patterns
- Testing requirements
- Configuration management
- Type hints usage
- Code organization
- Best practices

## Using Rules

1. **Development**

   - Follow the rules when writing new code
   - Use the rules as a reference for code reviews
   - Apply rules consistently across the project

2. **Code Review**

   - Check for rule compliance
   - Suggest improvements based on rules
   - Document rule exceptions when necessary

3. **Maintenance**
   - Keep rules up to date
   - Remove outdated rules
   - Add new rules as needed

## References

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules)
- [Python Documentation Guidelines](https://docs.python.org/3/docstring.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
