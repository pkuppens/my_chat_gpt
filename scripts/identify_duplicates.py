import os
import requests
import logging
from datetime import datetime, timedelta

# Configure logging to show in GitHub Actions
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_issues(repo, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def find_duplicates(new_issue, issues, threshold=0.8):
    duplicates = []
    new_description = new_issue["body"]
    for issue in issues:
        if issue["number"] == new_issue["number"]:
            logging.info(f"Skipping current issue #{issue['number']}")
            continue
        similarity = calculate_similarity(new_description, issue["body"])
        logging.debug(f"Similarity score for issue #{issue['number']}: {similarity}")
        if similarity >= threshold:
            duplicates.append(issue)
    return duplicates

def calculate_similarity(text1, text2):
    # Placeholder for actual similarity calculation logic
    return 0.9

def comment_on_issue(repo, issue_number, comment, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

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
    recently_closed_issues = [issue for issue in issues if issue["state"] == "closed" and datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ") > one_hundred_twenty_days_ago]
    logging.info(f"Found {len(recently_closed_issues)} recently closed issues (last 120 days)")

    duplicates = find_duplicates(new_issue, open_issues + recently_closed_issues)

    if duplicates:
        comment = "Possible duplicate issues:\n"
        for duplicate in duplicates:
            comment += f"- #{duplicate['number']}: {duplicate['title']}\n"
        comment_on_issue(repo, new_issue_number, comment, token)

if __name__ == "__main__":
    main()
