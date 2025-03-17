# Retrieving and Using an OpenAI API Key Securely

## Purpose

This guide explains how to securely retrieve, store, and use an **OpenAI API key** in Python.  
It also includes error handling for missing, incorrect, or expired API keys by validating access before making requests.

## Steps to Obtain the API Key

1. **Log in to OpenAI**  
   - Go to [OpenAI's API platform](https://platform.openai.com/).
   - Log in with your OpenAI account.

2. **Generate an API Key**  
   - Navigate to **API Keys** and click **Create a new secret key**.
   - Give the key a descriptive name (e.g., `my_app_key`).
   - **Copy the key immediately**, as it will not be displayed again.

3. **Store the API Key Securely**  
   - **Do not hardcode** the key in your code. Instead, store it in:
     - A `.env` file (recommended for local development)
     - System environment variables (recommended for production)

## Storing the API Key Securely

### Option 1: Using a `.env` File

1. **Create a `.env` File**  
   - In your project directory, create a file named `.env`.
   - Add the following line:

     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

   - **Ensure the `.env` file is included in `.gitignore`** to prevent accidental exposure.

2. **Install `python-dotenv`**  

   ```bash
   pip install python-dotenv
   ```

3. **Load the API Key in Python**  

   ```python
   import os
   from dotenv import load_dotenv

   # Load environment variables from .env file
   load_dotenv()

   # Retrieve the OpenAI API key
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

   if not OPENAI_API_KEY:
       raise ValueError("OpenAI API key is missing. Set it in the .env file or environment variables.")
   ```

### Option 2: Using Windows Environment Variables

1. **Set the Environment Variable**  
   - Open **Start** → search for **Environment Variables** → **Edit the system environment variables**.
   - Click **Environment Variables**.
   - Under **User variables**, click **New** and add:

     ```
     Variable name: OPENAI_API_KEY
     Variable value: your_openai_api_key
     ```

2. **Load the API Key in Python**  

   ```python
   import os

   # Retrieve the OpenAI API key from system environment variables
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

   if not OPENAI_API_KEY:
       raise ValueError("OpenAI API key is missing. Set it in the environment variables.")
   ```

## Validating the API Key

Before making chat requests, validate the API key by fetching available models:

```python
import openai
from openai.error import AuthenticationError, OpenAIError

def validate_api_key():
    """Validates the OpenAI API key by listing available models."""
    try:
        models = openai.Model.list()
        print("API key is valid. Available models:")
        for model in models['data']:
            print(model['id'])
    except AuthenticationError:
        print("Authentication failed: check your API key.")
        raise
    except OpenAIError as e:
        print(f"An error occurred: {e}")
        raise

# Validate API key before usage
validate_api_key()
```

## Making a Chat Completion Request with Error Handling

This example sends a chat request while handling authentication, invalid requests, and rate limits:

```python
from openai.error import AuthenticationError, InvalidRequestError, RateLimitError, OpenAIError

def create_chat_completion(messages):
    """Creates a chat completion request with error handling."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message['content'].strip()
    except AuthenticationError:
        print("Authentication failed: check your API key.")
        raise
    except InvalidRequestError as e:
        print(f"Invalid request: {e}")
        raise
    except RateLimitError:
        print("Rate limit exceeded: please try again later.")
        raise
    except OpenAIError as e:
        print(f"An error occurred: {e}")
        raise

# Example usage
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! How can you assist me today?"}
]

try:
    response = create_chat_completion(messages)
    print(response)
except Exception as e:
    print(f"Chat request failed: {e}")
```

## Security Best Practices

- **Do not hardcode API keys in source code.** Always use environment variables or a `.env` file.
- **Rotate API keys periodically.** Revoke old keys and generate new ones in the OpenAI dashboard.
- **Monitor API usage.** Check the OpenAI dashboard for usage statistics and cost tracking.
- **Use API key restrictions.** If OpenAI offers IP or domain restrictions, consider enabling them.

## References

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [OpenAI Python Library (GitHub)](https://github.com/openai/openai-python)
- [OpenAI Error Handling Guide](https://help.openai.com/en/articles/6897213-openai-library-error-types-guidance)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agent Patterns](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns)
