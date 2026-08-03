from __future__ import annotations

from typing import Iterator

import psycopg
from fastapi import Depends

from backend.app.config import Settings, get_settings
from backend.app.database import get_connection


def get_db_connection() -> Iterator[psycopg.Connection]:
    """
    FastAPI dependency that provides a PostgreSQL connection
    for the duration of a request.
    """
    with get_connection() as conn:
        yield conn


def get_app_settings() -> Settings:
    """
    Returns the cached application settings.
    """
    return get_settings()


DatabaseDep = Depends(get_db_connection)
SettingsDep = Depends(get_app_settings)
