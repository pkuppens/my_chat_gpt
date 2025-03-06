import os
import re
import yaml
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

import openai
import requests
from packaging import version
import github
from github import Github, Repository, Issue

from utils.github_utils import (
    get_github_client,
    get_repository,
    get_issues,
    create_issue,
    edit_issue,
    add_comment,
    ISSUE_TYPES,
    PRIORITY_LEVELS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
# just to see which of these work.
logging.info("Logging the start of the issue analysis...")
logger.info("Logger the start of the issue analysis...")
print("Printing the start of the issue analysis...")

# Configuration constants
DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.1
REQUIRED_OPENAI_VERSION = "1.65.2"

@dataclass
class OpenAIConfig:
    """
    Configuration for OpenAI API interactions.
    
    Attributes:
        api_key (str): OpenAI API key.
        model (str): LLM model to use.
        max_tokens (int): Maximum tokens for completion.
        temperature (float): Sampling temperature for generation.
    """
    api_key: str
    model: str = DEFAULT_LLM_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE

@dataclass
class IssueAnalysis:
    """
    Represents the result of an LLM-based issue analysis.
    
    Attributes:
        issue_type (str): Categorized type of the issue.
        priority (str): Assigned priority level.
        complexity (str): Estimated complexity.
        review_feedback (Dict[str, Any]): Detailed review insights.
        analysis (Dict[str, Any]): In-depth issue analysis.
        planning (List[str]): Suggested planning steps.
        goals (Dict[str, Any]): Issue goals and success criteria.
        next_steps (List[str]): Recommended immediate actions.
    """
    issue_type: str = "Unknown"
    priority: str = "Medium"
    complexity: str = "Unknown"
    review_feedback: Dict[str, Any] = field(default_factory=dict)
    analysis: Dict[str, Any] = field(default_factory=dict)
    planning: List[str] = field(default_factory=list)
    goals: Dict[str, Any] = field(default_factory=dict)
    next_steps: List[str] = field(default_factory=lambda: ["Review issue manually"])

class OpenAIVersionChecker:
    """Utility for checking OpenAI library version compatibility."""
    
    @staticmethod
    def check_library_version() -> bool:
        """
        Validate the installed OpenAI library version.
        
        Returns:
            bool: True if version is compatible, False otherwise.
        """
        try:
            current_version = version.parse(openai.__version__)
            required_version = version.parse(REQUIRED_OPENAI_VERSION)
            
            if current_version < required_version:
                logger.warning(
                    f"Outdated OpenAI library version. "
                    f"Current: {current_version}, Required: {required_version}. "
                    "Please upgrade using: pip install --upgrade openai"
                )
                return False
            return True
        except Exception as e:
            logger.error(f"Version check failed: {e}")
            return False

class OpenAIValidator:
    """Validates OpenAI API key and permissions."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate the OpenAI API key's permissions.
        
        Args:
            api_key (str): OpenAI API key to validate.
        
        Returns:
            bool: True if key is valid, False otherwise.
        """
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.openai.com/v1/models", headers=headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

class LLMIssueAnalyzer:
    """
    Performs LLM-based analysis of GitHub issues using OpenAI's API.
    """
    def __init__(self, config: OpenAIConfig):
        """
        Initialize the LLM issue analyzer.
        
        Args:
            config (OpenAIConfig): Configuration for OpenAI interactions.
        """
        self.config = config
        openai.api_key = config.api_key
    
    def _prepare_prompt(self, issue_data: Dict[str, Any]) -> str:
        """
        Prepare a system and user prompt for issue analysis.
        
        Args:
            issue_data (Dict[str, Any]): Issue details for analysis.
        
        Returns:
            str: Formatted prompt for LLM analysis.
        """
        from SuperPrompt import load_analyze_issue_prompt

        placeholders = {
            "issue_types": ', '.join(ISSUE_TYPES),
            "priority_levels": ', '.join(PRIORITY_LEVELS),
            "issue_data": issue_data,
            "issue_title": issue_data['issue_title'],
            "issue_body": issue_data['issue_body']
        }
        
        system_prompt, user_prompt = load_analyze_issue_prompt(placeholders=placeholders)
        return system_prompt, user_prompt
    
    def analyze_issue(self, issue_data: Dict[str, Any]) -> IssueAnalysis:
        """
        Analyze a GitHub issue using an LLM.
        
        Args:
            issue_data (Dict[str, Any]): Details of the issue to analyze.
        
        Returns:
            IssueAnalysis: Structured analysis of the issue.
        """
        system_prompt, user_prompt = self._prepare_prompt(issue_data)
        
        try:
            response = openai.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            response_content = response.choices[0].message.content.strip()
            clean_yaml = re.sub(r"^```yaml\n|```$", "", response_content, flags=re.MULTILINE)
            
            try:
                analysis_dict = yaml.safe_load(clean_yaml)
                if not isinstance(analysis_dict, dict):
                    raise ValueError("Parsed YAML is not a dictionary")
                
                return IssueAnalysis(**{k: v for k, v in analysis_dict.items() if hasattr(IssueAnalysis, k)})
            
            except Exception as parsing_error:
                logger.warning(f"YAML parsing failed: {parsing_error}")
                return IssueAnalysis(review_feedback=response_content)
        
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return IssueAnalysis()

class GitHubLabelManager:
    """
    Manages GitHub issue labels, ensuring required labels exist and are applied.
    """
    def __init__(self, github_token: str):
        """
        Initialize the label manager.
        
        Args:
            github_token (str): GitHub authentication token.
        """
        self.github_token = github_token
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def ensure_labels_exist(
        self, 
        repo_owner: str, 
        repo_name: str, 
        labels: List[str], 
        color: str = "6f42c1"
    ) -> None:
        """
        Ensure specified labels exist in the repository.
        
        Args:
            repo_owner (str): GitHub repository owner.
            repo_name (str): GitHub repository name.
            labels (List[str]): Labels to ensure exist.
            color (str, optional): Default color for new labels.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/labels"
        
        # Get existing labels
        response = requests.get(url, headers=self.headers)
        existing_labels = [label['name'] for label in response.json()]
        
        # Create missing labels
        for label in labels:
            if label not in existing_labels:
                label_data = {"name": label, "color": color}
                requests.post(url, headers=self.headers, json=label_data)
    
    def add_labels_to_issue(
        self, 
        repo_owner: str, 
        repo_name: str, 
        issue_number: int, 
        labels: List[str]
    ) -> bool:
        """
        Add labels to a specific GitHub issue.
        
        Args:
            repo_owner (str): GitHub repository owner.
            repo_name (str): GitHub repository name.
            issue_number (int): Issue number to label.
            labels (List[str]): Labels to add.
        
        Returns:
            bool: True if labels were successfully added, False otherwise.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        response = requests.post(url, headers=self.headers, json={"labels": labels})
        return response.status_code == 200

def main():
    """
    Main execution function for GitHub issue LLM analysis.
    """
    # Validate OpenAI library and API key
    if not OpenAIVersionChecker.check_library_version():
        raise RuntimeError("Incompatible OpenAI library version")
    
    # Setup configurations
    openai_config = OpenAIConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("LLM_MODEL", DEFAULT_LLM_MODEL),
        max_tokens=int(os.environ.get("MAX_TOKENS", DEFAULT_MAX_TOKENS)),
        temperature=float(os.environ.get("TEMPERATURE", DEFAULT_TEMPERATURE))
    )
    
    # Validate OpenAI API key
    if not OpenAIValidator.validate_api_key(openai_config.api_key):
        raise ValueError("Invalid OpenAI API key")
    
    # Process issue data
    from SuperPrompt import ISSUE_TYPES, PRIORITY_LEVELS
    
    # Retrieve issue data using GitHubEventProcessor from previous script
    from identify_duplicates_v2 import GitHubEventProcessor
    
    try:
        event = GitHubEventProcessor.parse_issue_event()
        issue_data = {
            'repo_owner': event.get('repository', {}).get('owner', {}).get('login'),
            'repo_name': event.get('repository', {}).get('name'),
            'issue_number': event.get('issue', {}).get('number'),
            'issue_title': event.get('issue', {}).get('title'),
            'issue_body': event.get('issue', {}).get('body') or ""
        }
        
        # Analyze issue
        llm_analyzer = LLMIssueAnalyzer(openai_config)
        analysis = llm_analyzer.analyze_issue(issue_data)
        
        # Prepare labels
        label_manager = GitHubLabelManager(os.environ.get("GITHUB_TOKEN", ""))
        
        # Ensure all potential labels exist
        all_labels = [
            *[f"Type: {issue_type}" for issue_type in ISSUE_TYPES],
            *[f"Priority: {priority}" for priority in PRIORITY_LEVELS],
            "Complexity: Simple", "Complexity: Moderate", "Complexity: Complex"
        ]
        label_manager.ensure_labels_exist(
            issue_data['repo_owner'], 
            issue_data['repo_name'], 
            all_labels
        )
        
        # Add specific labels for this issue
        specific_labels = [
            f"Type: {analysis.issue_type}",
            f"Priority: {analysis.priority}",
            f"Complexity: {analysis.complexity}"
        ]
        label_manager.add_labels_to_issue(
            issue_data['repo_owner'], 
            issue_data['repo_name'], 
            issue_data['issue_number'], 
            specific_labels
        )
        
        # Add comment with analysis details
        comment = f"""
## Issue Analysis

**Type:** {analysis.issue_type}
**Priority:** {analysis.priority}
**Complexity:** {analysis.complexity}

### Review Summary
{analysis.review_feedback}

### Suggested Next Steps
{chr(10).join(f'- {step}' for step in analysis.next_steps)}

---
*Analyzed automatically at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Optional: Add comment to issue
        logger.info(f"Analysis complete for issue #{issue_data['issue_number']}")
        logger.info(f"Analysis result: {analysis}")
        logger.info(f"Comment added to issue: {comment}")
        # You would implement this similar to previous script's add_comment_to_issue method
        
    except Exception as e:
        logger.error(f"Issue analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()
