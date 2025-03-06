from utils.github_utils import ISSUE_TYPES, PRIORITY_LEVELS

def load_analyze_issue_prompt(placeholders: dict = {}) -> tuple[str, str]:
    """Load the prompt for analyzing a GitHub issue with LLM"""
    with open("SuperPrompt/analyze_issue_system_prompt.txt", "r") as file:
        raw_prompt = file.read()

    system_prompt = raw_prompt.format(**placeholders)

    with open("SuperPrompt/analyze_issue_user_prompt.txt", "r") as file:
        raw_prompt = file.read()
    user_prompt = raw_prompt.format(**placeholders)

    return system_prompt, user_prompt
