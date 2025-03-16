# **Enhanced Superprompt: Production-Ready Python Code Generation**

## **Initial Requirements Analysis Phase**

### **1. Requirements Evaluation and Validation**
- **Analyze requirements** for completeness, correctness, and clarity
- **Identify contradictions** or mutually exclusive requirements
- **Flag ambiguities** requiring further clarification
- **Check feasibility** within technical constraints
- **Determine potential edge cases** not explicitly covered
- **Provide recommendations** for refining unclear specifications
- **Continue only when** requirements are clear and feasible

---

## **Core Objective**
Generate Python code that is **production-ready**, **fully documented**, **robust**, and **maintainable** based on user requirements, stories, or technical specifications.

---

## **Coding Standards & Best Practices**

### **1. Production-Grade Code**
- **Complete functionality** with comprehensive **error handling** for all edge cases
- **Defensive programming** techniques to prevent runtime failures
- **Proper logging** with appropriate severity levels
- **Performance optimization** considerations where relevant
- **Resource management** (file handles, network connections, etc.)

### **2. Documentation Excellence**
- **Rich docstrings** in **Google-style format**
- **Practical doctest examples** demonstrating real-world usage
- **Inline comments** only for complex logic, not obvious operations
- **Module-level documentation** explaining the purpose and relationships
- **Architecture diagrams** for complex systems (ASCII or link to external tool)

### **3. Code Quality**
- **Full PEP 8 compliance** with **132 character line length** maximum
- **Consistent naming conventions** following Python standards
- **Type hinting** for all function signatures and variables
- **Static type checking** readiness (mypy compatible)
- **Dead code elimination** and **code duplication avoidance**

### **4. Type System**
- **Comprehensive type annotations** using the `typing` module
- **Union types** for multiple possible return types
- **Generic types** for flexible container implementations
- **Protocol classes** for duck typing where appropriate
- **TypedDict** for dictionary structures with known keys
- **Literal types** for constrained string/numeric values

### **5. Software Architecture**
- **SOLID principles** application throughout the codebase
- **Design patterns** implementation where appropriate
- **Dependency injection** for flexible component coupling
- **Interface segregation** with clear boundaries
- **Command-query separation** for predictable behavior

### **6. Error Handling & Resilience**
- **Custom exception hierarchies** for domain-specific errors
- **Graceful degradation** strategies for external dependencies
- **Retry mechanisms** with exponential backoff for transient failures
- **Circuit breakers** for failing fast when systems are unavailable
- **Detailed error messages** that aid troubleshooting

### **7. Library Selection & Usage**
- **Standard library preference** when functionality is available
- **Widely-adopted packages** for specialized needs
- **Explicit version pinning** in requirements.txt
- **Minimal dependencies** to reduce vulnerability surface
- **Feature detection** over version checking

### **8. Project Structure**
- **Clear separation of concerns** between modules
- **Consistent import organization** (standard library, third-party, local)
- **Package-based organization** for related functionality
- **Configuration management** separated from business logic
- **Suggested directory structure** for complete implementations

### **9. Testing Strategy**
- **Pytest fixtures** for test setup and teardown
- **Parameterized tests** for multiple input scenarios
- **Property-based testing** for complex input spaces
- **Mock objects** for external dependencies
- **Integration tests** for critical system boundaries
- **Coverage metrics** for test quality evaluation

### **10. Security Considerations**
- **Input validation** for all external data
- **Output encoding** to prevent injection attacks
- **Secrets management** best practices
- **Safe cryptographic implementations**
- **Regular dependency scanning** recommendations

### **11. Educational Considerations**
- **Explain complex patterns** with analogies and examples
- **Define advanced concepts** like Circuit Breakers and Mocks in comments
- **Provide implementation rationale** for non-obvious design decisions
- **Include references** to design patterns and principles used
- **Comment code at appropriate difficulty level** for junior/intermediate developers (B2 English + technical jargon)

---

## **Implementation Example: JMESPath Context Substitution**

### **Requirements Analysis:**

Before implementing the JMESPath-based context replacement utility, let's analyze the requirements:

**Requirements Review:**
1. **Fill JSON specification with values from context dictionary** - Clear and feasible
2. **Replace JMESPath placeholders with actual values** - Well-defined task
3. **Leave placeholders unchanged if values not found** - Edge case handled
4. **Support nested queries and arrays** - Specific functionality requirement

**Potential Issues:**
- **Mutability concerns** - Need to ensure we don't modify input dictionaries during processing
- **Type safety** - JMESPath queries might return unexpected types requiring careful handling
- **Deep copying overhead** - Performance implications of copying nested structures
- **Recursive structures** - Potential for infinite recursion with circular references

**Resolution Strategy:**
- Implement with immutable approach using deep copies to prevent modifying inputs
- Add comprehensive type annotations and runtime type checking
- Handle edge cases explicitly with detailed documentation
- Include safeguards against excessive recursion depth

### **Implementation with Explanations:**

```python
# FILE: utilities/json_context_resolver.py

"""
Utility module for resolving JMESPath expressions in JSON structures using context data.

This module provides functionality to replace placeholders in JSON structures with
actual values from a context dictionary, supporting nested paths, arrays, and wildcards.

Examples:
    >>> from utilities.json_context_resolver import resolve_json_placeholders
    >>> spec = {"name": "{user.name}", "orders": "{orders[*].id}"}
    >>> context = {"user": {"name": "Alice"}, "orders": [{"id": "A001"}, {"id": "A002"}]}
    >>> resolve_json_placeholders(spec, context)
    {'name': 'Alice', 'orders': ['A001', 'A002']}
"""

import copy
import jmespath
from typing import Any, Dict, List, Union, Optional, TypeVar, cast

# Type definitions to make the code more readable and type-safe
JSONValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JSONDict = Dict[str, JSONValue]
T = TypeVar('T')


def resolve_json_placeholders(
    specification: JSONDict,
    context: JSONDict,
    placeholder_pattern: str = "{}",
    max_recursion_depth: int = 100,
) -> JSONDict:
    """
    Resolves JMESPath placeholders in a JSON specification using values from a context dictionary.

    This function creates a new copy of the specification and replaces any placeholder strings
    that match the format "{expression}" with the result of evaluating the JMESPath expression
    against the provided context dictionary.

    Args:
        specification: The JSON specification containing placeholders to be resolved.
        context: The context dictionary providing values for placeholder resolution.
        placeholder_pattern: The pattern used for placeholders, defaults to "{}" where the
                            expression is enclosed in curly braces.
        max_recursion_depth: Maximum depth for recursive processing to prevent stack overflow
                            from circular references.

    Returns:
        A new JSON dictionary with placeholders replaced by their resolved values.

    Raises:
        ValueError: If the placeholder pattern is invalid or empty.
        TypeError: If the specification or context is not a dictionary.
        RecursionError: If the maximum recursion depth is exceeded.

    Examples:
        >>> spec = {"user": "{user.name}", "location": "{address.city}"}
        >>> ctx = {"user": {"name": "John"}, "address": {"city": "New York"}}
        >>> resolve_json_placeholders(spec, ctx)
        {'user': 'John', 'location': 'New York'}

        >>> # Nested placeholders
        >>> spec = {"details": {"name": "{user.name}", "age": "{user.age}"}}
        >>> ctx = {"user": {"name": "Alice", "age": 30}}
        >>> resolve_json_placeholders(spec, ctx)
        {'details': {'name': 'Alice', 'age': 30}}

        >>> # Array handling
        >>> spec = {"order_ids": "{orders[*].id}"}
        >>> ctx = {"orders": [{"id": 101}, {"id": 102}]}
        >>> resolve_json_placeholders(spec, ctx)
        {'order_ids': [101, 102]}

        >>> # Unresolved placeholders remain unchanged
        >>> resolve_json_placeholders({"name": "{unknown}"}, {})
        {'name': '{unknown}'}
    """
    # Input validation
    if not isinstance(specification, dict):
        raise TypeError("Specification must be a dictionary")

    if not isinstance(context, dict):
        raise TypeError("Context must be a dictionary")

    if not placeholder_pattern or placeholder_pattern.count("{}") != 1:
        raise ValueError("Invalid placeholder pattern: must contain exactly one '{}' placeholder")

    # Create a deep copy to avoid modifying the original specification
    # This is important to maintain immutability of inputs
    spec_copy = copy.deepcopy(specification)

    # Extract the placeholder start and end markers
    start, end = placeholder_pattern.split("{}")

    def _resolve_value(value: JSONValue, depth: int = 0) -> JSONValue:
        """
        Recursively resolves placeholders in a JSON value.

        Args:
            value: The JSON value to process.
            depth: Current recursion depth to prevent stack overflow.

        Returns:
            The resolved value.

        Raises:
            RecursionError: If maximum recursion depth is exceeded.
        """
        # Check recursion depth to prevent stack overflow
        if depth > max_recursion_depth:
            raise RecursionError(f"Maximum recursion depth ({max_recursion_depth}) exceeded. Possible circular reference.")

        # Handle strings with placeholders
        if isinstance(value, str) and value.startswith(start) and value.endswith(end):
            # Extract the JMESPath expression
            expression = value[len(start):-len(end)]

            # Evaluate the expression against the context
            try:
                result = jmespath.search(expression, context)
                # Only replace if a value was found, otherwise keep the placeholder
                return result if result is not None else value
            except jmespath.exceptions.JMESPathError as e:
                # Log the error for debugging (in a real application)
                # logger.debug(f"Invalid JMESPath expression: {expression}. Error: {str(e)}")
                # If the expression is invalid, return the original value
                return value

        # Handle nested dictionaries - create a new dictionary with resolved values
        elif isinstance(value, dict):
            return {k: _resolve_value(v, depth + 1) for k, v in value.items()}

        # Handle lists - create a new list with resolved values
        elif isinstance(value, list):
            return [_resolve_value(item, depth + 1) for item in value]

        # Return other types unchanged (int, float, bool, None)
        return value

    # Process the entire specification
    return cast(JSONDict, _resolve_value(spec_copy))


# Additional utility function to demonstrate alternative approaches
def resolve_with_custom_error_handling(
    specification: JSONDict,
    context: JSONDict,
    on_error: str = "preserve"  # Options: "preserve", "null", "empty-string", "raise"
) -> JSONDict:
    """
    Resolves placeholders with custom error handling strategies.

    This is an extended version showing how different error handling strategies
    could be implemented for different scenarios.

    Args:
        specification: The JSON specification with placeholders.
        context: The context data for resolution.
        on_error: Strategy for handling failed resolutions:
                 - "preserve": Keep the original placeholder (default)
                 - "null": Replace with None
                 - "empty-string": Replace with empty string
                 - "raise": Raise an exception

    Returns:
        Resolved JSON dictionary.

    Raises:
        ValueError: If on_error is "raise" and a placeholder cannot be resolved.
    """
    # Implementation would be similar to resolve_json_placeholders but with
    # additional error handling logic based on the on_error parameter

    # This is a placeholder function to demonstrate the concept
    return resolve_json_placeholders(specification, context)
```

### **Unit Tests with Educational Comments**

```python
# FILE: tests/utilities/test_json_context_resolver.py

"""
Unit tests for the JSON context resolver utility.

This module contains comprehensive tests for the resolve_json_placeholders function,
covering various scenarios including basic substitution, nested structures,
arrays, and error cases.
"""

import pytest
from typing import Any, Dict, List
import copy
from utilities.json_context_resolver import resolve_json_placeholders


@pytest.fixture
def sample_context() -> Dict[str, Any]:
    """
    Provides a sample context dictionary for testing.

    A fixture in pytest is a function that provides test data or test objects.
    It's a way to set up a consistent test environment.

    Returns:
        A dictionary with test data.
    """
    return {
        "user": {
            "name": "Alice Smith",
            "age": 32,
            "contact": {
                "email": "alice@example.com",
                "phone": "555-1234"
            }
        },
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701"
        },
        "orders": [
            {"id": "A001", "amount": 125.50},
            {"id": "A002", "amount": 75.25},
            {"id": "A003", "amount": 220.00}
        ],
        "preferences": {
            "theme": "dark",
            "notifications": True
        },
        "empty_list": [],
        "null_value": None
    }


class TestJSONContextResolver:
    """
    Test suite for the JSON context resolver utility.

    This class groups related tests together. In pytest, classes are optional
    but can help organize tests logically.
    """

    def test_immutability(self, sample_context: Dict[str, Any]) -> None:
        """
        Test that the original inputs are not modified.

        This test verifies that our resolver function doesn't have side effects
        by modifying its input parameters.
        """
        # Create deep copies of inputs to compare after function call
        spec = {"name": "{user.name}", "age": "{user.age}"}
        spec_copy = copy.deepcopy(spec)
        context_copy = copy.deepcopy(sample_context)

        # Call the function
        resolve_json_placeholders(spec, sample_context)

        # Verify inputs weren't changed
        assert spec == spec_copy, "Input specification was modified"
        assert sample_context == context_copy, "Input context was modified"

    def test_basic_placeholders(self, sample_context: Dict[str, Any]) -> None:
        """Test basic placeholder resolution."""
        spec = {
            "name": "{user.name}",
            "email": "{user.contact.email}",
            "city": "{address.city}"
        }

        result = resolve_json_placeholders(spec, sample_context)

        assert result == {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "city": "Springfield"
        }

    def test_nested_structures(self, sample_context: Dict[str, Any]) -> None:
        """Test placeholder resolution in nested structures."""
        spec = {
            "user_info": {
                "name": "{user.name}",
                "contact": {
                    "email": "{user.contact.email}",
                    "phone": "{user.contact.phone}"
                }
            },
            "location": {
                "city": "{address.city}",
                "state": "{address.state}"
            }
        }

        result = resolve_json_placeholders(spec, sample_context)

        assert result == {
            "user_info": {
                "name": "Alice Smith",
                "contact": {
                    "email": "alice@example.com",
                    "phone": ...
```
