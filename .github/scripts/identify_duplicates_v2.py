from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import os
import json
import logging
import sys
from datetime import datetime, timedelta

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

@dataclass
class IssueContext:
    """
    Represents the context and metadata of a GitHub issue.
    
    Attributes:
        number (int): The unique issue number.
        title (str): The title of the issue.
        body (str): The body/description of the issue.
        state (str): Current state of the issue (open/closed).
        created_at (datetime): Timestamp when the issue was created.
        url (str): HTML URL of the issue.
    """
    number: int
    title: str
    body: Optional[str]
    state: str
    created_at: datetime
    url: str

class GithubClientFactory:
    """
    Factory class for creating GitHub API clients and retrieving repository context.
    """
    @classmethod
    def create_client(cls) -> Github:
        """
        Creates a GitHub client using environment-based authentication.
        
        Returns:
            Github: Authenticated GitHub client instance.
        
        Raises:
            ValueError: If GitHub token is not found in environment.
        """
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        return get_github_client(github_token)
    
    @classmethod
    def get_repository(cls, client: Github) -> Repository.Repository:
        """
        Retrieves the GitHub repository from environment configuration.
        
        Args:
            client (Github): Authenticated GitHub client.
        
        Returns:
            Repository.Repository: The specified GitHub repository.
        
        Raises:
            ValueError: If repository name is not found in environment.
        """
        repo_name = os.getenv('GITHUB_REPOSITORY')
        if not repo_name:
            raise ValueError("GITHUB_REPOSITORY not found in environment variables")
        return get_repository(client, repo_name)

class IssueRetriever:
    """
    Service for retrieving and filtering GitHub issues.
    """
    def __init__(self, repository: Repository.Repository):
        """
        Initialize the issue retriever with a specific repository.
        
        Args:
            repository (Repository.Repository): The GitHub repository to query.
        """
        self.repository = repository
    
    def get_recent_issues(
        self, 
        days_back: int = 30, 
        state: Optional[str] = None
    ) -> List[IssueContext]:
        """
        Retrieve recent issues from the repository.
        
        Args:
            days_back (int, optional): Number of days to look back. Defaults to 30.
            state (str, optional): Filter by issue state (open/closed). Defaults to None.
        
        Returns:
            List[IssueContext]: List of recent issues in the repository.
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        issues = get_issues(self.repository, state=state)
        
        return [
            IssueContext(
                number=issue.number,
                title=issue.title,
                body=issue.body,
                state=issue.state,
                created_at=issue.created_at,
                url=issue.html_url
            ) for issue in issues if issue.created_at >= cutoff_date
        ]

class IssueSimilarityAnalyzer:
    """
    Performs similarity analysis on GitHub issues using TF-IDF and cosine similarity.
    """
    def __init__(self, vectorizer: Optional[TfidfVectorizer] = None):
        """
        Initialize the similarity analyzer.
        
        Args:
            vectorizer (Optional[TfidfVectorizer]): Custom vectorizer. Uses default if not provided.
        """
        self.vectorizer = vectorizer or TfidfVectorizer(stop_words='english')
    
    def compute_similarities(
        self, 
        target_issue: IssueContext, 
        existing_issues: List[IssueContext], 
        threshold: float = 0.8
    ) -> List[Tuple[IssueContext, float]]:
        """
        Compute similarities between a target issue and existing issues.
        
        Args:
            target_issue (IssueContext): The issue to compare against others.
            existing_issues (List[IssueContext]): List of issues to compare.
            threshold (float, optional): Minimum similarity score. Defaults to 0.8.
        
        Returns:
            List[Tuple[IssueContext, float]]: Similar issues with their similarity scores.
        """
        def prepare_text(issue: IssueContext) -> str:
            return f"{issue.title}\n{issue.body or ''}"
        
        issue_texts = [prepare_text(issue) for issue in existing_issues]
        target_text = prepare_text(target_issue)
        
        # Add target text and compute similarities
        all_texts = issue_texts + [target_text]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        # Filter and return similar issues
        return [
            (existing_issues[i], similarities[i]) 
            for i in range(len(similarities)) 
            if similarities[i] >= threshold
        ]

class GitHubEventProcessor:
    """
    Processes GitHub webhook events for issue-related actions.
    """
    @staticmethod
    def parse_issue_event() -> Dict[str, Any]:
        """
        Parse the GitHub Actions event file.
        
        Returns:
            Dict[str, Any]: Parsed GitHub event data.
        
        Raises:
            ValueError: If event cannot be processed.
        """
        event_path = os.getenv('GITHUB_EVENT_PATH')
        if not event_path:
            raise ValueError("Not running in GitHub Actions environment")
        
        try:
            with open(event_path, 'r') as f:
                event = json.load(f)
            
            if 'issue' not in event:
                raise ValueError("Event does not contain issue data")
            
            return event
        except Exception as e:
            logger.error(f"Event processing error: {e}")
            raise
    
    @classmethod
    def extract_issue_context(cls, event: Dict[str, Any]) -> IssueContext:
        """
        Extract IssueContext from a GitHub event.
        
        Args:
            event (Dict[str, Any]): Parsed GitHub event.
        
        Returns:
            IssueContext: Extracted issue context.
        """
        issue_data = event['issue']
        return IssueContext(
            number=issue_data['number'],
            title=issue_data['title'],
            body=issue_data.get('body'),
            state=issue_data['state'],
            created_at=datetime.fromisoformat(issue_data['created_at'].replace("Z", "+00:00")),
            url=issue_data['html_url']
        )

def main():
    """
    Main execution function for GitHub issue similarity detection.
    """
    try:
        # Setup GitHub client and repository
        github_client = GithubClientFactory.create_client()
        repository = GithubClientFactory.get_repository(github_client)
        
        # Process event and extract issue context
        event = GitHubEventProcessor.parse_issue_event()
        current_issue = GitHubEventProcessor.extract_issue_context(event)
        
        # Retrieve recent issues
        issue_retriever = IssueRetriever(repository)
        recent_issues = issue_retriever.get_recent_issues(state='all')
        
        # Filter out current issue from recent issues
        comparable_issues = [
            issue for issue in recent_issues 
            if issue.number != current_issue.number
        ]
        
        # Analyze similarities
        similarity_analyzer = IssueSimilarityAnalyzer()
        similar_issues = similarity_analyzer.compute_similarities(
            current_issue, 
            comparable_issues
        )
        
        # Optional: log or process similar issues
        for issue, similarity in similar_issues:
            logger.info(
                f"Similar Issue: #{issue.number} "
                f"(Similarity: {similarity:.2%}, URL: {issue.url})"
            )
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
