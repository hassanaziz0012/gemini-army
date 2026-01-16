"""Gemini AI integration module."""

import os
from enum import Enum
from dataclasses import dataclass
from google import genai

from config import config


class GeminiModel(str, Enum):
    """Enum of accepted Gemini models."""

    # Dynamically create enum values from config
    def __new__(cls, value: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj


# Create model enum values from config
for model_name in config.accepted_models:
    # Convert model name to valid Python identifier for enum
    enum_key = model_name.upper().replace("-", "_").replace(".", "_")
    setattr(GeminiModel, enum_key, model_name)


@dataclass
class GeminiResponse:
    """Response from Gemini API."""

    text: str
    model: str
    usage_metadata: dict | None = None
    finish_reason: str | None = None


# Store loaded API keys
_api_keys: list[str] = []
_current_key_index: int = 0


def load_api_keys() -> list[str]:
    """Load API keys from environment variables.

    Loads keys in format: GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc.
    Continues until n_api_keys from config is reached.

    Returns:
        List of loaded API keys.

    Raises:
        ValueError: If no API keys are found.
    """
    global _api_keys

    _api_keys = []
    for i in range(1, config.n_api_keys + 1):
        key_name = f"GEMINI_API_KEY_{i}"
        key = os.environ.get(key_name)
        if key:
            _api_keys.append(key)

    if not _api_keys:
        raise ValueError(
            f"No API keys found. Expected environment variables: "
            f"GEMINI_API_KEY_1 to GEMINI_API_KEY_{config.n_api_keys}"
        )

    return _api_keys


def get_next_api_key() -> str:
    """Get the next API key using round-robin selection.

    Returns:
        The next API key to use.
    """
    global _current_key_index

    if not _api_keys:
        load_api_keys()

    key = _api_keys[_current_key_index]
    _current_key_index = (_current_key_index + 1) % len(_api_keys)
    return key


def ask_gemini(prompt: str, model: str | GeminiModel) -> GeminiResponse:
    """Send a prompt to Gemini and get a response.

    Args:
        prompt: The prompt to send to Gemini.
        model: The model to use (either GeminiModel enum or string).

    Returns:
        GeminiResponse containing the response text and metadata.

    Raises:
        ValueError: If the model is not in the accepted models list.
    """
    # Convert enum to string if needed
    model_name = model.value if isinstance(model, GeminiModel) else model

    # Validate model
    if model_name not in config.accepted_models:
        raise ValueError(
            f"Model '{model_name}' not in accepted models: {config.accepted_models}"
        )

    # Get API key and create client
    api_key = get_next_api_key()
    client = genai.Client(api_key=api_key)

    # Generate content
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    # Extract usage metadata if available
    usage_metadata = None
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        usage_metadata = {
            "prompt_token_count": getattr(
                response.usage_metadata, "prompt_token_count", None
            ),
            "candidates_token_count": getattr(
                response.usage_metadata, "candidates_token_count", None
            ),
            "total_token_count": getattr(
                response.usage_metadata, "total_token_count", None
            ),
        }

    # Extract finish reason if available
    finish_reason = None
    if response.candidates and len(response.candidates) > 0:
        finish_reason = str(response.candidates[0].finish_reason)

    return GeminiResponse(
        text=response.text,
        model=model_name,
        usage_metadata=usage_metadata,
        finish_reason=finish_reason,
    )
