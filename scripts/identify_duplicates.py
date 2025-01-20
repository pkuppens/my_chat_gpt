import os
import requests

def get_issues(repo, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def find_duplicates(new_issue, issues):
    duplicates = []
    new_description = new_issue["body"]
    for issue in issues:
        if issue["number"] == new_issue["number"]:
            continue
        if new_description in issue["body"]:
            duplicates.append(issue)
    return duplicates

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

    issues = get_issues(repo, token)
    new_issue = next(issue for issue in issues if issue["number"] == int(new_issue_number))
    duplicates = find_duplicates(new_issue, issues)

    if duplicates:
        comment = "Possible duplicate issues:\n"
        for duplicate in duplicates:
            comment += f"- #{duplicate['number']}: {duplicate['title']}\n"
        comment_on_issue(repo, new_issue_number, comment, token)

if __name__ == "__main__":
    main()
