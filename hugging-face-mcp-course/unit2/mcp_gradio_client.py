import json
import logging
from typing import Any, Dict, Optional

import gradio as gr
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_mcp_config() -> Optional[Dict[str, Any]]:
    """Load MCP configuration from config file."""
    import os

    # Try multiple possible locations for the config file
    possible_paths = [
        "mcp-config.json",  # Current directory
        "hugging-face-mcp-course/unit2/mcp-config.json",  # From project root
        os.path.join(os.path.dirname(__file__), "mcp-config.json"),  # Same directory as this script
    ]

    for config_path in possible_paths:
        try:
            if os.path.exists(config_path):
                logger.info(f"Loading MCP config from: {config_path}")
                with open(config_path, "r") as f:
                    config = json.load(f)
                return config["servers"][0]
        except Exception as e:
            logger.debug(f"Failed to load config from {config_path}: {e}")
            continue

    logger.error(f"Could not find mcp-config.json in any of these locations: {possible_paths}")
    return None


def call_gradio_api_directly(text: str, server_url: str = "http://localhost:7860") -> dict:
    """
    Call the Gradio API directly to get sentiment analysis.

    Args:
        text (str): The text to analyze
        server_url (str): The base URL of the Gradio server

    Returns:
        dict: The sentiment analysis results
    """
    try:
        # Try different Gradio API endpoints (newer versions use different paths)
        api_endpoints = [
            f"{server_url}/gradio_api/run/predict",
            f"{server_url}/gradio_api/call/sentiment_analysis",
            f"{server_url}/run/predict",
            f"{server_url}/api/predict",
            f"{server_url}/call/sentiment_analysis",
        ]

        # Prepare the request payload
        payload = {
            "data": [text],  # Gradio expects data as a list
            "fn_index": 0,  # Index of the function (usually 0 for single function interfaces)
        }

        last_error = None

        # Try each endpoint until one works
        for api_url in api_endpoints:
            try:
                # Make the API call
                response = requests.post(api_url, json=payload, timeout=30)
                response.raise_for_status()

                # Parse the response
                result = response.json()

                # Extract the data from Gradio's response format
                if "data" in result and len(result["data"]) > 0:
                    return result["data"][0]  # Return the sentiment analysis result
                else:
                    return {"error": "No data returned from server", "polarity": 0, "subjectivity": 0, "assessment": "error"}

            except requests.exceptions.HTTPError as e:
                last_error = f"HTTP {e.response.status_code} at {api_url}"
                continue  # Try next endpoint
            except Exception as e:
                last_error = f"Error at {api_url}: {str(e)}"
                continue  # Try next endpoint

        # If we get here, all endpoints failed
        return {
            "error": f"All API endpoints failed. Last error: {last_error}",
            "polarity": 0,
            "subjectivity": 0,
            "assessment": "error",
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to MCP server. Make sure the server is running at http://localhost:7860",
            "polarity": 0,
            "subjectivity": 0,
            "assessment": "error",
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The server took too long to respond.",
            "polarity": 0,
            "subjectivity": 0,
            "assessment": "error",
        }
    except Exception as e:
        return {"error": f"Failed to call server: {str(e)}", "polarity": 0, "subjectivity": 0, "assessment": "error"}


def test_server_connection(server_url: str = "http://localhost:7860") -> bool:
    """
    Test if the MCP server is running and accessible.

    Args:
        server_url (str): The base URL of the server

    Returns:
        bool: True if server is accessible, False otherwise
    """
    try:
        # Try to access the server's main page
        response = requests.get(server_url, timeout=5)
        return response.status_code == 200
    except:
        return False


def sentiment_client_interface(text: str) -> str:
    """
    Interface function for the Gradio client that calls the MCP server.

    Args:
        text (str): The text to analyze

    Returns:
        str: Formatted sentiment analysis results
    """
    if not text.strip():
        return "Please enter some text to analyze."

    # Load configuration
    server_config = load_mcp_config()
    if not server_config:
        return "❌ Error: Could not load MCP configuration. Make sure mcp-config.json exists."

    # Extract server URL from config (remove the /gradio_api/mcp/sse part for direct API calls)
    server_url = server_config["transport"]["url"].replace("/gradio_api/mcp/sse", "")

    # Test server connection first
    if not test_server_connection(server_url):
        return f"❌ Error: Cannot connect to MCP server at {server_url}. Make sure the server is running."

    # Call the sentiment analysis
    result = call_gradio_api_directly(text, server_url)

    # Format the results in a user-friendly way
    if "error" in result:
        return f"❌ Error: {result['error']}"

    polarity = result.get("polarity", 0)
    subjectivity = result.get("subjectivity", 0)
    assessment = result.get("assessment", "unknown")

    # Create emoji indicators
    if assessment == "positive":
        emoji = "😊"
    elif assessment == "negative":
        emoji = "😞"
    else:
        emoji = "😐"

    # Format the response
    formatted_result = f"""
{emoji} **Sentiment Assessment: {assessment.upper()}**

📊 **Detailed Analysis:**
• **Polarity**: {polarity} (Range: -1 to +1)
• **Subjectivity**: {subjectivity} (Range: 0 to 1)

💡 **Interpretation:**
• Polarity indicates how positive or negative the text is
• Subjectivity indicates how objective or subjective the text is
• Values closer to 0 are more neutral/objective

🔗 **Connection Info:**
• Server URL: {server_url}
• Protocol: HTTP API (via MCP-enabled Gradio server)
"""

    return formatted_result.strip()


def get_server_status() -> str:
    """Get the current status of the MCP server."""
    server_config = load_mcp_config()
    if not server_config:
        return "❌ Configuration not found"

    server_url = server_config["transport"]["url"].replace("/gradio_api/mcp/sse", "")

    if test_server_connection(server_url):
        return f"✅ Server is running at {server_url}"
    else:
        return f"❌ Server is not accessible at {server_url}"


# Create the Gradio interface for the MCP client
with gr.Blocks(title="Gradio MCP Client - Sentiment Analysis") as client_demo:
    gr.Markdown("# 🔗 Gradio MCP Client - Sentiment Analysis")

    gr.Markdown(
        """
    This is a Gradio MCP client that connects to our sentiment analysis MCP server.

    **How it works:**
    1. You enter text in the input box
    2. The client sends the text to the MCP server via HTTP API calls
    3. The server analyzes the sentiment using TextBlob
    4. The results are displayed in a user-friendly format

    **Note:** Make sure the sentiment analysis server is running at http://localhost:7860
    """
    )

    # Server status section
    with gr.Row():
        with gr.Column(scale=3):
            status_display = gr.Textbox(
                label="Server Status", value="Click 'Check Status' to verify server connection", interactive=False
            )
        with gr.Column(scale=1):
            status_btn = gr.Button("Check Status", variant="secondary")

    # Main interface
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to Analyze", placeholder="Enter text to analyze sentiment via MCP server...", lines=3
            )

            analyze_btn = gr.Button("Analyze Sentiment", variant="primary")

        with gr.Column():
            output_display = gr.Markdown(label="Sentiment Analysis Results", value="Results will appear here after analysis...")

    # Examples section
    gr.Markdown("### Example Texts to Try:")
    example_buttons = []
    examples = [
        "I absolutely love this new feature! It's amazing!",
        "This is the worst experience I've ever had.",
        "The weather today is partly cloudy with a chance of rain.",
        "I'm not sure how I feel about this change.",
    ]

    with gr.Row():
        for i, example in enumerate(examples):
            btn = gr.Button(f"Example {i + 1}", size="sm")
            example_buttons.append(btn)
            btn.click(lambda ex=example: ex, outputs=text_input)

    # Technical details section
    with gr.Accordion("Technical Details", open=False):
        gr.Markdown(
            """
        ### MCP Client Implementation Details

        This client demonstrates how to connect to an MCP-enabled Gradio server:

        1. **Configuration**: Reads server details from `mcp-config.json`
        2. **Connection**: Uses HTTP API calls to communicate with the Gradio server
        3. **Error Handling**: Provides detailed error messages and connection status
        4. **Response Formatting**: Converts server responses into user-friendly format

        The MCP (Model Context Protocol) enables standardized communication between
        AI tools and services, making it easy to integrate different components.
        """
        )

    # Event handlers
    status_btn.click(get_server_status, outputs=status_display)
    analyze_btn.click(sentiment_client_interface, inputs=text_input, outputs=output_display)
    text_input.submit(sentiment_client_interface, inputs=text_input, outputs=output_display)


# Launch the client interface
if __name__ == "__main__":
    print("🚀 Starting Gradio MCP Client...")
    print("📡 This client will connect to the MCP server at: http://localhost:7860")
    print("🌐 Client interface will be available at: http://localhost:7861")
    print()
    print("Make sure to start the MCP server first by running:")
    print("  uv run hugging-face-mcp-course/unit2/sentiment_analysis_mcp_server.py")
    print()

    # Launch on a different port to avoid conflicts with the server
    client_demo.launch(server_port=7861, share=False, show_error=True, server_name="0.0.0.0")  # Allow access from other machines
