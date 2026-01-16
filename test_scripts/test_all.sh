#!/bin/bash
# Run all API endpoint tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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

echo "========================================"
echo "   Gemini Army API Test Suite"
echo "========================================"
echo ""

echo "1. Health Check"
echo "----------------"
bash "$SCRIPT_DIR/test_health.sh" --access-key "$API_KEY"
echo ""

echo "2. List Models"
echo "----------------"
bash "$SCRIPT_DIR/test_models.sh" --access-key "$API_KEY"
echo ""

echo "3. Generate (with default prompt)"
echo "----------------------------------"
bash "$SCRIPT_DIR/test_generate.sh" "What is 2+2?" --access-key "$API_KEY"
echo ""

echo "========================================"
echo "   All tests completed!"
echo "========================================"
