"""Utilities for interacting with OpenAI's API and managing API configurations."""

import os
from dataclasses import dataclass

import openai
import requests
import yaml
from openai import OpenAI
from packaging import version

from my_chat_gpt_utils.logger import logger

# Configuration constants
DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.1
REQUIRED_OPENAI_VERSION = "1.65.2"


@dataclass
class OpenAIConfig:
    """
    Configuration for OpenAI API interactions.

    Attributes
    ----------
        api_key (str): OpenAI API key.
        model (str): LLM model to use.
        max_tokens (int): Maximum tokens for completion.
        temperature (float): Sampling temperature for generation.

    """

    api_key: str
    model: str = DEFAULT_LLM_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE


class OpenAIVersionChecker:
    """Utility for checking OpenAI library version compatibility."""

    @staticmethod
    def check_library_version() -> bool:
        """
        Validate the installed OpenAI library version.

        Returns
        -------
            bool: True if version is compatible, False otherwise.

        """
        try:
            current_version = version.parse(openai.__version__)
            required_version = version.parse(REQUIRED_OPENAI_VERSION)

            if current_version < required_version:
                logger.warning(
                    f"Outdated OpenAI library version. "
                    f"Current: {current_version}, Required: {required_version}. "
                    "Please upgrade using: pip install --upgrade openai"
                )
                return False
            return True
        except Exception as e:
            logger.error(f"Version check failed: {e}")
            return False


class OpenAIValidator:
    """Validates OpenAI API key and permissions."""

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate the OpenAI API key's permissions.

        Args:
        ----
            api_key (str): OpenAI API key to validate.

        Returns:
        -------
            bool: True if key is valid, False otherwise.

        """
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.openai.com/v1/models", headers=headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False


def parse_openai_response(response_content: str):
    """
    Parse the OpenAI API response content as YAML.

    Args:
    ----
        response_content (str): The response content from OpenAI API.

    Returns:
    -------
        dict: Parsed YAML content as a dictionary.
        text: The response content if parsing fails.

    """
    try:
        response_content = response_content.strip("`")  # remove markdown open/close tags
        return yaml.safe_load(response_content)
    except yaml.YAMLError as e:
        logger.warning(f"YAML parsing failed: {e}")
        return response_content


def make_openai_api_call(api_key: str, model: str, messages: list, temperature: float, max_tokens: int):
    """
    Make an OpenAI API call to generate a response.

    Args:
    ----
        api_key (str): OpenAI API key.
        model (str): LLM model to use.
        messages (list): List of messages for the chat completion.
        temperature (float): Sampling temperature for generation.
        max_tokens (int): Maximum tokens for completion.

    Returns:
    -------
        str: The response content from OpenAI API.

    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        raise


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def validate_openai_config() -> None:
    """Validate OpenAI API key and library version."""
    try:
        client = get_openai_client()
        # Test the API key by making a simple request
        client.models.list()
        logger.info("OpenAI configuration validated successfully")
    except Exception as e:
        logger.error(f"OpenAI configuration validation failed: {e}")
        raise


def main() -> None:
    """Validate OpenAI configuration and API key."""
    validate_openai_config()


if __name__ == "__main__":
    main()
