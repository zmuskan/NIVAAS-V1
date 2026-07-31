from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from psycopg import Connection

from elt.common.config import Settings
from elt.common.database import get_connection
from elt.sources.osm.client import OverpassClient
from elt.sources.osm.normalizer import normalize_element
from elt.sources.osm.repository import AmenityRepository


logger = logging.getLogger(__name__)

PIPELINE_NAME = "osm_bengaluru_amenity_ingestion"


@dataclass(frozen=True, slots=True)
class PipelineResult:
    fetched: int
    normalized: int
    skipped: int
    persisted: int


def _start_pipeline_run(connection: Connection) -> str:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO metadata.pipeline_run (
                pipeline_name,
                status
            )
            VALUES (%s, %s)
            RETURNING pipeline_run_id
            """,
            (PIPELINE_NAME, "running"),
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Failed to create pipeline run.")

        return str(row[0])


def _finish_pipeline_run(
    connection: Connection,
    pipeline_run_id: str,
    status: str,
    duration_seconds: float,
) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE metadata.pipeline_run
            SET
                completed_at = NOW(),
                status = %s,
                duration_seconds = %s
            WHERE pipeline_run_id = %s
            """,
            (
                status,
                round(duration_seconds, 3),
                pipeline_run_id,
            ),
        )


def run_osm_pipeline(settings: Settings) -> PipelineResult:
    started = time.monotonic()

    with get_connection(settings) as connection:
        pipeline_run_id = _start_pipeline_run(connection)
        connection.commit()

    try:
        logger.info("Starting OSM amenity ingestion")

        client = OverpassClient(settings)
        elements = client.fetch_bengaluru_amenities()

        logger.info("Fetched %s OSM elements", len(elements))

        amenities = []

        for element in elements:
            normalized = normalize_element(element)

            if normalized is not None:
                amenities.append(normalized)

        skipped = len(elements) - len(amenities)

        logger.info(
            "Normalization complete: normalized=%s skipped=%s",
            len(amenities),
            skipped,
        )

        with get_connection(settings) as connection:
            repository = AmenityRepository(connection)
            counts = repository.upsert_many(amenities)

        result = PipelineResult(
            fetched=len(elements),
            normalized=len(amenities),
            skipped=skipped,
            persisted=counts.processed,
        )

        duration = time.monotonic() - started

        with get_connection(settings) as connection:
            _finish_pipeline_run(
                connection,
                pipeline_run_id,
                "completed",
                duration,
            )

        logger.info("OSM amenity ingestion completed: %s", result)

        return result

    except Exception:
        duration = time.monotonic() - started

        try:
            with get_connection(settings) as connection:
                _finish_pipeline_run(
                    connection,
                    pipeline_run_id,
                    "failed",
                    duration,
                )
        except Exception:
            logger.exception(
                "Failed to record pipeline failure metadata."
            )

        raise
