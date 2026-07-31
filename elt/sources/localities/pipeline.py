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
    requested_localities: int
    resolved_localities: int
    unresolved_localities: tuple[str, ...]
    deferred_corridors: tuple[str, ...]
    rejected: tuple[str, ...]
    amenities_assigned: int


def run_locality_pipeline(
    settings: Settings,
) -> LocalityPipelineResult:
    logger.info("Starting NIVAAS locality ingestion")

    locality_targets = tuple(
        target
        for target in TARGET_LOCALITIES
        if target.area_type == "locality"
    )

    corridor_targets = tuple(
        target
        for target in TARGET_LOCALITIES
        if target.area_type == "corridor"
    )

    resolved = 0
    unresolved: list[str] = []

    # ---------------------------------------------------------
    # 1. Resolve neighbourhood/locality polygons
    # ---------------------------------------------------------

    with (
        LocalityClient() as client,
        get_connection(settings) as connection,
    ):
        repository = LocalityRepository(connection)

        for target in locality_targets:
            candidates = client.search(target)
            boundary = select_boundary(
                target,
                candidates,
            )

            if boundary is None:
                logger.warning(
                    "No acceptable boundary found for %s",
                    target.name,
                )
                unresolved.append(target.name)
                continue

            repository.upsert(boundary)
            resolved += 1

            logger.info(
                "Resolved %s -> OSM %s/%s",
                target.name,
                boundary.source_type,
                boundary.source_id,
            )

        # -----------------------------------------------------
        # 2. Geometry quality assurance
        # -----------------------------------------------------

        minimum_areas = {
            target.name: target.min_area_km2
            for target in locality_targets
        }

        rejected = repository.delete_implausible_boundaries(
            minimum_areas
        )

        for name in rejected:
            logger.warning(
                "Rejected implausible locality boundary: %s",
                name,
            )

        # A locality may have passed candidate normalization but failed
        # the PostGIS area QA. Do not report it as successfully resolved.
        rejected_set = set(rejected)
        resolved_after_qa = resolved - len(rejected_set)

        # -----------------------------------------------------
        # 3. Spatially assign amenities
        # -----------------------------------------------------

        amenities_assigned = repository.assign_amenities()

    deferred_corridors = tuple(
        target.name
        for target in corridor_targets
    )

    for corridor in deferred_corridors:
        logger.info(
            "Deferred corridor geometry: %s",
            corridor,
        )

    logger.info(
        (
            "Locality ingestion completed: "
            "requested_localities=%s "
            "resolved_localities=%s "
            "unresolved_localities=%s "
            "rejected=%s "
            "deferred_corridors=%s "
            "amenities_assigned=%s"
        ),
        len(locality_targets),
        resolved_after_qa,
        len(unresolved),
        len(rejected),
        len(deferred_corridors),
        amenities_assigned,
    )

    return LocalityPipelineResult(
        requested_localities=len(locality_targets),
        resolved_localities=resolved_after_qa,
        unresolved_localities=tuple(unresolved),
        deferred_corridors=deferred_corridors,
        rejected=tuple(rejected),
        amenities_assigned=amenities_assigned,
    )
