"""FastAPI application for Gemini Army."""

import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dotenv import load_dotenv

from config import config
from gemini import ask_gemini, load_api_keys, GeminiResponse


# Load environment variables from .env file
load_dotenv()

# Load API keys on startup
load_api_keys()

# Get the access key from environment
ARMY_ACCESS_KEY = os.getenv("ARMY_ACCESS_KEY")

app = FastAPI(
    title="Gemini Army",
    description="API for interacting with Google Gemini models",
    version="1.0.0",
)


# Paths that don't require authentication
PUBLIC_PATHS = {"/docs", "/redoc", "/openapi.json"}


@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    """Middleware to authenticate all requests using ARMY_ACCESS_KEY."""
    # Skip authentication for public paths (docs)
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    # Get the Authorization header
    auth_header = request.headers.get("Authorization")

    # Check if access key is configured
    if not ARMY_ACCESS_KEY:
        return JSONResponse(
            status_code=500,
            content={"detail": "Server misconfiguration: ARMY_ACCESS_KEY not set"},
        )

    # Validate the Authorization header
    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Authorization header"},
        )

    if auth_header != ARMY_ACCESS_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid access key"},
        )

    # Proceed with the request if authenticated
    response = await call_next(request)
    return response


class GenerateRequest(BaseModel):
    """Request body for the generate endpoint."""

    prompt: str
    model: str | None = None  # Optional, defaults to first accepted model


class GenerateResponse(BaseModel):
    """Response body for the generate endpoint."""

    text: str
    model: str
    usage_metadata: dict | None = None
    finish_reason: str | None = None


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate a response from Gemini.

    Args:
        request: The generation request containing prompt and optional model.

    Returns:
        GenerateResponse with the generated text and metadata.

    Raises:
        HTTPException: If model is invalid or generation fails.
    """
    # Use default model if not specified
    model = request.model or config.accepted_models[0]

    # Validate model
    if model not in config.accepted_models:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model '{model}'. Accepted models: {config.accepted_models}",
        )

    try:
        response: GeminiResponse = ask_gemini(prompt=request.prompt, model=model)

        return GenerateResponse(
            text=response.text,
            model=response.model,
            usage_metadata=response.usage_metadata,
            finish_reason=response.finish_reason,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}",
        )


@app.get("/models")
async def list_models() -> dict:
    """List all accepted models.

    Returns:
        Dictionary containing the list of accepted models.
    """
    return {"models": config.accepted_models}


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        Dictionary indicating service health.
    """
    return {"status": "healthy"}
