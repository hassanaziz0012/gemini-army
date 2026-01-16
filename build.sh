#!/bin/bash

IMAGE_NAME="gemini-army"

docker build -t "$IMAGE_NAME" .

echo "Image '$IMAGE_NAME' built successfully"
