#!/usr/bin/env python3
import os
import json
import openai
import yaml
import re
import requests
from datetime import datetime
from packaging import version

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

SAMPLE_GITHUB_EVENT = {
  "action": "opened",
  "issue": {
    "number": 22,
    "title": "Add an LLM review to newly opened GitHub issues.",
    "body": """
When a new Github issue is created, start a workflow that reviews the issue:
* is the title clear?
* do the title and description match?
* is the description 'SMART'?

Optionally:
* make the workflow multi-stage, e.g. first determine the issue type, add a label for issue type, and make the description review depend on the issue type: bug reports need a different review than EPICs or Subtasks

Test/Proof of Concept:
* write an issue that implements a software reverse engineering ticket that writes YAML/XML documentation for components/classes/methods
    """,
    "html_url": "https://github.com/pkuppens/my_chat_gpt/issues/22",
    "labels": [
      {"name": "bug"},
      {"name": "enhancement"}
    ]
  },
  "repository": {
    "name": "my_chat_gpt",
    "owner": {
      "login": "pkuppens"
    }
  },
  "sender": {
    "login": "pkuppens"
  }
}

GITHUB_EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")
# Use the ChatCompletion model by default
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 2048))
TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.1))

# Issue categorization options
ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def check_openai_library_version():
    """Check if the openai library is up-to-date."""
    required_version = "0.27.0"
    if version.parse(openai.__version__) < version.parse(required_version):
        print(f"Your openai library version ({openai.__version__}) is outdated. "
              f"Please upgrade to at least version {required_version} using:\n"
              "pip install --upgrade openai")

def get_issue_data():
    """Read the GitHub event data for the issue"""
    if not GITHUB_EVENT_PATH:
        print("No GitHub event data found.")
        event_data = SAMPLE_GITHUB_EVENT
    else:
        with open(GITHUB_EVENT_PATH, 'r') as f:
            event_data = json.load(f)
    
    issue = event_data.get('issue', {})
    return {
        'repo_owner': event_data.get('repository', {}).get('owner', {}).get('login'),
        'repo_name': event_data.get('repository', {}).get('name'),
        'issue_number': issue.get('number'),
        'issue_title': issue.get('title'),
        'issue_body': issue.get('body') or "",
        'issue_url': issue.get('html_url'),
        'existing_labels': [label.get('name') for label in issue.get('labels', [])]
    }

def analyze_issue_with_llm(issue_data):
    """Use OpenAI chat.completions to analyze the issue and return parsed YAML output"""
    prompt = f"""
    Analyze and review this GitHub issue and provide the following:
    1. Issue Type (select one): {', '.join(ISSUE_TYPES)}
    2. Priority (select one): {', '.join(PRIORITY_LEVELS)}
    3. Estimated complexity (select one): Simple, Moderate, Complex
    4. Feedback:
        1. whether the Title is clear and concise, and matches the description
        2. whether the Description is unambiguous, detailed, and provides necessary context
        3. whether the Description is SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
        4. suggested first steps to address the issue, if not provided in the issue description
    
    FORMAT YOUR RESPONSE AS YAML, with the following keys:
    - issue_type
    - priority
    - complexity
    - review
    - next_steps
    
    ISSUE TITLE: {issue_data['issue_title']}
    
    ISSUE DESCRIPTION:
    {issue_data['issue_body']}
    """
    
    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes GitHub issues."},
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    response_content = response.choices[0].message.content.strip()
    clean_yaml = re.sub(r"^```yaml\n|```$", "", response_content, flags=re.MULTILINE)


    # Attempt to parse the YAML output; if parsing fails, fall back to a basic dict
    try:
        analysis = yaml.safe_load(clean_yaml)
        if not isinstance(analysis, dict):
            raise ValueError("Parsed YAML is not a dictionary.")
    except Exception as exc:
        print("Warning: Failed to parse YAML output. Using raw response as feedback.")
        analysis = {
            "issue_type": "Unknown",
            "priority": "Medium",
            "complexity": "Unknown",
            "review": response_content,
            "next_steps": ["Review issue manually"]
        }
    
    return analysis

def get_or_create_labels(repo_owner, repo_name, labels_to_create):
    """Ensure all required labels exist in the repository"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get existing labels
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/labels"
    response = requests.get(url, headers=headers)
    existing_labels = [label['name'] for label in response.json()]
    
    # Create any missing labels
    for label in labels_to_create:
        if label not in existing_labels:
            label_data = {
                "name": label,
                "color": "6f42c1"  # Default purple color
            }
            requests.post(url, headers=headers, json=label_data)

def add_labels_to_issue(repo_owner, repo_name, issue_number, labels):
    """Add labels to the issue"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
    data = {"labels": labels}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def add_comment_to_issue(repo_owner, repo_name, issue_number, comment):
    """Add a comment to the issue with the analysis"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201

def get_available_models():
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.get("https://api.openai.com/v1/models", headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
    models_data = response.json().get("data", [])
    models = [model["id"] for model in models_data]
    return models

def validate_openai_api_key():
    """Validate the OpenAI API key and its permissions"""
    try:
        get_available_models()
        return True
    except Exception as exc:
        print(f"Error validating OpenAI API key: {exc}")
        return False

def validate_github_token():
    """Validate the GitHub token and its permissions"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = "https://api.github.com/user"
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def main():
    # Check if the openai library is up-to-date
    check_openai_library_version()
    
    # Validate API keys and tokens
    if not validate_openai_api_key():
        raise ValueError("Invalid OpenAI API key or insufficient permissions.")
    if not validate_github_token():
        raise ValueError("Invalid GitHub token or insufficient permissions.")
    
    # Get issue data
    issue_data = get_issue_data()
    
    # Analyze issue with OpenAI chat.completions
    analysis = analyze_issue_with_llm(issue_data)
    
    # Prepare labels based on analysis
    labels_to_add = [
        f"Type: {analysis.get('issue_type', 'Unknown')}",
        f"Priority: {analysis.get('priority', 'Medium')}",
        f"Complexity: {analysis.get('complexity', 'Unknown')}"
    ]
    
    # Labels to ensure exist in the repository
    all_needed_labels = []
    for issue_type in ISSUE_TYPES:
        all_needed_labels.append(f"Type: {issue_type}")
    for priority in PRIORITY_LEVELS:
        all_needed_labels.append(f"Priority: {priority}")
    all_needed_labels.extend(["Complexity: Simple", "Complexity: Moderate", "Complexity: Complex"])
    
    # Create any missing labels
    get_or_create_labels(issue_data['repo_owner'], issue_data['repo_name'], all_needed_labels)
    
    # Add labels to issue
    add_labels_to_issue(
        issue_data['repo_owner'],
        issue_data['repo_name'],
        issue_data['issue_number'],
        labels_to_add
    )
    
    # Format the analysis comment
    next_steps = analysis.get('next_steps', ['Review issue manually'])
    if isinstance(next_steps, list):
        steps_formatted = "\n".join(['- ' + step for step in next_steps])
    else:
        steps_formatted = next_steps  # If it's not a list, use as is.
    
    comment = f"""
## Issue Analysis

**Type:** {analysis.get('issue_type', 'Unknown')}  
**Priority:** {analysis.get('priority', 'Medium')}  
**Complexity:** {analysis.get('complexity', 'Unknown')}

### Review Summary
{analysis.get('review', 'No summary available.')}

### Suggested Next Steps
{steps_formatted}

---
*Analyzed automatically at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Add the comment
    add_comment_to_issue(
        issue_data['repo_owner'],
        issue_data['repo_name'],
        issue_data['issue_number'],
        comment
    )

if __name__ == "__main__":
    main()
