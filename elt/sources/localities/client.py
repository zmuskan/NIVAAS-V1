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

    def search(
        self,
        locality: TargetLocality,
    ) -> list[dict[str, Any]]:
        query = f"{locality.name}, {locality.city}, {locality.state}, India"

        logger.info("Searching locality boundary: %s", query)

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
                f"Unexpected Nominatim response for {locality.name}"
            )

        time.sleep(self.request_delay_seconds)

        return payload

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "LocalityClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
