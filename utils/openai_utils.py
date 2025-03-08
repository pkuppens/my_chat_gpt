import openai
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def parse_openai_response(response_content: str):
    """
    Parse the OpenAI API response content as YAML.

    Args:
        response_content (str): The response content from OpenAI API.

    Returns:
        dict: Parsed YAML content as a dictionary.
    """
    try:
        return yaml.safe_load(response_content)
    except yaml.YAMLError as e:
        logger.warning(f"YAML parsing failed: {e}")
        return None

def make_openai_api_call(api_key: str, model: str, messages: list, temperature: float, max_tokens: int):
    """
    Make an OpenAI API call to generate a response.

    Args:
        api_key (str): OpenAI API key.
        model (str): LLM model to use.
        messages (list): List of messages for the chat completion.
        temperature (float): Sampling temperature for generation.
        max_tokens (int): Maximum tokens for completion.

    Returns:
        str: The response content from OpenAI API.
    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        raise
