"""
Issue Analysis Prompt Manager.

This module provides functionality for loading and formatting prompts used by LLMs
to analyze GitHub issues. It handles the loading of system and user prompts from
template files and performs variable substitution for customization.

The module leverages issue classification constants from github_utils to ensure
consistency in how issues are categorized and prioritized across the application.

Dependencies:
    - my_chat_gpt_utils.github_utils

Usage:
    Import this module to load pre-defined prompts for issue analysis,
    with support for dynamic placeholder substitution.

Example:
-------
    system_prompt, user_prompt = load_analyze_issue_prompt({
        "issue_title": "Fix login screen",
        "issue_body": "Users cannot log in with correct credentials"
    })

TODO: Be explicit about the placeholders that can be used in the prompt templates.
E.g. {issue_title}, {issue_body}, {issue_types}, {priority_levels}, etc.
The current function could leave undefined placeholders in the prompt.

"""

import os
import tempfile
from typing import Any

# Try to import from my_chat_gpt_utils package, but fallback to constants if running standalone
try:
    from my_chat_gpt_utils.github_utils import ISSUE_TYPES, PRIORITY_LEVELS
except ImportError:
    # Define constants for standalone operation
    ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
    PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]


class PlaceholderDict(dict):
    """
    Dictionary subclass that returns placeholder strings for missing keys.

    This class is used to handle undefined placeholders in prompt templates
    by returning the placeholder key wrapped in curly braces instead of raising
    a KeyError.
    """

    def __missing__(self, key):
        """
        Return a placeholder string for missing keys.

        Args:
        ----
            key: The missing key.

        Returns:
        -------
            str: The key wrapped in curly braces as a placeholder.

        """
        return "{" + key + "}"


def load_analyze_issue_prompt(
    placeholders: dict[str, Any] | None = None,
    include_best_practices: bool = False,
) -> tuple[str, str]:
    """
    Load and format the system and user prompts for issue analysis.

    Args:
    ----
        placeholders: Dictionary of placeholder values to substitute in the prompts.
        include_best_practices: If True, includes additional best practices context
                               (note: best practices are now embedded in the system prompt).

    Returns:
    -------
        Tuple containing the formatted system prompt and user prompt.

    """
    placeholders = placeholders or {}  # do not use mutable {} as default parameter!

    # Add standard placeholders if not provided
    if "issue_types" not in placeholders:
        placeholders["issue_types"] = ", ".join(ISSUE_TYPES)
    if "priority_levels" not in placeholders:
        placeholders["priority_levels"] = ", ".join(PRIORITY_LEVELS)

    placeholders = PlaceholderDict(placeholders)

    try:
        with open("SuperPrompt/analyze_issue_system_prompt.txt", encoding="utf-8") as file:
            raw_prompt = file.read()
        system_prompt = raw_prompt.format_map(placeholders)

        with open("SuperPrompt/analyze_issue_user_prompt.txt", encoding="utf-8") as file:
            raw_prompt = file.read()

        user_prompt = raw_prompt.format_map(placeholders)
    except FileNotFoundError:
        # For testing: use sample prompts if files don't exist
        system_prompt = (
            "System prompt: Analyze this GitHub issue. Issue types: {issue_types}. Priority levels: {priority_levels}".format(
                **placeholders,
            )
        )
        user_prompt = (
            ("User prompt: Analyze issue titled '{issue_title}' with description '{issue_body}'".format(**placeholders))
            if "issue_title" in placeholders and "issue_body" in placeholders
            else "User prompt: Please provide issue details."
        )

    return system_prompt, user_prompt


# Test functions
def test_load_prompt_with_empty_placeholders():
    """Test loading prompts with no placeholders."""
    system, user = load_analyze_issue_prompt()
    assert "Issue Type" in system
    assert isinstance(system, str)
    assert isinstance(user, str)


def test_load_prompt_with_placeholders():
    """Test loading prompts with placeholders."""
    placeholders = {
        "issue_title": "Bug in login form",
        "issue_body": "Users cannot log in with correct credentials",
    }
    system, user = load_analyze_issue_prompt(placeholders)
    assert "Bug in login form" in user


def test_create_temp_prompt_files():
    """Test loading prompts from temp files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "SuperPrompt"), exist_ok=True)

        # Create temp prompt files
        with open(
            os.path.join(tmpdir, "SuperPrompt", "analyze_issue_system_prompt.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("Test system prompt with {issue_types}")

        with open(
            os.path.join(tmpdir, "SuperPrompt", "analyze_issue_user_prompt.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("Test user prompt for {issue_title}")

        # Save current directory
        original_dir = os.getcwd()
        try:
            # Change to temp directory
            os.chdir(tmpdir)

            # Test loading
            system, user = load_analyze_issue_prompt({"issue_title": "Test Issue"})
            assert "Test system prompt with" in system
            assert "Test user prompt for Test Issue" in user
        finally:
            # Restore original directory
            os.chdir(original_dir)


def run_tests():
    """Run all tests in this module."""
    # This is a simple test runner for standalone execution
    test_functions = [
        test_load_prompt_with_empty_placeholders,
        test_load_prompt_with_placeholders,
        test_create_temp_prompt_files,
    ]

    failures = 0
    for test_func in test_functions:
        try:
            print(f"Running {test_func.__name__}...")
            test_func()
            print(f"✓ {test_func.__name__} passed")
        except Exception as e:
            failures += 1
            print(f"✗ {test_func.__name__} failed: {e!s}")

    print(f"\nTest summary: {len(test_functions) - failures} passed, {failures} failed")
    return failures == 0


if __name__ == "__main__":
    print("Running standalone tests for Issue Analysis Prompt Manager")
    success = run_tests()
    exit(0 if success else 1)


class DocumentationPrompt:
    """Class for managing documentation generation prompts."""

    def __init__(self):
        """Initialize the DocumentationPrompt instance."""

    @staticmethod
    def get_prompt(item: dict[str, Any]) -> str:
        """
        Generate a documentation prompt for the given item.

        Args:
        ----
            item: Dictionary containing the item details to document.

        Returns:
        -------
            str: The formatted documentation prompt.

        """
        return f"""Generate documentation for the following item:
Title: {item.get("title", "N/A")}
Description: {item.get("description", "N/A")}
Type: {item.get("type", "N/A")}

Please provide clear, concise documentation that follows best practices."""


def get_documentation_prompt(item: dict[str, Any]) -> str:
    """Get a documentation prompt for the given item."""
    return DocumentationPrompt.get_prompt(item)


class IssueAnalysisPrompt:
    """Class for managing issue analysis prompts."""

    def __init__(self, issue_type: str, priority: str, title: str, body: str):
        """
        Initialize the IssueAnalysisPrompt instance.

        Args:
        ----
            issue_type: The type of the issue.
            priority: The priority level of the issue.
            title: The title of the issue.
            body: The body of the issue.
        """
        self.issue_type = issue_type
        self.priority = priority
        self.title = title
        self.body = body
        self.system_prompt_file = "SuperPrompt/analyze_issue_system_prompt.txt"

    def get_system_prompt(self) -> str:
        try:
            with open(self.system_prompt_file, "r", encoding="utf-8") as f:
                raw_prompt = f.read()
            return raw_prompt.format(
                issue_type=self.issue_type,
                priority=self.priority,
                title=self.title,
                body=self.body,
            )
        except FileNotFoundError:
            return (
                "You are a helpful assistant that analyzes GitHub issues. "
                "Please analyze the following issue and provide a detailed response.\n\n"
                "Issue Type: {issue_type}\nPriority: {priority}\n\n"
                "Title: {title}\n\nBody: {body}"
            ).format(
                issue_type=self.issue_type,
                priority=self.priority,
                title=self.title,
                body=self.body,
            )
