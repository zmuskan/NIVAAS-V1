from __future__ import annotations

from .repository import AnalyticsRepository


class AnalyticsPipeline:

    def __init__(self):

        self.repository = AnalyticsRepository()

    def run(self):

        rows = self.repository.fetch_locality_metrics()

        self.repository.save_metrics(rows)

        print(f"Saved {len(rows)} locality metrics.")

        self.repository.close()
