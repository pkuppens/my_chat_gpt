#!/usr/bin/env python3
import os
import json
import openai
import yaml
import re
import requests
from datetime import datetime

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")
LLM_PROVIDER = os.environ.get("LLM_MODEL", "openai")
LLM_MODEL = os.environ.get("LLM_MODEL", "o3-mini")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 2048))
TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.1))

# Issue categorization options
ISSUE_TYPES = ["Epic", "Change Request", "Bug Fix", "Task", "Question"]
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

def get_issue_data():
    """Read the GitHub event data for the issue"""
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
    """Use OpenAI to analyze the issue"""
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
    
    # Extract response markdown content
    return response.choices[0].message.content.strip()

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

def main():
    # Get issue data
    issue_data = get_issue_data()
    
    # Analyze issue with OpenAI
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
    comment = f"""
## Issue Analysis

**Type:** {analysis.get('issue_type', 'Unknown')}  
**Priority:** {analysis.get('priority', 'Medium')}  
**Complexity:** {analysis.get('complexity', 'Unknown')}

### Review Summary
{analysis.get('review', 'No summary available.')}

### Suggested Next Steps
{chr(10).join(['- ' + step for step in analysis.get('next_steps', ['Review issue manually'])])}

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
