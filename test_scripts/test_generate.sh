#!/bin/bash
# Test the /generate endpoint

BASE_URL="${BASE_URL:-http://localhost:8000}"
API_KEY=""
PROMPT=""
MODEL=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --access-key)
      API_KEY="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    *)
      # First positional argument is the prompt
      if [ -z "$PROMPT" ]; then
        PROMPT="$1"
        shift
      else
        echo "Unknown option: $1"
        echo "Usage: $0 \"prompt\" --access-key KEY [--model MODEL]"
        exit 1
      fi
      ;;
  esac
done

# Validate required arguments
if [ -z "$API_KEY" ]; then
  echo "Error: --access-key is required"
  echo "Usage: $0 \"prompt\" --access-key KEY [--model MODEL]"
  exit 1
fi

if [ -z "$PROMPT" ]; then
  echo "Error: prompt is required"
  echo "Usage: $0 \"prompt\" --access-key KEY [--model MODEL]"
  exit 1
fi

echo "Testing POST /generate ..."
echo "=========================="

# Build the JSON payload
if [ -n "$MODEL" ]; then
  JSON_PAYLOAD=$(jq -n --arg prompt "$PROMPT" --arg model "$MODEL" '{prompt: $prompt, model: $model}')
else
  JSON_PAYLOAD=$(jq -n --arg prompt "$PROMPT" '{prompt: $prompt}')
fi

echo "Request payload:"
echo "$JSON_PAYLOAD" | jq .
echo ""

curl -s -X POST "$BASE_URL/generate" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD" | jq .

echo ""
echo "Done."
