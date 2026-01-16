# API Test Scripts

Bash scripts for testing the Gemini Army API endpoints using `curl`.

## Prerequisites

- `curl` - for making HTTP requests
- `jq` - for JSON formatting (install with `sudo apt install jq`)

## Scripts

| Script | Description |
|--------|-------------|
| `test_health.sh` | Tests `GET /health` endpoint |
| `test_models.sh` | Tests `GET /models` endpoint |
| `test_generate.sh` | Tests `POST /generate` endpoint |
| `test_all.sh` | Runs all tests sequentially |

## Usage

```bash
# Test health endpoint
./test_health.sh --access-key YOUR_API_KEY

# Test models endpoint
./test_models.sh --access-key YOUR_API_KEY

# Test generate with prompt (model is optional)
./test_generate.sh "Your prompt here" --access-key YOUR_API_KEY
./test_generate.sh "Hello world" --access-key YOUR_API_KEY --model gemini-2.0-flash

# Run all tests
./test_all.sh --access-key YOUR_API_KEY
```

## Environment Variables

- `BASE_URL` - API base URL (default: `http://localhost:8000`)
