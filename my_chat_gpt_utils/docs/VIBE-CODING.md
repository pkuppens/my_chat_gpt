# Vibe Coding Overview

Vibe coding is an AI-assisted coding technique where developers instruct AI models using natural
language prompts. These prompts guide the AI in generating, modifying, debugging, or optimizing code.
This method shifts developer roles toward guiding, reviewing, and refining generated code, improving
productivity and efficiency.

## Best Practices for Guiding AI Coding

1. **Clarity and Precision**
   Clearly describe what you need. Specify behavior, inputs, outputs, and constraints explicitly.

2. **Incremental Development**
   Break complex problems into smaller, simpler steps or requests. Incremental refinement leads to
   accurate outcomes.

3. **Contextual Guidance**
   Provide relevant code or context when asking for enhancements or debugging help.

4. **Structured Prompts**
   Structure your requests clearly, highlighting important details such as performance requirements,
   readability, or code quality.

5. **Explicit Documentation Requests**
   Request clear comments or documentation to ensure generated code is maintainable and easy to modify
   later.

## Example Prompts and Rationale

Prompt Example 1:

    Prompt: Write a well-documented Python function to calculate Fibonacci numbers with caching, using
    simple, well-explained steps.

    Rationale: Asking explicitly for documentation and simplicity ensures that the AI generates clear,
    maintainable, and production-quality code. It simplifies debugging and future modifications.

Prompt Example 2:

    Prompt: Create a small React component to display user profiles, using functional components and
    clear inline comments to explain props and state.

    Rationale: Clearly requesting inline comments and functional React components ensures clean,
    modern, and understandable frontend code. It enhances readability and maintainability.

Prompt Example 3:

    Prompt: Generate a SQL query to fetch the latest five orders from a database table named
    'customer_orders', including comments explaining each query step clearly.

    Rationale: Explicitly asking for step-by-step comments and clarity ensures generated SQL is easy
    to debug, modify, and validate against business logic.

Prompt Example 4:

    Prompt: Provide a GitHub Actions workflow YAML file that runs automated unit tests for a Python
    project upon every commit to the main branch, with explanatory comments.

    Rationale: Asking for explanatory comments helps ensure clarity around each action step, making
    future adjustments straightforward and reducing potential confusion.

Prompt Example 5:

    Prompt: Create markdown-formatted project documentation for setup instructions, clearly structured
    with numbered steps and brief explanations.

    Rationale: Explicit structuring and simplicity requests help create effective and clear
    documentation that facilitates smooth onboarding and ongoing project management.

## Cursor IDE Features

Cursor is a powerful AI-enhanced IDE that provides advanced features for vibe coding. Here are some
key features and how to use them effectively:

### Documentation Integration

Cursor allows you to reference documentation directly in your prompts using @ tags:

1. **Local Documentation References**
   ```
   @file:path/to/file.md
   @function:functionName
   @class:ClassName
   ```

2. **Remote Documentation**
   ```
   @url:https://docs.example.com/api
   @github:username/repo/path/to/file
   ```

### Smart Code Navigation

- Use `@file` to navigate to specific files
- Use `@function` to jump to function definitions
- Use `@class` to locate class implementations

### AI-Assisted Features

1. **Code Generation**
   - Generate boilerplate code
   - Create test cases
   - Implement interfaces

2. **Code Refactoring**
   - Suggest improvements
   - Optimize performance
   - Enhance readability

3. **Debugging Assistance**
   - Identify potential issues
   - Suggest fixes
   - Explain error messages

### Best Practices for Cursor

1. **Context-Aware Prompts**
   - Reference specific files or functions using @ tags
   - Provide relevant code snippets
   - Specify the programming language and framework

2. **Iterative Development**
   - Use Cursor's AI to refine code incrementally
   - Leverage the built-in code review capabilities
   - Take advantage of automatic documentation generation

3. **Integration with Version Control**
   - Generate commit messages
   - Review changes
   - Create pull request descriptions

Use these structured approaches to maximize efficiency and maintainability when using vibe coding
techniques with Cursor.
