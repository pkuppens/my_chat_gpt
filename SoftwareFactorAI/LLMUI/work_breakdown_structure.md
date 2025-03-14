# Work Breakdown Structure

```mermaid
graph TD
    A[User] -->|Interacts with| B(Frontend)
    B -->|API Requests| C(Backend Server)
    C -->|Fetches Models| D(LLM Provider APIs: Ollama, OpenAI, ...)
    C -->|Sends Prompts| D
    D -->|Returns Responses| C
    C -->|Sends Data| B
```

## Components

| Component        | Responsibilities                                                                                   | Interfaces                                           | Deployment | Notes                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ---------- | ---------------------------------------------------------------- |
| **Frontend**     | - Display UI elements (dropdowns, text editors, output area).<br>- Handle user interactions (button clicks, input).<br>- Make API calls to the backend.<br>- Render LLM output (text and code blocks). | - REST API (provided by the Backend Server)           | Local      | Runs in the user's browser.                                   |
| **Backend Server** | - Serve static frontend files (HTML, CSS, JS).<br>- Handle API requests from the frontend.<br>- Interact with LLM provider APIs.<br>- Manage file saving.                        | - REST API (consumed by the Frontend)<br>- LLM Provider APIs | Local      | Node.js server, runs on user's machine.                        |
| **LLM Providers** | - Provide LLM models and inference capabilities.                                                   | - Provider-specific APIs (e.g., Ollama API, OpenAI API) | External   | Accessed via HTTP requests from the Backend Server.              |
