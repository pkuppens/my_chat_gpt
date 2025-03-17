# Creating and Using a GitHub Fine-Grained Personal Access Token for Repository Management

## Purpose

This guide details the steps to create a fine-grained personal access token (PAT) for interacting
with the `pkuppens/my_chat_gpt` repository using **PyGithub**. The token will:

- **Read and modify issues**
- **Comment on issues**
- **Read and write repository files** (optional, depending on your requirements)
- **Manage pull request reviews and comments** (optional)
- **Inspect repository actions** (optional)

## Steps to Create the Token

1. **Open GitHub and Navigate to Developer Settings**

   - Click on your profile picture in the upper-right corner.
   - Select **Settings**.
   - **Scroll down** and click **Developer settings** (it is not immediately visible).

2. **Create a Fine-Grained Personal Access Token**

   - In the left sidebar, select **Personal access tokens** → **Fine-grained tokens**.
   - Click **Generate new token**.
   - Set a **Token name** (e.g., `repo_management_token`).
   - Choose an **Expiration date** (recommended for security).

3. **Configure Repository Access**

   - Under **Resource Owner**, select your GitHub username.
   - Under **Repository Access**, choose **Only select repositories**, then select `pkuppens/my_chat_gpt`.

4. **Set Required Permissions**

   - Under **Repository permissions**, set:
     - **Issues** → **Read and write** (to read and modify issues)
     - **Contents** → **Read and write** (to read and write repository files; optional, enable if needed)
     - **Pull requests** → **Read and write** (to manage pull request reviews and comments; optional, enable if needed)
     - **Actions** → **Read** (to inspect repository actions; optional, enable if needed)

5. **Generate and Store the Token**

   - Click **Generate token**.
   - **Copy the token immediately**, as you won't be able to see it again.

## Storing the Token Securely

### Using a `.env` File

1. **Create a `.env` File**

   - In your project directory, create a file named `.env`.
   - Add the following line to the `.env` file:

     ```
     GITHUB_TOKEN=your_generated_token
     ```

   - **Ensure** that the `.env` file is added to your `.gitignore` to prevent it from being committed to version control.

2. **Install `python-dotenv`**

   - Install the `python-dotenv` package to load environment variables from the `.env` file:

     ```bash
     pip install python-dotenv
     ```

3. **Load the Token in Your Python Script**

   - Use the following code to load the token:

     ```python
     from github import Github
     import os
     from dotenv import load_dotenv

     # Load environment variables from .env file
     load_dotenv()

     # Retrieve the token from environment variables
     TOKEN = os.getenv('GITHUB_TOKEN')

     # Authenticate with PyGithub
     g = Github(TOKEN)

     # Access the repository
     repo = g.get_repo("pkuppens/my_chat_gpt")

     # Example: List issues
     for issue in repo.get_issues():
         print(f"Issue #{issue.number}: {issue.title}")
     ```

### Using Windows Environment Variables

1. **Set the Environment Variable**

   - Open the **Start** menu, search for "Environment Variables," and select **Edit the system environment variables**.
   - Click **Environment Variables**.
   - Under **User variables**, click **New** and add:

     ```
     Variable name: GITHUB_TOKEN
     Variable value: your_generated_token
     ```

2. **Load the Token in Your Python Script**

   - Use the following code to retrieve the token:

     ```python
     from github import Github
     import os

     # Retrieve the token from environment variables
     TOKEN = os.getenv('GITHUB_TOKEN')

     # Authenticate with PyGithub
     g = Github(TOKEN)

     # Access the repository
     repo = g.get_repo("pkuppens/my_chat_gpt")

     # Example: List issues
     for issue in repo.get_issues():
         print(f"Issue #{issue.number}: {issue.title}")
     ```

## Additional Permissions and Recommendations

Depending on your use cases, consider enabling the following permissions:

- **Pull requests** → **Read and write**: Allows managing pull request reviews and comments. Enable if your application needs to interact with pull requests.

- **Actions** → **Read**: Allows inspecting repository actions. Enable if you need to monitor or analyze GitHub Actions workflows.

**Recommendation:** Enable only the permissions necessary for your application's functionality to adhere to the principle of least privilege, enhancing security.

## References

For more details, refer to [GitHub's official documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
