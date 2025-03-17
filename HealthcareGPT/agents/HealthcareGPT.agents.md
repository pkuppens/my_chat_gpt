# AI Agents

This document details the AI agents that power the HealthcareGPT platform. For a high-level overview of the entire project, please refer to the [main project documentation](../HealthcareGPT.md).

## Overview
The AI agents system is the core intelligence layer of HealthcareGPT, responsible for:
- Adapting communication styles
- Managing medical terminology
- Ensuring security compliance
- Supporting development processes

## Directory Structure

### `prompts/`
Contains specialized prompts for different AI agents:
- Communication style adaptation prompts
- Medical terminology translation prompts
- Patient education prompts
- Peer communication prompts
- Code generation and review prompts

### `code/`
Contains the implementation of AI agents:
- Agent base classes and interfaces
- Specialized agent implementations
- Agent configuration and management
- Integration with the main application

## Agent Types

1. **Communication Agent**
   - Adapts medical communication based on user expertise
   - Handles multi-language translation
   - Manages medical terminology simplification

2. **Development Agent**
   - Assists in code generation and review
   - Helps maintain code quality and standards
   - Provides technical documentation

3. **Security Agent**
   - Ensures HIPAA compliance
   - Manages data privacy
   - Handles authentication and authorization

4. **Testing Agent**
   - Generates test cases
   - Validates code changes
   - Ensures system reliability

## Integration with Application
For details on how these agents integrate with the main application, see the [application documentation](../app/HealthcareGPT.app.md).

## Usage
[Documentation to be added]
