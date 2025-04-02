"""Custom exceptions for the my_chat_gpt_utils package."""


class ProblemCauseSolution(Exception):
    """
    Exception class that wraps other exceptions with Problem-Cause-Solution information.
    
    This helps provide clear guidance on what went wrong, why it happened, and how to fix it.
    """

    def __init__(self, problem: str, cause: str, solution: str, original_exception: Exception | None = None):
        """
        Initialize the exception with problem, cause, and solution information.

        Args:
            problem (str): Description of what went wrong
            cause (str): Explanation of why it happened
            solution (str): Instructions on how to fix it
            original_exception (Exception | None, optional): The original exception that caused this
        """
        self.problem = problem
        self.cause = cause
        self.solution = solution
        self.original_exception = original_exception
        super().__init__(f"{problem}\nCause: {cause}\nSolution: {solution}")


class GithubAuthenticationError(ProblemCauseSolution):
    """Exception for GitHub authentication issues."""

    def __init__(self, original_exception: Exception | None = None, problem: str | None = None, cause: str | None = None, solution: str | None = None):
        """
        Initialize the GitHub authentication error.

        Args:
            original_exception (Exception | None, optional): The original exception that caused this
            problem (str | None, optional): Custom problem description
            cause (str | None, optional): Custom cause description
            solution (str | None, optional): Custom solution description
        """
        if problem is None and cause is None and solution is None:
            super().__init__(
                problem="GitHub API request failed with 403 Forbidden",
                cause="Invalid or expired GitHub token",
                solution="Check and create a new GitHub access token at https://github.com/settings/tokens",
                original_exception=original_exception
            )
        else:
            super().__init__(
                problem=problem or "GitHub API authentication failed",
                cause=cause or "Invalid or expired GitHub token",
                solution=solution or "Check your GitHub token and ensure it has the required permissions",
                original_exception=original_exception
            )


class OpenAIAuthenticationError(ProblemCauseSolution):
    """Exception for OpenAI authentication issues."""

    def __init__(self, original_exception: Exception | None = None, problem: str | None = None, cause: str | None = None, solution: str | None = None):
        """
        Initialize the OpenAI authentication error.

        Args:
            original_exception (Exception | None, optional): The original exception that caused this
            problem (str | None, optional): Custom problem description
            cause (str | None, optional): Custom cause description
            solution (str | None, optional): Custom solution description
        """
        if problem is None and cause is None and solution is None:
            super().__init__(
                problem="OpenAI API request failed",
                cause="Invalid or expired OpenAI API key",
                solution="Check and create a new OpenAI API key at https://platform.openai.com/api-keys",
                original_exception=original_exception
            )
        else:
            super().__init__(
                problem=problem or "OpenAI API authentication failed",
                cause=cause or "Invalid or expired API key",
                solution=solution or "Check your OpenAI API key and ensure it is correctly set in the environment",
                original_exception=original_exception
            ) 