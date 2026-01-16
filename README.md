# Gemini Army

Private FastAPI service for interacting with Google Gemini models with automatic API key rotation and rate limit handling.

## Setup

1. **Install Dependencies:**
   ```bash
   uv sync  # or pip install -r requirements.txt
   ```

2. **Environment:**
   Create `.env`:
   ```env
   ARMY_ACCESS_KEY=your_secret_key
   GEMINI_API_KEYS=key1,key2,key3
   ```

3. **Run:**
   ```bash
   ./run.sh
   # OR
   uvicorn app:app --reload
   ```

## Usage

**Authentication:** header `Authorization: <ARMY_ACCESS_KEY>`

- **Generate:** `POST /generate` `{"prompt": "...", "model": "gemini-..."}`
- **Models:** `GET /models`
- **Health:** `GET /health`
- **Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Deployment

```bash
docker build -t gemini-army .
docker run -d --restart unless-stopped --env-file .env -p 8000:8000 gemini-army
```
