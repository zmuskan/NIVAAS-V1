from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from elt.sources.localities.registry import TargetLocality


logger = logging.getLogger(__name__)


class LocalityClient:
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(
        self,
        *,
        timeout_seconds: float = 30.0,
        request_delay_seconds: float = 1.1,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.request_delay_seconds = request_delay_seconds

        self._client = httpx.Client(
            timeout=timeout_seconds,
            headers={
                "User-Agent": (
                    "NIVAAS/1.0 "
                    "(Bengaluru livability research project)"
                )
            },
        )

    def _search_name(
        self,
        *,
        name: str,
        city: str,
        state: str,
    ) -> list[dict[str, Any]]:
        query = f"{name}, {city}, {state}, India"

        logger.info(
            "Searching locality boundary: %s",
            query,
        )

        try:
            response = self._client.get(
                self.BASE_URL,
                params={
                    "q": query,
                    "format": "jsonv2",
                    "polygon_geojson": 1,
                    "addressdetails": 1,
                    "limit": 5,
                    "countrycodes": "in",
                },
            )

            response.raise_for_status()

            payload = response.json()

            if not isinstance(payload, list):
                raise ValueError(
                    f"Unexpected Nominatim response for {name}"
                )

            return [
                candidate
                for candidate in payload
                if isinstance(candidate, dict)
            ]

        finally:
            # Respect the public Nominatim service.
            time.sleep(self.request_delay_seconds)

    def search(
        self,
        locality: TargetLocality,
    ) -> list[dict[str, Any]]:
        """
        Search using the canonical locality name followed by configured
        aliases.

        Results are deduplicated using the OSM object type and ID.
        """
        candidates: list[dict[str, Any]] = []
        seen: set[tuple[str, int]] = set()

        for search_name in locality.search_names:
            results = self._search_name(
                name=search_name,
                city=locality.city,
                state=locality.state,
            )

            for candidate in results:
                osm_type = candidate.get("osm_type")
                osm_id = candidate.get("osm_id")

                if (
                    isinstance(osm_type, str)
                    and isinstance(osm_id, int)
                ):
                    identity = (
                        osm_type,
                        osm_id,
                    )

                    if identity in seen:
                        continue

                    seen.add(identity)

                candidates.append(candidate)

        logger.info(
            "Collected %s unique candidates for %s",
            len(candidates),
            locality.name,
        )

        return candidates

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "LocalityClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
