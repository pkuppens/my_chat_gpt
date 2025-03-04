ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

def load_analyze_issue_prompt(placeholders: dict = {}) -> str:
    """Load the prompt for analyzing a GitHub issue with LLM"""
    with open("SuperPrompt/analyze_issue_prompt.txt", "r") as file:
        raw_prompt = file.read()

    prompt = raw_prompt.format(**placeholders)

    return prompt
