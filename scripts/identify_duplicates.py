import os
import logging
from datetime import datetime, timedelta

import requests

from utils.logger import logger


def get_issues(repo, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def categorize_similarity(similarity):
    if 0.7 <= similarity:
        return "high"
    elif 0.4 <= similarity < 0.7:
        return "moderate"
    else:
        return "low"


def find_similar_issues(new_issue, issues):
    high_similarity_issues = []
    moderate_similarity_issues = []
    new_description = new_issue["body"]
    for issue in issues:
        if issue["number"] == new_issue["number"]:
            logging.info(f"Skipping current issue #{issue['number']}")
            continue
        similarity = calculate_similarity(new_description, issue["body"])
        logging.debug(f"Similarity score for issue #{issue['number']}: {similarity}")
        similarity_category = categorize_similarity(similarity)
        if similarity_category == "high":
            high_similarity_issues.append(issue)
        elif similarity_category == "moderate":
            moderate_similarity_issues.append(issue)
    return high_similarity_issues, moderate_similarity_issues


def calculate_similarity(text1, text2):
    # Placeholder for actual similarity calculation logic
    return 0.9


def comment_on_issue(repo, issue_number, comment, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def create_similarity_comment(issue_number, high_similarity_issues, moderate_similarity_issues):
    if not high_similarity_issues and not moderate_similarity_issues:
        logging.info("No similar or related issues found, skipping comment creation")
        return

    comment_body = "## Similarity Analysis\n\n"

    if high_similarity_issues:
        comment_body += "### Potential Duplicate Issues (High Similarity >=70%)\n\n"
        for issue in high_similarity_issues:
            comment_body += f"- #{issue['number']}: {issue['title']}\n"

    if moderate_similarity_issues:
        comment_body += "\n### Related Issues (Moderate Similarity 40-70%)\n\n"
        for issue in moderate_similarity_issues:
            comment_body += f"- #{issue['number']}: {issue['title']}\n"

    logging.info(f"Creating comment on issue #{issue_number} with similarity analysis")
    return comment_body


def main():
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")
    new_issue_number = os.getenv("GITHUB_ISSUE_NUMBER")

    logging.info(f"Repository: {repo}")

    issues = get_issues(repo, token)
    new_issue = next(issue for issue in issues if issue["number"] == int(new_issue_number))
    logging.info(f"Processing issue #{new_issue['number']}: {new_issue['title']}")

    # Get and count open issues
    open_issues = [issue for issue in issues if issue["state"] == "open"]
    logging.info(f"Found {len(open_issues)} open issues")

    # Get and count recently closed issues (last 120 days)
    one_hundred_twenty_days_ago = datetime.now() - timedelta(days=120)
    recently_closed_issues = [
        issue
        for issue in issues
        if (
            issue["state"] == "closed" and datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ") > one_hundred_twenty_days_ago
        )
    ]
    logging.info(f"Found {len(recently_closed_issues)} recently closed issues (last 120 days)")

    high_similarity_issues, moderate_similarity_issues = find_similar_issues(new_issue, open_issues + recently_closed_issues)

    comment = create_similarity_comment(new_issue_number, high_similarity_issues, moderate_similarity_issues)
    if comment:
        comment_on_issue(repo, new_issue_number, comment, token)


if __name__ == "__main__":
    main()
