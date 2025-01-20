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
        issues = repo.get_issues(state='all', since=datetime.now() - timedelta(days=30))
        
        issue_texts = [issue.title + " " + issue.body for issue in issues]
        new_issue_text = issue_title + " " + issue_body
        
        tfidf_matrix = self.vectorizer.fit_transform(issue_texts + [new_issue_text])
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        
        similar_issues = []
        for i, score in enumerate(cosine_similarities):
            if score >= threshold:
                similar_issues.append((issues[i], score, issues[i].state))
        
        similar_issues.sort(key=lambda x: x[1], reverse=True)
        return similar_issues

    def comment_on_issue(self, repo_name, issue_number, comment):
        """
        Add a comment to a specific issue.
        
        Args:
            repo_name (str): Full repository name (e.g., 'owner/repo')
            issue_number (int): Number of the issue to comment on
            comment (str): Comment text to add
        """
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment)

def main():
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    issue_number = int(os.getenv("GITHUB_ISSUE_NUMBER"))
    issue_title = os.getenv("GITHUB_ISSUE_TITLE")
    issue_body = os.getenv("GITHUB_ISSUE_BODY")
    
    detector = GithubDuplicateIssueDetector(github_token)
    similar_issues = detector.find_similar_issues(repo_name, issue_title, issue_body)
    
    if similar_issues:
        comment = "Possible duplicate issues:\n"
        for issue, score, status in similar_issues:
            comment += f"- #{issue.number} [{status}]: {issue.title} (Similarity: {score:.2f})\n"
        detector.comment_on_issue(repo_name, issue_number, comment)

if __name__ == "__main__":
    main()
