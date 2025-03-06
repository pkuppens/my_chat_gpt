from utils.github_utils import ISSUE_TYPES, PRIORITY_LEVELS

def load_analyze_issue_prompt(placeholders: dict = {}) -> str:
    """Load the prompt for analyzing a GitHub issue with LLM"""
    with open("SuperPrompt/analyze_issue_prompt.txt", "r") as file:
        raw_prompt = file.read()

    prompt = raw_prompt.format(**placeholders)

    return prompt
