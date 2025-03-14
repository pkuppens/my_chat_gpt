# Implementation Tasks (for Tester)

## Priority: High

TASK #1: Backend Server - Get Available Providers

CONTEXT:
- Component Purpose: Provide a list of supported LLM providers to the frontend.
- Architectural Constraints: REST API endpoint.
- Dependencies: None.

REQUIREMENTS:
- Implement a GET endpoint `/api/providers`.
- Return a hardcoded list of providers: `["Ollama", "OpenAI"]`.

INTERFACES:
- GET /api/providers: Returns a JSON array of strings.

ACCEPTANCE CRITERIA:
- Calling `/api/providers` returns `["Ollama", "OpenAI"]` with HTTP status 200.

PRIORITY: High
ESTIMATED COMPLEXITY: Low

---

TASK #2: Backend Server - Get Models for Provider

CONTEXT:
- Component Purpose:  Retrieve the available models for a given LLM provider.
- Architectural Constraints: REST API endpoint, must handle Ollama and OpenAI.
- Dependencies: LLM Provider APIs.

REQUIREMENTS:
- Implement a GET endpoint `/api/models?provider=<provider_name>`.
- For `provider=Ollama`, use the Ollama API to fetch the model list.
- For `provider=OpenAI`, use the OpenAI API to fetch the model list. (Requires OpenAI API key).
- Return a JSON array of model names.

INTERFACES:
- GET /api/models?provider=Ollama: Returns a JSON array of Ollama model names.
- GET /api/models?provider=OpenAI: Returns a JSON array of OpenAI model names.

ACCEPTANCE CRITERIA:
- Calling `/api/models?provider=Ollama` returns a valid list of models (can be mocked initially).
- Calling `/api/models?provider=OpenAI` returns a valid list of models (can be mocked initially).
- Calling with an invalid provider returns a 400 error.
- Errors from LLM provider APIs are handled gracefully (502 error).

PRIORITY: High
ESTIMATED COMPLEXITY: Medium

---

TASK #3: Backend Server - Send Prompt and Get Response

CONTEXT:
- Component Purpose: Send the user's prompt to the selected LLM and return the response.
- Architectural Constraints: REST API endpoint, handles both text and code block outputs.
- Dependencies: LLM Provider APIs.

REQUIREMENTS:
- Implement a POST endpoint `/api/generate`.
- Parse the request body (provider, model, systemPrompt, userPrompt, format).
- Call the appropriate LLM provider API based on the `provider` and `model`.
- Process the LLM response:
    - If `format` is `"text"`, extract the plain text output.
    - If the output contains code blocks (single or array), extract them into the `codeBlocks` array.
- Return the response in the specified JSON format.

INTERFACES:
- POST /api/generate: Accepts a JSON body, returns a JSON response with `output` and `codeBlocks`.

ACCEPTANCE CRITERIA:
- Sending a valid request to `/api/generate` returns a successful response (200) with the expected JSON format.
- Text output is correctly extracted.
- Code blocks are correctly identified and parsed.
- Errors from LLM provider APIs are handled gracefully (502, 504).

PRIORITY: High
ESTIMATED COMPLEXITY: High

---

TASK #4: Backend Server - Save File

CONTEXT:
- Component Purpose: Save a code block to a file on the server.
- Architectural Constraints: REST API endpoint.
- Dependencies: File system access.

REQUIREMENTS:
- Implement a POST endpoint `/api/save`.
- Parse the request body (filename, content).
- Save the content to a file with the given filename in a designated directory (e.g., `./saved_code/`).
- Return a success/failure response.

INTERFACES:
- POST /api/save: Accepts a JSON body, returns a JSON response indicating success or failure.

ACCEPTANCE CRITERIA:
- Sending a valid request to `/api/save` creates a file with the correct content.
- Invalid requests (missing filename/content) return a 400 error.
- File system errors are handled gracefully (500 error).

PRIORITY: High
ESTIMATED COMPLEXITY: Medium

---

## Priority: Medium

TASK #5: Frontend - UI Layout and Basic Interactions

CONTEXT:
- Component Purpose: Create the user interface and handle basic user input.
- Architectural Constraints: Vanilla TypeScript, no frameworks.
- Dependencies: None.

REQUIREMENTS:
- Create the HTML structure (dropdowns for provider and model, text editors for prompts, output area, buttons).
- Implement event listeners for:
    - Provider selection change.
    - Model selection change.
    - Load/Save buttons for system prompt.
    - Load/Save buttons for user prompt.
    - Submit button to send prompts.
    - Save buttons for code blocks.
- Populate the provider dropdown on page load.

INTERFACES:
- User interactions with UI elements.

ACCEPTANCE CRITERIA:
- All UI elements are present and functional.
- Provider dropdown is populated with "Ollama" and "OpenAI".
- Clicking buttons triggers corresponding event handlers (can be empty functions initially).

PRIORITY: Medium
ESTIMATED COMPLEXITY: Medium

---

TASK #6: Frontend - API Calls

CONTEXT:
- Component Purpose: Make API calls to the backend server.
- Architectural Constraints: Use `fetch` API.
- Dependencies: Backend Server.

REQUIREMENTS:
- Implement functions to call:
    - `/api/providers`
    - `/api/models?provider=<provider>`
    - `/api/generate`
    - `/api/save`
- Handle responses and errors from the API calls.
- Update the UI based on the API responses (e.g., populate the model dropdown, display LLM output).

INTERFACES:
- Calls to the backend server's REST API.

ACCEPTANCE CRITERIA:
- API calls are made correctly.
- Responses are parsed correctly.
- Errors are handled gracefully (e.g., display error messages to the user).
- UI is updated correctly based on API responses.

PRIORITY: Medium
ESTIMATED COMPLEXITY: High

---

## Priority: Low

TASK #7: Frontend - Code Block Rendering

CONTEXT:
- Component Purpose: Render code blocks with save buttons.
- Architectural Constraints: Dynamically create HTML elements.
- Dependencies: Frontend - API Calls.

REQUIREMENTS:
- When the LLM response contains `codeBlocks`, create a multiline text area for each block.
- Set the `name` and `content` of the text area.
- Add a 'Save' button next to each text area.
- When the 'Save' button is clicked, call the `/api/save` endpoint with the filename and content.

INTERFACES:
- Dynamic HTML element creation and manipulation.

ACCEPTANCE CRITERIA:
- Code blocks are rendered correctly.
- Save buttons are present and functional.
- Clicking a Save button triggers the API call to save the file.

PRIORITY: Low
ESTIMATED COMPLEXITY: Medium
