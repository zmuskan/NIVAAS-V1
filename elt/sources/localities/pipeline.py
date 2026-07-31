from __future__ import annotations

import logging
from dataclasses import dataclass

from elt.common.config import Settings
from elt.common.database import get_connection
from elt.sources.localities.client import LocalityClient
from elt.sources.localities.normalizer import select_boundary
from elt.sources.localities.registry import TARGET_LOCALITIES
from elt.sources.localities.repository import LocalityRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class LocalityPipelineResult:
    requested: int
    resolved: int
    unresolved: tuple[str, ...]
    rejected: tuple[str, ...]
    amenities_assigned: int


def run_locality_pipeline(
    settings: Settings,
) -> LocalityPipelineResult:
    logger.info("Starting NIVAAS locality ingestion")

    resolved = 0
    unresolved: list[str] = []

    # ---------------------------------------------------------
    # 1. Resolve target localities from OpenStreetMap
    # ---------------------------------------------------------

    with LocalityClient() as client:
        for target in TARGET_LOCALITIES:
            candidates = client.search(target)
            boundary = select_boundary(target, candidates)

            if boundary is None:
                logger.warning(
                    "No acceptable boundary found for %s",
                    target.name,
                )
                unresolved.append(target.name)
                continue

            with get_connection(settings) as connection:
                repository = LocalityRepository(connection)
                repository.upsert(boundary)

            resolved += 1

            logger.info(
                "Resolved %s -> OSM %s/%s",
                target.name,
                boundary.source_type,
                boundary.source_id,
            )

    # ---------------------------------------------------------
    # 2. Geometry quality assurance
    # ---------------------------------------------------------

    minimum_areas = {
        target.name: target.min_area_km2
        for target in TARGET_LOCALITIES
        if target.area_type == "locality"
    }

    with get_connection(settings) as connection:
        repository = LocalityRepository(connection)

        rejected = repository.delete_implausible_boundaries(
            minimum_areas
        )

    for name in rejected:
        logger.warning(
            "Rejected implausible locality boundary: %s",
            name,
        )

    # ---------------------------------------------------------
    # 3. Spatially assign amenities to accepted localities
    # ---------------------------------------------------------

    with get_connection(settings) as connection:
        repository = LocalityRepository(connection)

        amenities_assigned = repository.assign_amenities()

    logger.info(
        (
            "Locality ingestion completed: "
            "requested=%s resolved=%s unresolved=%s "
            "rejected=%s amenities_assigned=%s"
        ),
        len(TARGET_LOCALITIES),
        resolved,
        len(unresolved),
        len(rejected),
        amenities_assigned,
    )

    return LocalityPipelineResult(
        requested=len(TARGET_LOCALITIES),
        resolved=resolved,
        unresolved=tuple(unresolved),
        rejected=tuple(rejected),
        amenities_assigned=amenities_assigned,
    )
