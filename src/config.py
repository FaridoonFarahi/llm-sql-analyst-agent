"""Shared configuration: paths, model, and key validation."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "db" / "chinook.db"

MODEL = "gpt-4.1-mini"

# Result preview cap (rows printed in CLI). Underlying query still returns full result.
PREVIEW_ROWS = 20


def require_api_key() -> str:
    """Return the OpenAI API key from the environment, or raise a clear error."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return key
