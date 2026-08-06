from __future__ import annotations

import requests


OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"


class OSMScraper:

    def __init__(self, query: str):
        self.query = query

    def fetch(self):

        headers = {
            "Content-Type": "text/plain",
            "User-Agent": "NIVAAS/1.0"
        }

        response = requests.post(
            OVERPASS_URL,
            data=self.query,
            headers=headers,
            timeout=180,
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print(response.text[:500])

        response.raise_for_status()

        return response.json()["elements"]
