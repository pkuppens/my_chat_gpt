#!/usr/bin/env python3
"""
Quick Start Example for OpenAI Agents SDK with Guardrails

This script demonstrates the key features of the agent system.
Run this to see a simple example without needing a full Jupyter notebook.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from my_chat_gpt_utils.agents_sdk import (
    OpenAIProvider,
    OllamaProvider,
    LocalGuardrailProvider,
    OpenAIGuardrailProvider,
    Agent,
    AgentConfig,
    AgentOrchestrator,
    SuperPromptLoader,
    ToolRegistry,
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print_section("OpenAI Agents SDK with Guardrails - Quick Start")
    
    # Step 1: Initialize components
    print("\n1. Initializing components...")
    
    # Try to use OpenAI, fallback to Ollama
    llm_provider = None
    try:
        openai_provider = OpenAIProvider(model="gpt-4o-mini")
        llm_provider = openai_provider
        print("   ✓ Using OpenAI provider")
    except Exception as e:
        print(f"   ⚠ OpenAI not available: {e}")
        try:
            ollama_provider = OllamaProvider(model="llama3.2")
            llm_provider = ollama_provider
            print("   ✓ Using Ollama provider")
        except Exception as e:
            print(f"   ⚠ Ollama not available: {e}")
    
    if not llm_provider:
        print("\n❌ No LLM provider available. Please configure:")
        print("   - OpenAI: Set OPENAI_API_KEY environment variable")
        print("   - Ollama: Install and run Ollama locally")
        return
    
    # Initialize guardrails
    guardrail = LocalGuardrailProvider()
    try:
        # Test if OpenAI guardrails work
        test_guardrail = OpenAIGuardrailProvider()
        test_guardrail.check("test")
        guardrail = test_guardrail
        print("   ✓ Using OpenAI guardrails")
    except Exception:
        print("   ✓ Using local guardrails")
    
    prompt_loader = SuperPromptLoader()
    tool_registry = ToolRegistry()
    orchestrator = AgentOrchestrator()
    
    print("   ✓ All components initialized")
    
    # Step 2: Test guardrails
    print_section("2. Testing Guardrails")
    
    test_cases = [
        ("Hello world", "Safe content"),
        ("My password is secret123", "Content with sensitive keywords"),
    ]
    
    for content, description in test_cases:
        result = guardrail.check(content)
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"   {status}: {description}")
        if not result.passed:
            print(f"      Violations: {', '.join(result.violations)}")
    
    # Step 3: Create a simple agent
    print_section("3. Creating a Simple Agent")
    
    simple_config = AgentConfig(
        name="Assistant",
        system_prompt="You are a helpful AI assistant. Be concise and clear.",
        temperature=0.7,
        tools=tool_registry.get_tool_definitions()
    )
    
    agent = orchestrator.create_agent(
        name="assistant",
        config=simple_config,
        llm_provider=llm_provider,
        tool_registry=tool_registry,
        input_guardrail=guardrail,
        output_guardrail=guardrail
    )
    
    print(f"   ✓ Created agent: {simple_config.name}")
    print(f"     - LLM: {llm_provider.__class__.__name__}")
    print(f"     - Guardrails: {guardrail.__class__.__name__}")
    print(f"     - Tools: {len(tool_registry.get_tool_definitions())}")
    
    # Step 4: Test the agent
    print_section("4. Testing Agent")
    
    print("\n   Query: 'Explain what an API is in one sentence.'")
    print("   Response:")
    
    try:
        response = agent.run("Explain what an API is in one sentence.")
        print(f"   {response}")
    except Exception as e:
        print(f"   ⚠ Error: {e}")
    
    # Step 5: Load SuperPrompt
    print_section("5. Loading SuperPrompts")
    
    prompts = prompt_loader.list_prompts()
    print(f"   Found {len(prompts)} SuperPrompts:")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"   {i}. {prompt}")
    if len(prompts) > 5:
        print(f"   ... and {len(prompts) - 5} more")
    
    # Step 6: Component swapping demo
    print_section("6. Demonstrating Component Swapping")
    
    print("\n   Creating same agent with different configurations:")
    
    configs_created = []
    
    # Config 1: Try OpenAI + OpenAI guardrails
    try:
        if isinstance(llm_provider, OpenAIProvider):
            agent1 = Agent(
                config=simple_config,
                llm_provider=OpenAIProvider(),
                input_guardrail=OpenAIGuardrailProvider(),
                output_guardrail=LocalGuardrailProvider()
            )
            configs_created.append("OpenAI LLM + OpenAI Input + Local Output")
    except Exception:
        pass
    
    # Config 2: Local guardrails
    agent2 = Agent(
        config=simple_config,
        llm_provider=llm_provider,
        input_guardrail=LocalGuardrailProvider(),
        output_guardrail=LocalGuardrailProvider()
    )
    configs_created.append(f"{llm_provider.__class__.__name__} + Local Guardrails")
    
    for i, config in enumerate(configs_created, 1):
        print(f"   ✓ Config {i}: {config}")
    
    print("\n   All configurations use the same Agent interface!")
    print("   This demonstrates abstraction and swappability.")
    
    # Summary
    print_section("Summary")
    print("""
   ✓ Successfully demonstrated:
     - Swappable LLM providers
     - Swappable guardrail providers  
     - Agent creation and execution
     - SuperPrompt loading
     - Component abstraction
   
   Next Steps:
     - Open the Jupyter notebook for interactive examples
     - Try different LLM and guardrail combinations
     - Create agents from SuperPrompt templates
     - Build multi-agent systems
     - Add custom tools and guardrails
   
   See: notebooks/OpenAI_Agents_SDK_with_Guardrails.ipynb
   """)


if __name__ == "__main__":
    main()
