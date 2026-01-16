#!/bin/bash

CONTAINER_NAME="gemini-army"
IMAGE_NAME="gemini-army"

# Stop and remove existing container if it exists
docker stop "$CONTAINER_NAME" 2>/dev/null
docker rm "$CONTAINER_NAME" 2>/dev/null

# Run the container
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    --env-file .env \
    -p 8000:8000 \
    "$IMAGE_NAME"

echo "Container '$CONTAINER_NAME' is now running on port 8000"
