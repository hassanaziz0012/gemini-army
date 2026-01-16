#!/bin/bash
# Test the /models endpoint

BASE_URL="${BASE_URL:-http://localhost:8000}"
API_KEY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --access-key)
      API_KEY="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 --access-key KEY"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$API_KEY" ]; then
  echo "Error: --access-key is required"
  echo "Usage: $0 --access-key KEY"
  exit 1
fi

echo "Testing GET /models ..."
echo "========================"

curl -s -X GET "$BASE_URL/models" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" | jq .

echo ""
echo "Done."
