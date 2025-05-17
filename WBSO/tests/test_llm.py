import unittest
from WBSO.src.llm.client import LLMClient  # Assuming client.py is in WBSO.src.llm


class TestLLMClient(unittest.TestCase):
    def test_llm_client_creation(self):
        client = LLMClient(api_key="test_key")
        self.assertIsNotNone(client)
        self.assertEqual(client.api_key, "test_key")

    def test_generate_text_placeholder(self):
        client = LLMClient(api_key="test_key")
        prompt = "Hello, world!"
        expected_output = f"Generated text for prompt: {prompt}"
        self.assertEqual(client.generate_text(prompt), expected_output)


if __name__ == "__main__":
    unittest.main()
