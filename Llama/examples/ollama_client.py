"""
Client for interacting with the Ollama API.

This module provides a Python client for the Ollama API, allowing users to
generate text using various language models through Ollama's local API endpoint.
"""

import json
from typing import Generator, List, Optional

import requests


class OllamaClient:
    """
    Client for interacting with Ollama's API.

    This class provides methods to check Ollama's status, list available models,
    and generate text using the specified model.

    Attributes
    ----------
        base_url (str): Base URL for the Ollama API.
        version (str): Version of the running Ollama instance.
        available_models (List[str]): List of available models.

    """

    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama client.

        Args:
        ----
            base_url (str, optional): Base URL for the Ollama API.
                Defaults to "http://localhost:11434".

        Raises:
        ------
            ConnectionError: If Ollama is not running.
            Exception: If there's an error checking Ollama status.

        """
        self.base_url = base_url
        self._check_ollama_status()
        self.available_models = self._get_available_models()

    def _check_ollama_status(self) -> None:
        """Check if Ollama is running and get its version."""
        try:
            response = requests.get(f"{self.base_url}/api/version")
            response.raise_for_status()
            self.version = response.json()["version"]
            print(f"Ollama is running (version {self.version})")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Ollama is not running. Please start Ollama first.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error checking Ollama status: {e}")

    def _get_available_models(self) -> List[str]:
        """Get list of available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model["name"] for model in response.json()["models"]]
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch available models: {e}")
            return []

    def generate(
        self,
        prompt: str,
        model: str = "llama3.1:8b",
        stream: bool = False,
        temperature: float = 0.1,
        top_p: float = 0.9,
    ) -> Optional[str]:
        """Generate a response from the model."""
        if model not in self.available_models:
            print(f"Error: Model '{model}' not found. Available models: {', '.join(self.available_models)}")
            return None

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {"temperature": temperature, "top_p": top_p},
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 404:
                print(f"Error: Model '{model}' not found. Available models: {', '.join(self.available_models)}")
                return None
            response.raise_for_status()

            if stream:
                return self._handle_stream(response)
            else:
                return response.json()["response"]

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def _handle_stream(self, response: requests.Response) -> Generator[str, None, None]:
        """Handle streaming responses."""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    yield chunk["response"]
                except json.JSONDecodeError:
                    continue


def main():
    """
    Run example usage of the OllamaClient.

    Demonstrates creating a client, listing available models,
    and generating both streaming and non-streaming responses.
    """
    try:
        # Create client (this will check Ollama status and available models)
        client = OllamaClient()

        # Print available models
        print(f"Available models: {', '.join(client.available_models)}")

        # Generate response
        response = client.generate("What is the capital of France?")
        if response:
            print(response)

        # Test streaming
        print("\nTesting streaming response:")
        for chunk in client.generate("Tell me a short story", stream=True):
            print(chunk, end="", flush=True)
        print()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
