# Google MCP Server

A FastAPI-based MCP server providing tools to interact with Google Docs and Gmail.

## Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Docs API** and **Gmail API**.
3. Configure the OAuth consent screen and create an OAuth 2.0 Client ID (Desktop app).
4. Download the JSON file, rename it to `credentials.json`, and place it in the `google-mcp-server` directory.
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the server:
   ```bash
   uvicorn server:app --reload
   ```

## Usage

The server requires manual approval in the terminal for every action it executes. Make sure you run it in an interactive terminal.

### Endpoints

- `POST /append_to_doc`: Appends text to a Google Doc.
  - Payload: `{"doc_id": "...", "content": "..."}`
- `POST /create_email_draft`: Creates an email draft.
  - Payload: `{"to": "...", "subject": "...", "body": "..."}`
