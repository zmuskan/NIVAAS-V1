from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg_pool import ConnectionPool

from backend.app.config import settings

logger = logging.getLogger(__name__)

_pool: ConnectionPool | None = None


def init_pool() -> None:
    global _pool

    if _pool is not None:
        return

    logger.info("Initializing PostgreSQL connection pool...")

    _pool = ConnectionPool(
        conninfo=settings.DATABASE_URL,
        min_size=1,
        max_size=10,
        open=False,
    )

    _pool.open(wait=True)

    logger.info("Connection pool initialized successfully.")


def close_pool() -> None:
    global _pool

    if _pool is not None:
        logger.info("Closing PostgreSQL connection pool.")
        _pool.close()
        _pool = None


def get_pool() -> ConnectionPool:
    if _pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    return _pool


@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    with get_pool().connection() as conn:
        yield conn


def check_connection() -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True

    except Exception:
        logger.exception("Database health check failed.")
        return False
