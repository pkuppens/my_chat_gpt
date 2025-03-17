"""
Basic example of using Ollama with Python.
This example demonstrates basic model interaction, streaming, and error handling.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.ollama_client import OllamaClient

def main():
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
