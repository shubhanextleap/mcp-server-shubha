# Railway Deployment Plan

This document outlines the steps required to deploy the Google MCP Server to Railway.

## 1. Bypass Terminal Prompts in Production
Currently, the server pauses and waits for an explicit `y/n` input in the terminal. On Railway, there is no interactive terminal. If we keep the `input()` prompts, the server will hang indefinitely.
- We must update `server.py` to check for an environment variable (e.g., `BYPASS_APPROVAL=true`).
- If deployed, it will automatically bypass the `input()` prompt and process requests directly.

## 2. Secret Management
The files `credentials.json` and `token.json` contain sensitive credentials and must **never** be committed to GitHub.
- We will manage these by storing their contents as Base64-encoded Environment Variables in Railway (`CREDENTIALS_JSON_BASE64` and `TOKEN_JSON_BASE64`).
- We will create a `start.sh` script that decodes these variables using `base64 -d` and writes them to the ephemeral filesystem before starting the server.

## 3. Railway Configuration
- **Procfile**: Create a `Procfile` for Railway with the following content to start the server:
  `web: bash start.sh`
- **Python Version**: Railway defaults to the newest Python (3.13), which causes compiler errors with older dependencies. Create a `.python-version` file containing exactly `3.11` to force Railway to build the app using Python 3.11.

## 4. Git Configuration
- Create a `.gitignore` to exclude secrets:
  ```
  credentials.json
  token.json
  __pycache__/
  ```

## 5. Deployment Steps
1. Commit your code (ensuring `.gitignore` is in place) and push to a new GitHub repository.
2. In the Railway dashboard, connect your GitHub repository to create a new project.
3. In the Railway project settings, add your Base64 encoded secrets as environment variables:
   - `CREDENTIALS_JSON_BASE64`
   - `TOKEN_JSON_BASE64`
   - `BYPASS_APPROVAL=true`
4. Trigger the deployment and monitor the Railway logs. The `start.sh` script will reconstruct your `credentials.json` and `token.json`, and then launch `uvicorn`.
