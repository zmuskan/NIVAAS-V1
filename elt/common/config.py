from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str
    overpass_url: str = "https://overpass-api.de/api/interpreter"
    overpass_timeout_seconds: float = 60.0
    overpass_max_retries: int = 3
    overpass_backoff_seconds: float = 2.0

    @classmethod
    def from_env(cls) -> "Settings":
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError(
                "DATABASE_URL is required. "
                "Set it before running the ingestion pipeline."
            )

        return cls(
            database_url=database_url,
            overpass_url=os.getenv(
                "OVERPASS_URL",
                "https://overpass-api.de/api/interpreter",
            ),
            overpass_timeout_seconds=float(
                os.getenv("OVERPASS_TIMEOUT_SECONDS", "60")
            ),
            overpass_max_retries=int(
                os.getenv("OVERPASS_MAX_RETRIES", "3")
            ),
            overpass_backoff_seconds=float(
                os.getenv("OVERPASS_BACKOFF_SECONDS", "2")
            ),
        )
