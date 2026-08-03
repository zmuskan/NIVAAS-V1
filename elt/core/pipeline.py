from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from .repository import CoreRepository


@dataclass
class CorePipelineStats:
    total_read: int = 0
    total_listings_created: int = 0
    total_failed: int = 0
    elapsed_seconds: float = 0.0

    def print_summary(self):
        print("=" * 60)
        print("NIVAAS CORE PIPELINE")
        print("=" * 60)
        print(f"Records Read       : {self.total_read}")
        print(f"Listings Created   : {self.total_listings_created}")
        print(f"Failed             : {self.total_failed}")
        print(f"Elapsed            : {self.elapsed_seconds:.2f}s")
        print("=" * 60)


class CorePipeline:

    def __init__(self):
        self.repository = CoreRepository()

    def run(self):

        stats = CorePipelineStats()

        start = perf_counter()

        records = self.repository.fetch_staging_records(limit=500)

        stats.total_read = len(records)

        for record in records:

            try:

                success = self.repository.process_record(record)

                if success:
                    stats.total_listings_created += 1
                else:
                    stats.total_failed += 1

            except Exception as exc:

                stats.total_failed += 1
                print(exc)

        stats.elapsed_seconds = perf_counter() - start

        self.repository.close()

        return stats
