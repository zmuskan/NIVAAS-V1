from __future__ import annotations

import requests


class OSMClient:

    OVERPASS_URL = "https://overpass-api.de/api/interpreter"

    CATEGORIES = {
        "metro": 'node["railway"="station"]',
        "hospital": 'node["amenity"="hospital"]',
        "restaurant": 'node["amenity"="restaurant"]',
        "park": 'way["leisure"="park"]',
        "supermarket": 'node["shop"="supermarket"]',
    }

    def fetch_pois(self, locality: str):

        pois = []

        for category, selector in self.CATEGORIES.items():

            query = f"""
            [out:json][timeout:30];

            area
              ["name"="{locality}"]
              ["boundary"="administrative"];

            (
                {selector}(area);
            );

            out center;
            """

            try:

                response = requests.post(
                    self.OVERPASS_URL,
                    data=query,
                    timeout=60,
                )

                response.raise_for_status()

                data = response.json()

            except Exception as exc:

                print(f"{locality} ({category}) -> {exc}")

                continue

            for element in data.get("elements", []):

                tags = element.get("tags", {})

                lat = element.get("lat")
                lon = element.get("lon")

                if lat is None:

                    center = element.get("center")

                    if center:

                        lat = center.get("lat")
                        lon = center.get("lon")

                if lat is None or lon is None:

                    continue

                pois.append(
                    {
                        "name": tags.get("name", "Unknown"),
                        "category": category,
                        "latitude": lat,
                        "longitude": lon,
                        "locality": locality,
                        "source": "OpenStreetMap",
                    }
                )

        return pois
