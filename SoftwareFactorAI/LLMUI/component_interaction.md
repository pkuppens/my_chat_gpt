# Component Interaction Specifications

## Frontend <-> Backend Server

### 1. Get Available Providers

*   **Endpoint:** `/api/providers`
*   **Method:** `GET`
*   **Request:** (None)
*   **Response:** `["Ollama", "OpenAI", ...]` (JSON array of strings)
*   **Errors:** `500` (Internal Server Error)
*   **Authentication:** None

### 2. Get Models for Provider

*   **Endpoint:** `/api/models`
*   **Method:** `GET`
*   **Request:** `?provider=Ollama` (Query parameter: `provider`)
*   **Response:**  `["model1", "model2", ...]` (JSON array of strings)
*   **Errors:**
    *   `400` (Bad Request - Missing or invalid provider)
    *   `500` (Internal Server Error - Issue fetching models)
    *   `502` (Bad Gateway - Issue communicating with the LLM provider)
*    **Authentication:** None

### 3. Send Prompt and Get Response

*   **Endpoint:** `/api/generate`
*   **Method:** `POST`
*   **Request:** (JSON body)
    ```json
    {
      "provider": "Ollama",
      "model": "llama2",
      "systemPrompt": "You are a helpful assistant.",
      "userPrompt": "What is the capital of France?",
        "format": "text"
    }
    ```
*   **Response:** (JSON body)
    ```json
    {
      "output": "Paris is the capital of France.",
      "codeBlocks": []
    }
    ```
   or, with code blocks:
      ```json
      {
        "output": "Here is the python program that prints the capital of France",
      "codeBlocks": [
          { "name": "capital.py", "type": "python", "content": "print('Paris')" }
        ]
      }
    ```
* **Errors:**
    *    `400` (Bad request - invalid input data)
    *    `500` (Internal server error)
    *    `502` (Bad Gateway, if there are issues calling LLM providers)
    *    `504` (Gateway timeout, if the LLM response takes to long - consider streaming in the future)
* **Authentication:** None


### 4. Save File

*   **Endpoint:** `/api/save`
*   **Method:** `POST`
*   **Request:** (JSON body)
    ```json
    {
      "filename": "my_program.py",
      "content": "print('Hello, world!')"
    }
    ```
*   **Response:**  `{ "success": true }` or `{ "success": false, "error": "..." }`
*   **Errors:**
    *   `400` (Bad Request - Missing filename or content)
    *   `500` (Internal Server Error - Issue saving file)
*   **Authentication:** None

## Backend Server <-> LLM Providers

These interactions are provider-specific and follow the official API documentation for each provider (Ollama, OpenAI, etc.).  The Backend Server acts as a proxy and adapts the requests/responses to the format expected by the Frontend.

Key considerations:

*   **Error Handling:** The Backend Server should gracefully handle API errors from the LLM providers and return appropriate error codes to the Frontend.
*   **Rate Limiting:** Implement rate limiting if necessary to avoid exceeding API limits.
*   **API Keys:** Securely manage API keys for accessing the LLM providers (e.g., using environment variables).
