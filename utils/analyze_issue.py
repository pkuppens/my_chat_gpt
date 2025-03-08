import os
import logging
from typing import Dict, Any
from dataclasses import dataclass, field

from utils.github_utils import append_response_to_issue
from utils.openai_utils import parse_openai_response, make_openai_api_call

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

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

class LLMIssueAnalyzer:
    """
    Performs LLM-based analysis of GitHub issues using OpenAI's API.
    """
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM issue analyzer.
        
        Args:
            config (Dict[str, Any]): Configuration for OpenAI interactions.
        """
        self.config = config
    
    def _prepare_prompt(self, issue_data: Dict[str, Any]) -> str:
        """
        Prepare a system and user prompt for issue analysis.
        
        Args:
            issue_data (Dict[str, Any]): Issue details for analysis.
        
        Returns:
            str: Formatted prompt for LLM analysis.
        """
        from utils.prompts import load_analyze_issue_prompt

        placeholders = {
            "issue_types": ', '.join(self.config.get('issue_types', [])),
            "priority_levels": ', '.join(self.config.get('priority_levels', [])),
            "issue_data": issue_data,
            "issue_title": issue_data.get('issue_title', '{issue_title}'),
            "issue_body": issue_data.get('issue_body', '{issue_body}'),
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
            response_content = make_openai_api_call(
                api_key=self.config['api_key'],
                model=self.config['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            analysis_dict = parse_openai_response(response_content)
            
            if isinstance(analysis_dict, dict):
                return IssueAnalysis(**{k: v for k, v in analysis_dict.items() if hasattr(IssueAnalysis, k)})
            else:
                append_response_to_issue(issue_data, response_content)
                return IssueAnalysis(review_feedback=response_content)
        
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise
