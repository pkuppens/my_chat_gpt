---
description: Core principles for AI-assisted development
alwaysApply: true
---

# 🔑 Golden Rules for AI-Assisted Development

These rules define the core principles for working effectively with AI tools in the WBSO project. They are designed to ensure consistent, high-quality development practices.

## 1. Project Documentation

- Use markdown files for project management:
  - `README.md`: Project overview and setup
  - `PLANNING.md`: Development roadmap and architecture
  - `TASK.md`: Current task details and progress
- Keep documentation up-to-date as you develop
- Include examples and context in documentation

## 2. Code Organization

- Keep files under 500 lines
- Split large files into focused modules
- Use clear, descriptive file and module names
- Follow single responsibility principle

## 3. Conversation Management

- Start fresh conversations for new tasks
- Avoid long conversation threads
- One task per message
- Provide clear context and requirements

## 4. Testing Strategy

- Write tests for new functions immediately
- Include unit tests for all new features
- Test edge cases and error conditions
- Maintain high test coverage

## 5. Communication Guidelines

- Be specific in requests
- Provide examples when possible
- Include relevant context
- Reference existing code patterns

## 6. Documentation Practices

- Write documentation as you code
- Include docstrings for all functions
- Document design decisions
- Keep README.md current

## 7. Security Practices

- Never share API keys in code
- Use environment variables for secrets
- Implement security measures yourself
- Follow security best practices

## 8. Development Workflow

- Commit changes frequently
- Write clear commit messages
- Review code before committing
- Keep the codebase clean

## 9. Error Handling

- Implement proper error handling
- Use custom exceptions when needed
- Document error scenarios
- Provide clear error messages

## 10. Code Quality

- Follow PEP 8 guidelines
- Use type hints
- Write clean, readable code
- Keep functions focused

## Implementation Notes

These rules are automatically applied to all conversations in the project. They serve as a foundation for maintaining high-quality, maintainable code while working with AI tools.

### Rule Application

- These rules are always included in the model context
- They guide both code generation and review
- They ensure consistent development practices
- They help maintain project quality

### Best Practices

1. **When Starting a New Task**

   - Create a new conversation
   - Reference relevant documentation
   - Provide clear requirements
   - Include examples if possible

2. **During Development**

   - Write tests first
   - Document as you go
   - Keep files focused
   - Follow security practices

3. **When Reviewing Code**
   - Check against these rules
   - Verify documentation
   - Ensure proper testing
   - Validate security measures

## References

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules)
- [Python Documentation Guidelines](https://docs.python.org/3/docstring.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
