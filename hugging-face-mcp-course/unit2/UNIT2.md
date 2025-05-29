# Unit 2: Building an End-to-End MCP Application

## Overview

In Unit 2, we'll build a complete MCP application from scratch, focusing on creating a sentiment analysis server with Gradio and connecting it with multiple clients. This hands-on approach provides practical experience with the entire MCP ecosystem.

### Learning Objectives

By the end of this unit, you will:

- Create an MCP Server using Gradio's built-in MCP support
- Build a sentiment analysis tool that can be used by AI models
- Connect to the server using different client implementations
- Deploy your MCP Server to Hugging Face Spaces
- Test and debug the complete system

### Prerequisites Verification

- [x] **Python 3.12+** installed and verified (3.12.8)
- [x] **Node.js 22+** installed and verified (v22.11.0)
- [x] **Hugging Face account** created
- [x] **UV package manager** available/activated (shared environment approach)
- [x] **Basic understanding** of MCP concepts from Unit 1

## Task 1: Project Setup and Environment

### Task 1.1: Project Structure Setup

- [x] **Subtask 1.1.1**: Create project directory structure

  ```bash
  # Create the unit2 directory structure for our MCP application
  # This will house all our server and client implementations
  mkdir -p hugging-face-mcp-course/unit2
  cd hugging-face-mcp-course/unit2
  ```

- [x] **Subtask 1.1.2**: Install required dependencies in shared UV environment

  ```bash
  # Using shared UV environment (no separate venv)
  # gradio[mcp] - Gradio with MCP server capabilities
  # textblob - Natural language processing library for sentiment analysis
  # smolagents - Hugging Face agents framework for MCP client implementation
  uv add "gradio[mcp]" textblob smolagents
  ```

- [x] **Subtask 1.1.3**: Verify installations
  ```bash
  # Verify that all required packages are properly installed
  # These commands should run without errors and display version/availability info
  uv run python -c "import gradio; print('Gradio version:', gradio.__version__)"
  uv run python -c "import textblob; print('TextBlob available')"
  uv run python -c "import smolagents; print('SmolAgents available')"
  ```

**Implementation Notes:**

```
Decision: Using shared UV environment rather than separate venv per project
Rationale: Simplifies dependency management across units
Status: [x] Complete
Issues encountered:

```

### Task 1.2: TextBlob Setup

TextBlob is a Python library for processing textual data that provides a simple API for common natural language processing (NLP) tasks. For this project, we'll use it specifically for sentiment analysis, which helps determine the emotional tone of text by analyzing its polarity (positive/negative) and subjectivity (objective/subjective).

Official documentation: [TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)

- [x] **Subtask 1.2.1**: Download TextBlob corpora

  - Download required NLTK data for TextBlob

  - punkt: Tokenizer models for sentence splitting

  - brown: Corpus for training and testing

  ```bash
  # Download essential NLTK corpora that TextBlob depends on
  # punkt: Pre-trained tokenizer for splitting text into sentences
  # brown: Brown Corpus for training statistical models
  uv run python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
  ```

- [x] **Subtask 1.2.2**: Test TextBlob functionality
  ```bash
  # Test that TextBlob sentiment analysis is working correctly
  # Expected output: Sentiment(polarity=0.625, subjectivity=0.6)
  # polarity: -1 (negative) to 1 (positive)
  # subjectivity: 0 (objective) to 1 (subjective)
  uv run python -c "
  from textblob import TextBlob
  blob = TextBlob('I love this course!')
  print('Sentiment:', blob.sentiment)
  "
  >>> Sentiment: Sentiment(polarity=0.625, subjectivity=0.6)
  ```

## Task 2: MCP Server Development

### Task 2.1: Basic Sentiment Analysis Server

- [x] **Subtask 2.1.1**: Create sentiment_analysis_mcp_server.py file

  ```bash
  # Create the main server file that will contain our MCP server implementation
  touch hugging-face-mcp-course/unit2/sentiment_analysis_mcp_server.py
  ```

- [x] **Subtask 2.1.2**: Implement sentiment analysis function

  - [x] Step 2.1.2.1: Define function with proper type hints
  - [x] Step 2.1.2.2: Add comprehensive docstring with Args section
  - [x] Step 2.1.2.3: Implement TextBlob sentiment analysis
  - [x] Step 2.1.2.4: Return structured dictionary with polarity, subjectivity, assessment

- [x] **Subtask 2.1.3**: Create Gradio interface
  - [x] Step 2.1.3.1: Set up gr.Interface with textbox input
  - [x] Step 2.1.3.2: Configure JSON output component
  - [x] Step 2.1.3.3: Add appropriate title and description
  - [x] Step 2.1.3.4: Enable MCP server with `mcp_server=True`

**Code Implementation:**

```python
# sentiment_analysis_mcp_server.py implementation
import gradio as gr
from textblob import TextBlob

def sentiment_analysis(text: str) -> dict:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        dict: A dictionary containing polarity, subjectivity, and assessment
    """
    # Create TextBlob object for sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment

    # Return structured data that MCP clients can easily consume
    return {
        "polarity": round(sentiment.polarity, 2),  # -1 (negative) to 1 (positive)
        "subjectivity": round(sentiment.subjectivity, 2),  # 0 (objective) to 1 (subjective)
        "assessment": "positive" if sentiment.polarity > 0 else "negative" if sentiment.polarity < 0 else "neutral"
    }

# Create the Gradio interface that will serve as both web UI and MCP server
demo = gr.Interface(
    fn=sentiment_analysis,  # The function to expose as an MCP tool
    inputs=gr.Textbox(placeholder="Enter text to analyze..."),  # Input component with helpful placeholder
    outputs=gr.JSON(),  # JSON output for structured data display
    title="Text Sentiment Analysis",  # Title shown in web interface
    description="Analyze the sentiment of text using TextBlob"  # Description for users
)

# Launch the interface and MCP server
if __name__ == "__main__":
    # mcp_server=True enables the MCP server alongside the web interface
    # This makes the sentiment_analysis function available as an MCP tool
    demo.launch(mcp_server=True)
```

### Task 2.2: Server Testing and Validation

- [x] **Subtask 2.2.1**: Local server testing

  ```bash
  # Run the sentiment analysis server
  # This starts both the Gradio web interface and the MCP server
  # Web interface: http://localhost:7860
  # MCP server: http://localhost:7860/gradio_api/mcp/sse
  uv run hugging-face-mcp-course/unit2/sentiment_analysis_mcp_server.py
  ```

- [x] **Subtask 2.2.2**: Web interface validation

  - [x] Step 2.2.2.1: Access http://localhost:7860
  - [x] Step 2.2.2.2: Test with positive text: "I love this!"
  - [x] Step 2.2.2.3: Test with negative text: "This is terrible"
  - [x] Step 2.2.2.4: Test with neutral text: "The sky is blue"

  Note: It doesn't recognize subtle sarcasm:
  This restaurant is great if you enjoy your food being cooked by friendly puppies with no taste nor cooking skill.
  Scores polarity: 0.53 / positive.

- [x] **Subtask 2.2.3**: MCP endpoints verification

  More or less expected when the previous test succeeds.

  ```bash
  # Test MCP schema endpoint - shows available tools and their schemas
  # This endpoint returns JSON describing the sentiment_analysis tool
  curl http://localhost:7860/gradio_api/mcp/schema

  # Test MCP SSE endpoint (should establish connection)
  # This is the main MCP communication endpoint using Server-Sent Events
  curl http://localhost:7860/gradio_api/mcp/sse
  ```

## Task 3: MCP Client Development

<!-- Task Group 3 builds various types of MCP clients that can connect to and use our sentiment analysis server.
     This demonstrates the client side of the MCP protocol and shows how different frameworks can integrate with MCP. -->

### Task 3.1: MCP Configuration Setup

**What we're building**: A standardized configuration file that defines how MCP clients discover and connect to our sentiment analysis server.

**User benefits**:

- Centralized server configuration that can be shared across multiple clients
- Easy switching between development and production environments
- Standardized connection parameters for consistent client behavior

- [x] **Subtask 3.1.1**: Create MCP configuration file

  ```bash
  # Create configuration file that defines how clients connect to MCP servers
  # This file will be used by various MCP clients to discover and connect to servers
  touch hugging-face-mcp-course/unit2/mcp-config.json
  ```

- [x] **Subtask 3.1.2**: Define server configuration
  ```json
  {
    "servers": [
      {
        "name": "Sentiment Analysis MCP Server", // Human-readable name for the server
        "transport": {
          "type": "sse", // Server-Sent Events transport protocol
          "url": "http://localhost:7860/gradio_api/mcp/sse" // MCP server endpoint
        }
      }
    ]
  }
  ```

### Task 3.2: Gradio MCP Client Implementation

**What we're building**: A Gradio web application that connects to our MCP sentiment analysis server, providing an interactive interface for testing and experimenting with the MCP connection.

**User benefits**:

- Visual web interface for testing MCP server functionality without writing code
- Real-time feedback on MCP tool calls and responses
- Easy demonstration of MCP capabilities to stakeholders
- Debugging interface to verify server-client communication

- [x] **Subtask 3.2.1**: Create Gradio client file

  ```bash
  # Create a Gradio-based MCP client that can connect to our sentiment server
  # This demonstrates how Gradio can be used as both server and client in MCP
  touch hugging-face-mcp-course/unit2/gradio_client.py
  ```

- [x] **Subtask 3.2.2**: Implement Gradio MCP client

  - [x] Step 3.2.2.1: Import required Gradio MCP modules
    - **Implementation hint**: `from gradio_client import Client` and `import gradio as gr`
  - [x] Step 3.2.2.2: Configure MCP server connection
    - **Implementation hint**: Use `Client("http://localhost:7860")` to connect to the MCP server
  - [x] Step 3.2.2.3: Create client interface with text input
    - **Implementation hint**: `gr.Interface()` with `gr.Textbox()` for user input
  - [x] Step 3.2.2.4: Implement function to call MCP server
    - **Implementation hint**: Use `client.predict()` method to call the sentiment analysis function
  - [x] Step 3.2.2.5: Display results in user-friendly format
    - **Implementation hint**: Format JSON response into readable text or use `gr.JSON()` component

- [x] **Subtask 3.2.3**: Test Gradio client functionality
  ```bash
  # Run the Gradio MCP client
  # This should start a new Gradio interface that connects to our sentiment server
  # Users can input text and see sentiment analysis results from the MCP server
  uv run hugging-face-mcp-course/unit2/mcp_gradio_client.py
  ```

**Client Implementation Notes:**

```
Gradio Client Development:
- MCP connection established: [x] Success / [ ] Issues
- Tool discovery working: [x] Yes / [ ] No
- Sentiment analysis calls successful: [x] Yes / [ ] No
- Error handling implemented: [x] Yes / [ ] No

```

### Task 3.3: Python SmolAgents Client

**What we're building**: An AI agent using Hugging Face's SmolAgents framework that can automatically use our sentiment analysis MCP tool to respond to natural language queries about text sentiment.

**About SmolAgents**: SmolAgents is Hugging Face's lightweight framework for building AI agents that can use tools and reason about tasks. It provides a simple way to create agents that can automatically select and use appropriate tools based on user queries.

**Reference**: [SmolAgents Documentation](https://huggingface.co/docs/smolagents)

**User benefits**:

- Natural language interface - users can ask questions like "What's the sentiment of this review?" instead of using structured API calls
- Automatic tool selection - the agent decides when to use sentiment analysis based on context
- Conversational interaction - users can have back-and-forth discussions about sentiment analysis results
- Integration with Hugging Face ecosystem - easy access to models and other HF tools

- [ ] **Subtask 3.3.1**: Create SmolAgents client file

  ```bash
  # Create a SmolAgents-based MCP client
  # SmolAgents is Hugging Face's framework for building AI agents
  # This will create an agent that can use our sentiment analysis tool
  touch hugging-face-mcp-course/unit2/smolagents_client.py
  ```

- [ ] **Subtask 3.3.2**: Implement SmolAgents MCP client

  - [ ] Step 3.3.2.1: Import SmolAgents MCP modules
    - **Implementation hint**: First install with `uv add smolagents`, then `from smolagents import CodeAgent, MCPTool`
  - [ ] Step 3.3.2.2: Configure agent with MCP server
    - **Implementation hint**: Create `MCPTool` instance pointing to `http://localhost:7860/gradio_api/mcp/sse`
  - [ ] Step 3.3.2.3: Create agent instance with sentiment analysis tool
    - **Implementation hint**: `agent = CodeAgent(tools=[mcp_tool])` to initialize agent with MCP tool
  - [ ] Step 3.3.2.4: Implement test queries
    - **Implementation hint**: Use `agent.run("Analyze the sentiment of: 'I love this product!'")` for testing
  - [ ] Step 3.3.2.5: Add error handling and logging
    - **Implementation hint**: Wrap agent calls in try-except blocks and use `logging` module for debugging

- [ ] **Subtask 3.3.3**: Test SmolAgents client
  ```bash
  # Run the SmolAgents MCP client
  # This creates an AI agent that can automatically use sentiment analysis
  # The agent can respond to natural language queries about text sentiment
  uv run hugging-face-mcp-course/unit2/smolagents_client.py
  ```

**SmolAgents Implementation Notes:**

```
SmolAgents Client Development:
- Agent initialization: [ ] Success / [ ] Issues
- MCP tool registration: [ ] Success / [ ] Issues
- Query processing: [ ] Success / [ ] Issues
- Results accuracy: [ ] Verified / [ ] Issues found

```

### Task 3.4: JavaScript/TypeScript Client (Optional)

- [ ] **Subtask 3.4.1**: Set up Node.js environment

  ```bash
  # If Node.js client needed
  # Set up a JavaScript/TypeScript environment for web-based MCP client
  cd hugging-face-mcp-course/unit2
  npm init -y  # Initialize package.json
  npm install @huggingface/hub @huggingface/inference  # Install Hugging Face JS libraries
  ```

- [ ] **Subtask 3.4.2**: Create TypeScript client

  ```bash
  # Create a TypeScript/JavaScript MCP client
  # This demonstrates browser-based MCP integration
  touch hugging-face-mcp-course/unit2/typescript_client.ts
  ```

- [ ] **Subtask 3.4.3**: Implement and test TypeScript client

**JavaScript Client Notes:**

```
TypeScript Client (if implemented):
- Client setup: [ ] Complete / [ ] Skipped
- MCP connection: [ ] Success / [ ] Issues
- Tool integration: [ ] Working / [ ] Issues

```

## Task Group 4: Deployment and Production

### Task 4.1: Hugging Face Spaces Deployment

- [ ] **Subtask 4.1.1**: Create requirements.txt for deployment

  ```bash
  # Generate requirements file for Hugging Face Spaces deployment
  # This ensures all dependencies are available in the cloud environment
  echo "gradio[mcp]" > hugging-face-mcp-course/unit2/requirements.txt
  echo "textblob" >> hugging-face-mcp-course/unit2/requirements.txt
  ```

- [ ] **Subtask 4.1.2**: Create Hugging Face Space

  - [ ] Step 4.1.2.1: Go to huggingface.co/spaces
  - [ ] Step 4.1.2.2: Click "Create new Space"
  - [ ] Step 4.1.2.3: Choose "Gradio" as SDK
  - [ ] Step 4.1.2.4: Name space "mcp-sentiment-unit2"
  - [ ] Step 4.1.2.5: Configure as public space

- [ ] **Subtask 4.1.3**: Deploy to Hugging Face Spaces
  ```bash
  # Deploy the MCP server to Hugging Face Spaces for public access
  # This makes your MCP server available to anyone on the internet
  cd hugging-face-mcp-course/unit2
  git init  # Initialize git repository
  git add sentiment_analysis_mcp_server.py requirements.txt  # Add necessary files
  git commit -m "Unit 2: Sentiment Analysis MCP Server"  # Commit changes
  git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-sentiment-unit2  # Add remote
  git push -u origin main  # Push to Hugging Face Spaces
  ```

**Deployment Results:**

```
Hugging Face Spaces Deployment:
- Space created: [ ] Success / [ ] Issues
- Space URL:
- Deployment status: [ ] Success / [ ] Failed
- MCP server accessible at: https://YOUR_USERNAME-mcp-sentiment-unit2.hf.space/gradio_api/mcp/sse
- Public testing completed: [ ] Yes / [ ] No

```

### Task 4.2: Production Testing

- [ ] **Subtask 4.2.1**: Test deployed MCP server

  ```bash
  # Test deployed server schema
  # Verify that the deployed MCP server is accessible and working
  curl https://YOUR_USERNAME-mcp-sentiment-unit2.hf.space/gradio_api/mcp/schema
  ```

- [ ] **Subtask 4.2.2**: Update client configurations for production

  - [ ] Step 4.2.2.1: Update mcp-config.json with deployed URL
  - [ ] Step 4.2.2.2: Test clients against deployed server
  - [ ] Step 4.2.2.3: Verify end-to-end functionality

- [ ] **Subtask 4.2.3**: Performance and reliability testing
  - [ ] Step 4.2.3.1: Test with various input lengths
  - [ ] Step 4.2.3.2: Test with special characters and edge cases
  - [ ] Step 4.2.3.3: Monitor response times
  - [ ] Step 4.2.3.4: Test concurrent connections

**Production Testing Results:**

```
Production Testing:
- Deployed server response: [ ] Working / [ ] Issues
- Client connectivity: [ ] All clients working / [ ] Some issues
- Performance metrics:
  - Average response time:
  - Concurrent connections tested:
  - Error rate:

```

## Task Group 5: Advanced Features and Integration

### Task 5.1: Error Handling and Robustness

- [ ] **Subtask 5.1.1**: Enhance error handling in server

  - [ ] Step 5.1.1.1: Add input validation
  - [ ] Step 5.1.1.2: Handle empty/null inputs gracefully
  - [ ] Step 5.1.1.3: Add logging for debugging
  - [ ] Step 5.1.1.4: Implement proper HTTP error responses

- [ ] **Subtask 5.1.2**: Improve client error handling
  - [ ] Step 5.1.2.1: Add connection retry logic
  - [ ] Step 5.1.2.2: Handle server timeouts
  - [ ] Step 5.1.2.3: Provide user-friendly error messages

### Task 5.2: Documentation and Examples

- [ ] **Subtask 5.2.1**: Create API documentation

  ```bash
  # Create comprehensive API documentation for the MCP server
  # This helps other developers understand how to use your MCP tools
  touch hugging-face-mcp-course/unit2/API_DOCS.md
  ```

- [ ] **Subtask 5.2.2**: Create usage examples

  ```bash
  # Create practical examples showing how to use the MCP server
  # Include examples for different client types and use cases
  touch hugging-face-mcp-course/unit2/EXAMPLES.md
  ```

- [ ] **Subtask 5.2.3**: Document deployment process
  ```bash
  # Document the complete deployment process for future reference
  # Include troubleshooting tips and best practices
  touch hugging-face-mcp-course/unit2/DEPLOYMENT.md
  ```

## Quick Command Reference

### Development Commands

```bash
# Start sentiment analysis server
# Launches both web interface and MCP server
uv run hugging-face-mcp-course/unit2/sentiment_analysis_mcp_server.py

# Start Gradio MCP client
# Launches client interface that connects to sentiment server
uv run hugging-face-mcp-course/unit2/gradio_client.py

# Start SmolAgents client
# Creates AI agent with sentiment analysis capabilities
uv run hugging-face-mcp-course/unit2/smolagents_client.py

# Test server endpoints
# Verify MCP server is running and accessible
curl http://localhost:7860/gradio_api/mcp/schema
curl http://localhost:7860/gradio_api/mcp/sse
```

### Testing Commands

```bash
# Verify dependencies
# Ensure all required packages are installed and importable
uv run python -c "import gradio, textblob, smolagents; print('All imports successful')"

# Test sentiment analysis function
# Quick test of the core sentiment analysis functionality
uv run python -c "
from textblob import TextBlob
blob = TextBlob('This is amazing!')
print('Test sentiment:', blob.sentiment)
"

# Generate requirements for deployment
# Create requirements.txt file for Hugging Face Spaces
uv export --format requirements-txt > requirements.txt
```

## Progress Tracking

### Unit 2 Completion Checklist

- [ ] **Task Group 1**: Project Setup and Environment (0/2 tasks)
- [ ] **Task Group 2**: MCP Server Development (0/2 tasks)
- [ ] **Task Group 3**: MCP Client Development (0/4 tasks)
- [ ] **Task Group 4**: Deployment and Production (0/2 tasks)
- [ ] **Task Group 5**: Advanced Features (0/2 tasks)

### Success Criteria

- [ ] Sentiment analysis MCP server running locally
- [ ] Server deployed to Hugging Face Spaces
- [ ] At least one working MCP client
- [ ] End-to-end functionality demonstrated
- [ ] Documentation completed

### Next Steps After Unit 2

- [ ] Prepare for Unit 3: Advanced MCP Development
- [ ] Consider additional client implementations
- [ ] Explore more complex sentiment analysis features
- [ ] Plan integration with other MCP servers

---

**Last Updated**: [Current Date]
**Completion Status**: Not Started
**Current Focus**: Task Group 1 - Project Setup and Environment
