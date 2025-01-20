from github import Github
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import os
import json
import sys

class GithubDuplicateIssueDetector:
    def __init__(self, github_token):
        """
        Initialize the detector with GitHub credentials.
        
        Args:
            github_token (str): GitHub API token for authentication
        """
        self.github = Github(github_token)
        # TfidfVectorizer converts text to numerical vectors using term frequency-inverse document frequency
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def find_similar_issues(self, repo_name, issue_title, issue_body, threshold=0.8):
        """
        Check for similar issues, including those closed in the last 30 days.
        
        Args:
            repo_name (str): Full repository name (e.g., 'owner/repo')
            issue_title (str): Title of the new issue
            issue_body (str): Body of the new issue
            threshold (float): Minimum similarity score (0-1) to consider issues as similar
            
        Returns:
            list: List of tuples (issue, similarity_score, status) sorted by similarity
        """
        repo = self.github.get_repo(repo_name)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Fetch both current open issues and recently closed ones
        open_issues = repo.get_issues(state='open')
        recently_closed_issues = repo.get_issues(state='closed', since=thirty_days_ago)
        
        # Combine title and body for better comparison
        new_issue_text = f"{issue_title}\n{issue_body}"
        existing_issues = []
        issue_texts = []
        
        # Process both open and recently closed issues
        for issue_list in [open_issues, recently_closed_issues]:
            for issue in issue_list:
                existing_issues.append(issue)
                issue_texts.append(f"{issue.title}\n{issue.body}")
        
        if not issue_texts:
            return []
            
        # Add new issue text to the end of the list for vectorization
        all_texts = issue_texts + [new_issue_text]
        
        # Convert texts to TF-IDF matrix
        # Shape: (n_documents, n_features) where:
        # - n_documents = number of issues + 1 (new issue)
        # - n_features = number of unique terms in vocabulary
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate cosine similarity between the new issue (last row) and all existing issues
        # similarities shape: (1, n_documents-1)
        # Each value represents cosine similarity (0-1) where:
        # - 0 means completely different
        # - 1 means exactly the same
        # - Values like 0.8 suggest strong similarity
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        # Create list of similar issues that meet threshold
        similar_issues = [
            (existing_issues[i], similarities[i], 'closed' if existing_issues[i].state == 'closed' else 'open')
            for i in range(len(similarities))
            if similarities[i] >= threshold
        ]
        
        return sorted(similar_issues, key=lambda x: x[1], reverse=True)

def validate_github_event():
    """
    Validate that the GitHub event is an issue event and return the event data.
    
    Returns:
        dict: The event data if valid
    Raises:
        SystemExit: If event is invalid or not an issue event
    """
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        print("Error: This script should be run within a GitHub Action")
        sys.exit(1)
    
    try:
        with open(event_path, 'r') as f:
            event = json.load(f)
    except Exception as e:
        print(f"Error reading event file: {e}")
        sys.exit(1)
    
    # Verify this is an issue event
    if 'issue' not in event:
        print("Error: This action only works with issue events")
        sys.exit(1)
        
    # Verify we have the minimum required issue data
    required_fields = ['title', 'body', 'number']
    missing_fields = [field for field in required_fields if field not in event['issue']]
    if missing_fields:
        print(f"Error: Missing required issue fields: {', '.join(missing_fields)}")
        sys.exit(1)
        
    return event

def main():
    # Validate GitHub event and environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment")
        sys.exit(1)
    
    event = validate_github_event()
    repo_name = os.getenv('GITHUB_REPOSITORY')
    
    # Initialize detector and find similar issues
    detector = GithubDuplicateIssueDetector(github_token)
    similar_issues = detector.find_similar_issues(
        repo_name,
        event['issue']['title'],
        event['issue']['body'] or ''  # Handle case where body is None
    )
    
    # Only create comment if similar issues are found
    if similar_issues:
        comment_body = "## Potential Duplicate Issues Found\n\n"
        for similar_issue, similarity, state in similar_issues[:5]:  # Show top 5 matches
            status_emoji = "🟢" if state == "open" else "🔴"
            comment_body += (
                f"{status_emoji} #{similar_issue.number}: [{similar_issue.title}]({similar_issue.html_url})\n"
                f"   - Similarity: {similarity:.1%}\n"
                f"   - Status: {state}\n\n"
            )
        
        # Post comment on the issue
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=event['issue']['number'])
        issue.create_comment(comment_body)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run test code
        github_token = os.getenv('GITHUB_TOKEN')
        detector = GithubDuplicateIssueDetector(github_token)
        similar_issues = detector.find_similar_issues(
            'test/test',
            'Test Issue Title',
            'Test Issue Body'
        )
        print(similar_issues)
    else:
        main()
