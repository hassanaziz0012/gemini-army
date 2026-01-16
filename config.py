"""Configuration management for Gemini Army."""

import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Configuration dataclass for the application."""

    accepted_models: list[str]
    n_api_keys: int


def load_config(config_path: str | Path = "config.yaml") -> Config:
    """Load configuration from YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Config dataclass with loaded configuration.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        ValueError: If required config keys are missing.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        data = yaml.safe_load(f)

    required_keys = ["accepted_models", "n_api_keys"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required config key: {key}")

    return Config(
        accepted_models=data["accepted_models"],
        n_api_keys=data["n_api_keys"],
    )


# Global config instance - loaded once at module import
config = load_config()
