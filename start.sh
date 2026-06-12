#!/bin/bash

# Decode credentials if they are provided via environment variables
if [ -n "$CREDENTIALS_JSON_BASE64" ]; then
    echo "Decoding credentials.json from environment variable..."
    echo "$CREDENTIALS_JSON_BASE64" | base64 -d > credentials.json
fi

if [ -n "$TOKEN_JSON_BASE64" ]; then
    echo "Decoding token.json from environment variable..."
    echo "$TOKEN_JSON_BASE64" | base64 -d > token.json
fi

# Set default port to 8000 if not provided by Railway
PORT="${PORT:-8000}"

echo "Starting uvicorn server on port $PORT..."
exec uvicorn server:app --host 0.0.0.0 --port "$PORT"
