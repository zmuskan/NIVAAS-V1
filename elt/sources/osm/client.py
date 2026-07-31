from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from elt.common.config import Settings


logger = logging.getLogger(__name__)


class OverpassError(RuntimeError):
    pass


class OverpassClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def fetch_bengaluru_amenities(self) -> list[dict[str, Any]]:
        query = self._build_query()

        headers = {
            "User-Agent": (
                "NIVAAS/0.1 "
                "(Bengaluru livability research project)"
            )
        }

        last_error: Exception | None = None

        for attempt in range(1, self._settings.overpass_max_retries + 1):
            try:
                logger.info(
                    "Requesting Bengaluru amenities from Overpass "
                    "(attempt %s/%s)",
                    attempt,
                    self._settings.overpass_max_retries,
                )

                with httpx.Client(
                    timeout=self._settings.overpass_timeout_seconds,
                    headers=headers,
                ) as client:
                    response = client.post(
                        self._settings.overpass_url,
                        data={"data": query},
                    )

                response.raise_for_status()

                payload = response.json()
                elements = payload.get("elements")

                if not isinstance(elements, list):
                    raise OverpassError(
                        "Overpass response did not contain an elements list."
                    )

                return elements

            except (
                httpx.HTTPError,
                ValueError,
                OverpassError,
            ) as exc:
                last_error = exc

                logger.warning(
                    "Overpass request failed on attempt %s: %s",
                    attempt,
                    exc,
                )

                if attempt >= self._settings.overpass_max_retries:
                    break

                delay = (
                    self._settings.overpass_backoff_seconds
                    * (2 ** (attempt - 1))
                )
                time.sleep(delay)

        raise OverpassError(
            "Overpass request failed after all retry attempts."
        ) from last_error

    @staticmethod
    def _build_query() -> str:
        """
        Query Bengaluru using the administrative area registered in OSM.

        `out center` provides representative coordinates for ways/relations.
        """
        return """
[out:json][timeout:45];

area["name"="Bengaluru"]["boundary"="administrative"]->.searchArea;

(
  nwr["amenity"~"^(hospital|clinic|school|restaurant|fast_food|food_court|bus_station)$"](area.searchArea);

  nwr["shop"~"^(supermarket|grocery)$"](area.searchArea);

  nwr["leisure"~"^(park|garden|fitness_centre|fitness_station)$"](area.searchArea);

  nwr["highway"="bus_stop"](area.searchArea);

  nwr["public_transport"~"^(platform|stop_position|station)$"]["bus"="yes"](area.searchArea);

  nwr["railway"="station"]["station"~"^(subway|light_rail)$"](area.searchArea);

  nwr["railway"="subway_entrance"](area.searchArea);
);

out center tags;
""".strip()
