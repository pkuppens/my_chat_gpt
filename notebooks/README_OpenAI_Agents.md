# OpenAI Agent SDK with Guardrails - Proof of Concept

A production-ready, modular implementation of AI agents with swappable LLM providers and guardrails.

## Overview

This implementation demonstrates how to build a flexible agent system that follows SOLID principles and allows easy swapping of components. The design is inspired by the OpenAI Agents SDK with additional input/output guardrails for safety.

## Key Features

✅ **Swappable LLM Providers**
- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Ollama (local models like Llama 3.2)
- Easy to add new providers by implementing the `LLMProvider` interface

✅ **Swappable Guardrail Providers**
- OpenAI Moderation API
- Google Gemini
- Local rule-based guardrails
- Example: Use Gemini for guardrails on OpenAI prompts

✅ **Agent System**
- Create agents from SuperPrompt templates
- Tool support (file operations, custom tools)
- Agent-to-agent communication and delegation
- Meta-agents that can create other agents

✅ **Prompt Management**
- Load prompts from SuperPrompt library
- Compose multiple prompts together
- Reuse and combine prompt components

✅ **Safety Features**
- Input guardrails (check user input before processing)
- Output guardrails (validate agent responses)
- Multiple guardrail provider options

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                    Agent System                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Architect  │  │    Coder     │  │  Meta-Agent  │  │
│  │    Agent     │  │    Agent     │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
  ┌─────▼─────┐    ┌──────▼──────┐   ┌──────▼──────┐
  │ LLM       │    │ Guardrails  │   │   Tools     │
  │ Provider  │    │  Provider   │   │  Registry   │
  └───────────┘    └─────────────┘   └─────────────┘
        │                  │
  ┌─────┴─────┐    ┌──────┴──────┐
  │  OpenAI   │    │  OpenAI     │
  │  Ollama   │    │  Gemini     │
  │  Custom   │    │  Local      │
  └───────────┘    └─────────────┘
```

### Design Principles

1. **Abstraction**: Abstract base classes for extensibility
2. **Dependency Injection**: Components are injected, not hard-coded
3. **Single Responsibility**: Each class has one clear purpose
4. **Open/Closed**: Open for extension, closed for modification
5. **Liskov Substitution**: Providers are interchangeable

## Files

- **`my_chat_gpt_utils/agents_sdk.py`**: Core implementation
  - LLM providers (OpenAI, Ollama)
  - Guardrail providers (OpenAI, Gemini, Local)
  - Agent system with tool support
  - SuperPrompt loader
  - Tool registry

- **`notebooks/OpenAI_Agents_SDK_with_Guardrails.ipynb`**: Interactive examples
  - Setup and initialization
  - Creating agents from SuperPrompts
  - Multi-agent collaboration
  - Meta-agents creating other agents
  - Prompt composition
  - Guardrail testing
  - Component swapping demos

## Usage

### Basic Setup

```python
from my_chat_gpt_utils.agents_sdk import (
    OpenAIProvider,
    LocalGuardrailProvider,
    Agent,
    AgentConfig,
    ToolRegistry,
    SuperPromptLoader
)

# Initialize components
llm_provider = OpenAIProvider(model="gpt-4o-mini")
guardrail = LocalGuardrailProvider()
tool_registry = ToolRegistry()
prompt_loader = SuperPromptLoader()

# Create an agent from a SuperPrompt
config = AgentConfig(
    name="Architect",
    system_prompt=prompt_loader.load_prompt("software_architect_ai_prompt.txt"),
    tools=tool_registry.get_tool_definitions()
)

agent = Agent(
    config=config,
    llm_provider=llm_provider,
    tool_registry=tool_registry,
    input_guardrail=guardrail,
    output_guardrail=guardrail
)

# Use the agent
response = agent.run("Design a REST API for a todo app")
print(response)
```

### Swapping Components

```python
# Example 1: OpenAI LLM + Gemini Guardrails
agent1 = Agent(
    config=config,
    llm_provider=OpenAIProvider(),
    input_guardrail=GeminiGuardrailProvider(),
    output_guardrail=LocalGuardrailProvider()
)

# Example 2: Ollama LLM + OpenAI Guardrails
agent2 = Agent(
    config=config,
    llm_provider=OllamaProvider(model="llama3.2"),
    input_guardrail=OpenAIGuardrailProvider(),
    output_guardrail=OpenAIGuardrailProvider()
)

# Same interface, different implementations!
```

### Composing Prompts

```python
# Combine multiple SuperPrompts
composed_prompt = prompt_loader.compose_prompts(
    "3tier.md",
    "agentic_ai_framework_coder.md",
    "python-programmer-superprompt.md"
)

# Create a more capable agent
fullstack_config = AgentConfig(
    name="Full-Stack Developer",
    system_prompt=composed_prompt
)
```

### Multi-Agent Orchestration

```python
from my_chat_gpt_utils.agents_sdk import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Register multiple agents
orchestrator.register_agent("architect", architect_agent)
orchestrator.register_agent("coder", coder_agent)
orchestrator.register_agent("tester", tester_agent)

# Delegate tasks between agents
result = orchestrator.delegate_task(
    from_agent="architect",
    to_agent="coder",
    task="Implement the user authentication API"
)
```

## Examples in the Notebook

The Jupyter notebook demonstrates:

1. **Agent Creation**: Load SuperPrompts and create specialized agents
2. **Multi-Agent Collaboration**: Multiple agents working on different tasks
3. **Meta-Agents**: Agents that can create other agents
4. **Prompt Composition**: Combining multiple prompts for enhanced capabilities
5. **Guardrail Testing**: Validating different guardrail providers
6. **Component Swapping**: Demonstrating the flexibility of the architecture
7. **Tool Usage**: File operations and custom tools

## Requirements

### Core Dependencies
- Python 3.12+
- openai >= 1.58.1 (for OpenAI provider)
- ollama >= 0.4.5 (for Ollama provider, optional)
- google-generativeai (for Gemini guardrails, optional)

### Installation

```bash
# Install core dependencies (already in requirements.txt)
pip install openai ollama

# Optional: For Gemini guardrails
pip install google-generativeai
```

### Environment Variables

```bash
# Required for OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Optional for Gemini guardrails
export GOOGLE_API_KEY="your-google-api-key"
```

## Extending the System

### Adding a New LLM Provider

```python
from my_chat_gpt_utils.agents_sdk import LLMProvider, Message

class CustomLLMProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    def generate(self, messages: List[Message], **kwargs) -> Message:
        # Implement your LLM call here
        pass
    
    def generate_with_tools(self, messages: List[Message], 
                           tools: List[Dict], **kwargs) -> Message:
        # Implement tool calling support
        pass
```

### Adding a New Guardrail Provider

```python
from my_chat_gpt_utils.agents_sdk import GuardrailProvider, GuardrailResult

class CustomGuardrailProvider(GuardrailProvider):
    def check(self, content: str, context: Optional[str] = None) -> GuardrailResult:
        # Implement your guardrail logic
        passed = self._check_content(content)
        
        return GuardrailResult(
            passed=passed,
            message="Check completed",
            violations=[] if passed else ["custom_violation"]
        )
```

### Adding Custom Tools

```python
tool_registry = ToolRegistry()

tool_registry.register_tool(
    name="search_web",
    description="Search the web for information",
    function=lambda query: f"Search results for: {query}",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)
```

## Best Practices

1. **Use Lazy Initialization**: Providers initialize clients only when needed
2. **Abstract Interfaces**: Always code to interfaces, not implementations
3. **Dependency Injection**: Pass dependencies to constructors
4. **Error Handling**: Wrap API calls in try-except blocks
5. **Configuration**: Use environment variables for API keys
6. **Testing**: Test with different provider combinations
7. **Guardrails**: Always use both input and output guardrails

## Design Patterns Used

- **Strategy Pattern**: Swappable LLM and guardrail providers
- **Factory Pattern**: Agent creation and configuration
- **Registry Pattern**: Tool and agent registration
- **Template Method**: Agent execution flow
- **Decorator Pattern**: Guardrails wrap agent behavior
- **Facade Pattern**: Simplified interface for complex subsystems

## References

- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/guides/agents-sdk)
- [LinkedIn: AI Agents with Guardrails](https://www.linkedin.com/posts/liord_ai-agents-are-powerful-but-they-need-activity-7306348810824241152-xSAx)
- SuperPrompt library: `../SuperPrompt/`

## License

See LICENSE file in the repository root.

## Contributing

This is a proof of concept demonstrating architectural patterns for agent systems. Contributions that maintain the modularity and extensibility of the design are welcome.

## Future Enhancements

- [ ] Add streaming response support
- [ ] Implement agent state persistence
- [ ] Add more specialized tools
- [ ] Create web UI for agent interaction
- [ ] Add agent monitoring and observability
- [ ] Implement agent memory systems
- [ ] Add support for more LLM providers
- [ ] Create agent marketplace/template library
