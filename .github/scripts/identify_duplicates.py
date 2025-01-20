from github import Github
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import os
import json
import sys
import logging

# Configure logging to show in GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class GithubDuplicateIssueDetector:
    def __init__(self):
        """
        Initialize the detector with GitHub credentials and repository info.
        Reads configuration from environment variables.
        """
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN not found in environment")
            
        self.github = Github(self.github_token)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        self.repo_name = os.getenv('GITHUB_REPOSITORY')
        if not self.repo_name:
            raise ValueError("GITHUB_REPOSITORY not found in environment")
            
        self.repo = self.github.get_repo(self.repo_name)
        logging.info(f"Initialized detector for repository: {self.repo_name}")
        
    def find_similar_issues(self, current_issue_number, issue_title, issue_body, threshold=0.8):
        """
        Check for similar issues, including those closed in the last 30 days.
        """
        logging.info(f"Processing issue #{current_issue_number}: {issue_title}")
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Combine title and body for better comparison
        current_issue_text = f"{issue_title}\n{issue_body}"
        existing_issues = []
        issue_texts = []
        
        # Get and count open issues
        open_issues = list(self.repo.get_issues(state='open'))
        logging.info(f"Found {len(open_issues)} open issues")
        
        # Get and count recently closed issues
        recently_closed_issues = list(self.repo.get_issues(state='closed', since=thirty_days_ago))
        logging.info(f"Found {len(recently_closed_issues)} recently closed issues (last 30 days)")
        
        # Process both sets of issues
        for issue_set, set_type in [(open_issues, 'open'), (recently_closed_issues, 'closed')]:
            for issue in issue_set:
                if issue.number == current_issue_number:
                    logging.info(f"Skipping current issue #{issue.number} ({set_type})")
                    continue
                    
                logging.debug(f"Processing {set_type} issue #{issue.number}: {issue.title}")
                existing_issues.append(issue)
                issue_texts.append(f"{issue.title}\n{issue.body or ''}")
        
        if not issue_texts:
            logging.info("No existing issues found to compare against")
            return []
            
        logging.info(f"Comparing against {len(issue_texts)} existing issues")
            
        all_texts = issue_texts + [current_issue_text]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        similar_issues = [
            (existing_issues[i], similarities[i], 'closed' if existing_issues[i].state == 'closed' else 'open')
            for i in range(len(similarities))
            if similarities[i] >= threshold
        ]
        
        if similar_issues:
            logging.info(f"Found {len(similar_issues)} similar issues above threshold {threshold}")
            for issue, similarity, state in similar_issues[:5]:
                logging.info(f"Similar issue #{issue.number}: {issue.title} ({similarity:.1%} similar, {state})")
        else:
            logging.info("No similar issues found above threshold")
        
        return sorted(similar_issues, key=lambda x: x[1], reverse=True)

    def create_similarity_comment(self, issue_number, similar_issues):
        """
        Create a comment on the issue with similarity results.
        """
        if not similar_issues:
            logging.info("No similar issues found, skipping comment creation")
            return
            
        comment_body = "## Potential Duplicate Issues Found\n\n"
        for similar_issue, similarity, state in similar_issues[:5]:
            status_emoji = "🟢" if state == "open" else "🔴"
            comment_body += (
                f"{status_emoji} #{similar_issue.number}: [{similar_issue.title}]({similar_issue.html_url})\n"
                f"   - Similarity: {similarity:.1%}\n"
                f"   - Status: {state}\n\n"
            )
        
        logging.info(f"Creating comment on issue #{issue_number}")
        issue = self.repo.get_issue(number=issue_number)
        issue.create_comment(comment_body)

def validate_github_event():
    """
    Validate that the GitHub event is an issue event and return the event data.
    """
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        raise ValueError("This script should be run within a GitHub Action")
    
    try:
        with open(event_path, 'r') as f:
            event = json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading event file: {e}")
    
    if 'issue' not in event:
        raise ValueError("This action only works with issue events")
        
    required_fields = ['title', 'body', 'number']
    missing_fields = [field for field in required_fields if field not in event['issue']]
    if missing_fields:
        raise ValueError(f"Missing required issue fields: {', '.join(missing_fields)}")
        
    return event

def main():
    try:
        logging.info("Starting duplicate issue detection")
        event = validate_github_event()
        detector = GithubDuplicateIssueDetector()
        
        similar_issues = detector.find_similar_issues(
            event['issue']['number'],
            event['issue']['title'],
            event['issue']['body'] or ''
        )
        
        detector.create_similarity_comment(event['issue']['number'], similar_issues)
        logging.info("Completed duplicate issue detection")
        
    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        try:
            logging.info("Running in test mode")
            detector = GithubDuplicateIssueDetector()
            similar_issues = detector.find_similar_issues(
                123,  # Test issue number
                "Test Issue Title",
                "Test Issue Body"
            )
            logging.info(f"Test completed: found {len(similar_issues)} similar issues")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            sys.exit(1)
    else:
        main()