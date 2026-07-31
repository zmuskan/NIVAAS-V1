from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

import psycopg
from psycopg import Connection

from elt.common.config import Settings


@contextmanager
def get_connection(settings: Settings) -> Iterator[Connection]:
    connection = psycopg.connect(settings.database_url)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
