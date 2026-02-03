"""
OpenAI Agent SDK with Guardrails - Modular Implementation

This module provides a well-designed, production-ready implementation of
agents with swappable LLM providers and guardrails.

Key Components:
- LLM Providers (OpenAI, Ollama)
- Guardrail Providers (OpenAI, Gemini, Local)
- Agent System with tool support
- SuperPrompt loader
- Tool registry
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import json
import os


# ============================================================================
# Core Data Models
# ============================================================================

@dataclass
class Message:
    """Represents a message in the conversation"""
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None


@dataclass
class GuardrailResult:
    """Result from a guardrail check"""
    passed: bool
    message: str = ""
    modified_content: Optional[str] = None
    violations: List[str] = field(default_factory=list)


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2000
    tools: List[Dict] = field(default_factory=list)


class GuardrailType(Enum):
    """Types of guardrails"""
    INPUT = "input"
    OUTPUT = "output"
    BOTH = "both"


# ============================================================================
# LLM Provider Interface
# ============================================================================

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, messages: List[Message], **kwargs) -> Message:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def generate_with_tools(self, messages: List[Message], tools: List[Dict], **kwargs) -> Message:
        """Generate a response with tool calling support"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
    def _ensure_client(self):
        """Lazy initialization of OpenAI client"""
        if self.client is None:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("openai package not installed. Install with: pip install openai")
    
    def generate(self, messages: List[Message], **kwargs) -> Message:
        """Generate response using OpenAI"""
        self._ensure_client()
        
        # Convert Message objects to dict format
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            **kwargs
        )
        
        return Message(
            role="assistant",
            content=response.choices[0].message.content
        )
    
    def generate_with_tools(self, messages: List[Message], tools: List[Dict], **kwargs) -> Message:
        """Generate response with tool calling"""
        self._ensure_client()
        
        formatted_messages = [
            {k: v for k, v in {
                "role": msg.role,
                "content": msg.content,
                "name": msg.name,
                "tool_calls": msg.tool_calls,
                "tool_call_id": msg.tool_call_id
            }.items() if v is not None}
            for msg in messages
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            tools=tools,
            **kwargs
        )
        
        choice = response.choices[0].message
        return Message(
            role="assistant",
            content=choice.content or "",
            tool_calls=[tc.model_dump() for tc in choice.tool_calls] if choice.tool_calls else None
        )


class OllamaProvider(LLMProvider):
    """Ollama local LLM Provider"""
    
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.client = None
    
    def _ensure_client(self):
        """Lazy initialization of Ollama client"""
        if self.client is None:
            try:
                import ollama
                self.client = ollama.Client(host=self.base_url)
            except ImportError:
                raise ImportError("ollama package not installed. Install with: pip install ollama")
    
    def generate(self, messages: List[Message], **kwargs) -> Message:
        """Generate response using Ollama"""
        self._ensure_client()
        
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = self.client.chat(
            model=self.model,
            messages=formatted_messages,
            **kwargs
        )
        
        return Message(
            role="assistant",
            content=response['message']['content']
        )
    
    def generate_with_tools(self, messages: List[Message], tools: List[Dict], **kwargs) -> Message:
        """Generate response with tool calling (Ollama has limited support)"""
        self._ensure_client()
        
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        response = self.client.chat(
            model=self.model,
            messages=formatted_messages,
            tools=tools,
            **kwargs
        )
        
        message_dict = response['message']
        return Message(
            role="assistant",
            content=message_dict.get('content', ''),
            tool_calls=message_dict.get('tool_calls')
        )


# ============================================================================
# Guardrail Provider Interface
# ============================================================================

class GuardrailProvider(ABC):
    """Abstract base class for guardrail providers"""
    
    @abstractmethod
    def check(self, content: str, context: Optional[str] = None) -> GuardrailResult:
        """Check content against guardrails"""
        pass


class OpenAIGuardrailProvider(GuardrailProvider):
    """OpenAI-based guardrail checking using moderation API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
    
    def _ensure_client(self):
        if self.client is None:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("openai package not installed")
    
    def check(self, content: str, context: Optional[str] = None) -> GuardrailResult:
        """Check content using OpenAI moderation"""
        self._ensure_client()
        
        try:
            response = self.client.moderations.create(input=content)
            result = response.results[0]
            
            if result.flagged:
                violations = [cat for cat, val in result.categories.model_dump().items() if val]
                return GuardrailResult(
                    passed=False,
                    message=f"Content flagged for: {', '.join(violations)}",
                    violations=violations
                )
            
            return GuardrailResult(passed=True, message="Content passed moderation")
        except Exception as e:
            return GuardrailResult(passed=False, message=f"Moderation check failed: {str(e)}")


class GeminiGuardrailProvider(GuardrailProvider):
    """Gemini-based guardrail checking"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.client = None
    
    def _ensure_client(self):
        if self.client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel('gemini-pro')
            except ImportError:
                raise ImportError("google-generativeai package not installed")
    
    def check(self, content: str, context: Optional[str] = None) -> GuardrailResult:
        """Check content using Gemini"""
        self._ensure_client()
        
        try:
            prompt = f"""
            Analyze the following content for safety and appropriateness.
            Report any issues with:
            - Harmful content
            - Inappropriate language
            - Sensitive information
            - Privacy violations
            
            Content: {content}
            
            Respond with JSON: {{"safe": true/false, "issues": [list of issues]}}
            """
            
            response = self.client.generate_content(prompt)
            result_text = response.text
            
            # Simple heuristic check
            if '"safe": true' in result_text or '"safe":true' in result_text:
                return GuardrailResult(passed=True, message="Content passed Gemini checks")
            else:
                return GuardrailResult(
                    passed=False,
                    message="Content flagged by Gemini",
                    violations=["gemini_flagged"]
                )
        except Exception as e:
            return GuardrailResult(passed=False, message=f"Gemini check failed: {str(e)}")


class LocalGuardrailProvider(GuardrailProvider):
    """Local rule-based guardrail checking"""
    
    def __init__(self, rules: Optional[List[Callable[[str], bool]]] = None):
        self.rules = rules or self._default_rules()
    
    def _default_rules(self) -> List[Callable[[str], bool]]:
        """Default local guardrail rules"""
        return [
            lambda text: len(text) < 10000,  # Max length
            lambda text: not any(word in text.lower() for word in ['hack', 'exploit', 'bypass']),
        ]
    
    def check(self, content: str, context: Optional[str] = None) -> GuardrailResult:
        """Check content using local rules"""
        violations = []
        
        if len(content) > 10000:
            violations.append("content_too_long")
        
        # Check for sensitive keywords
        sensitive_words = ['password', 'secret', 'api_key', 'token']
        found_sensitive = [word for word in sensitive_words if word in content.lower()]
        if found_sensitive:
            violations.append(f"sensitive_keywords: {', '.join(found_sensitive)}")
        
        if violations:
            return GuardrailResult(
                passed=False,
                message=f"Local guardrail violations: {', '.join(violations)}",
                violations=violations
            )
        
        return GuardrailResult(passed=True, message="Content passed local checks")


# ============================================================================
# SuperPrompt Loader
# ============================================================================

class SuperPromptLoader:
    """Load and manage SuperPrompt templates"""
    
    def __init__(self, prompts_dir: str = None):
        if prompts_dir is None:
            # Default to SuperPrompt directory relative to this file
            base_dir = Path(__file__).parent.parent
            prompts_dir = base_dir / "SuperPrompt"
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}
    
    def load_prompt(self, filename: str) -> str:
        """Load a prompt from file"""
        if filename in self._cache:
            return self._cache[filename]
        
        filepath = self.prompts_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Prompt file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._cache[filename] = content
        return content
    
    def list_prompts(self) -> List[str]:
        """List all available prompts"""
        if not self.prompts_dir.exists():
            return []
        return [f.name for f in self.prompts_dir.iterdir() if f.is_file()]
    
    def compose_prompts(self, *filenames: str, separator: str = "\n\n---\n\n") -> str:
        """Compose multiple prompts together"""
        prompts = [self.load_prompt(f) for f in filenames]
        return separator.join(prompts)
    
    def create_agent_config(self, name: str, prompt_file: str, **kwargs) -> AgentConfig:
        """Create an agent configuration from a prompt file"""
        system_prompt = self.load_prompt(prompt_file)
        return AgentConfig(name=name, system_prompt=system_prompt, **kwargs)


# ============================================================================
# Tool System
# ============================================================================

class ToolRegistry:
    """Registry for agent tools"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_definitions: List[Dict] = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        self.register_tool(
            name="save_file",
            description="Save content to a file",
            function=self._save_file,
            parameters={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to save"},
                    "content": {"type": "string", "description": "The content to save"}
                },
                "required": ["filename", "content"]
            }
        )
        
        self.register_tool(
            name="read_file",
            description="Read content from a file",
            function=self._read_file,
            parameters={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The name of the file to read"}
                },
                "required": ["filename"]
            }
        )
    
    def register_tool(self, name: str, description: str, function: Callable, parameters: Dict):
        """Register a new tool"""
        self.tools[name] = function
        self.tool_definitions.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
    
    def _save_file(self, filename: str, content: str) -> str:
        """Save content to file"""
        try:
            output_dir = Path("/tmp/agent_outputs")
            output_dir.mkdir(exist_ok=True)
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully saved to {filepath}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
    
    def _read_file(self, filename: str) -> str:
        """Read content from file"""
        try:
            output_dir = Path("/tmp/agent_outputs")
            filepath = output_dir / filename
            
            if not filepath.exists():
                return f"File not found: {filepath}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name"""
        if tool_name not in self.tools:
            return f"Tool not found: {tool_name}"
        
        try:
            result = self.tools[tool_name](**arguments)
            return str(result)
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"
    
    def get_tool_definitions(self) -> List[Dict]:
        """Get all tool definitions for LLM"""
        return self.tool_definitions


# ============================================================================
# Agent System
# ============================================================================

class Agent:
    """An AI agent with guardrails and tool support"""
    
    def __init__(
        self,
        config: AgentConfig,
        llm_provider: LLMProvider,
        tool_registry: Optional[ToolRegistry] = None,
        input_guardrail: Optional[GuardrailProvider] = None,
        output_guardrail: Optional[GuardrailProvider] = None
    ):
        self.config = config
        self.llm_provider = llm_provider
        self.tool_registry = tool_registry or ToolRegistry()
        self.input_guardrail = input_guardrail
        self.output_guardrail = output_guardrail
        self.conversation_history: List[Message] = []
        
        # Initialize with system prompt
        self.conversation_history.append(
            Message(role="system", content=config.system_prompt)
        )
    
    def _check_input_guardrails(self, content: str) -> GuardrailResult:
        """Check input against guardrails"""
        if self.input_guardrail:
            return self.input_guardrail.check(content)
        return GuardrailResult(passed=True, message="No input guardrails configured")
    
    def _check_output_guardrails(self, content: str) -> GuardrailResult:
        """Check output against guardrails"""
        if self.output_guardrail:
            return self.output_guardrail.check(content)
        return GuardrailResult(passed=True, message="No output guardrails configured")
    
    def run(self, user_message: str, max_iterations: int = 5) -> str:
        """Run the agent with a user message"""
        # Check input guardrails
        input_check = self._check_input_guardrails(user_message)
        if not input_check.passed:
            return f"Input guardrail violation: {input_check.message}"
        
        # Add user message to history
        self.conversation_history.append(
            Message(role="user", content=user_message)
        )
        
        # Agent loop with tool calling
        for iteration in range(max_iterations):
            # Get response from LLM
            if self.config.tools:
                response = self.llm_provider.generate_with_tools(
                    self.conversation_history,
                    tools=self.config.tools,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
            else:
                response = self.llm_provider.generate(
                    self.conversation_history,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
            
            self.conversation_history.append(response)
            
            # Check if there are tool calls
            if response.tool_calls:
                # Execute tools
                for tool_call in response.tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = json.loads(tool_call['function']['arguments'])
                    
                    # Execute the tool
                    tool_result = self.tool_registry.execute_tool(tool_name, tool_args)
                    
                    # Add tool result to history
                    self.conversation_history.append(
                        Message(
                            role="tool",
                            content=tool_result,
                            tool_call_id=tool_call['id'],
                            name=tool_name
                        )
                    )
                
                # Continue loop to get final response
                continue
            
            # No more tool calls, check output and return
            if response.content:
                output_check = self._check_output_guardrails(response.content)
                if not output_check.passed:
                    return f"Output guardrail violation: {output_check.message}"
                
                return response.content
        
        return "Max iterations reached without final response"
    
    def reset(self):
        """Reset conversation history"""
        self.conversation_history = [
            Message(role="system", content=self.config.system_prompt)
        ]


class AgentOrchestrator:
    """Orchestrate multiple agents"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
    
    def register_agent(self, name: str, agent: Agent):
        """Register an agent"""
        self.agents[name] = agent
    
    def create_agent(
        self,
        name: str,
        config: AgentConfig,
        llm_provider: LLMProvider,
        tool_registry: Optional[ToolRegistry] = None,
        input_guardrail: Optional[GuardrailProvider] = None,
        output_guardrail: Optional[GuardrailProvider] = None
    ) -> Agent:
        """Create and register a new agent"""
        agent = Agent(
            config=config,
            llm_provider=llm_provider,
            tool_registry=tool_registry,
            input_guardrail=input_guardrail,
            output_guardrail=output_guardrail
        )
        self.register_agent(name, agent)
        return agent
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def delegate_task(self, from_agent: str, to_agent: str, task: str) -> str:
        """Delegate a task from one agent to another"""
        target_agent = self.get_agent(to_agent)
        if not target_agent:
            return f"Agent {to_agent} not found"
        
        return target_agent.run(task)
