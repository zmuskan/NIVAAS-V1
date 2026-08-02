from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from .matcher import PropertyMatcher
from .repository import CoreRepository


@dataclass
class CorePipelineStats:
    total_read: int = 0
    total_properties_created: int = 0
    total_properties_reused: int = 0
    total_listings_created: int = 0
    total_failed: int = 0
    elapsed_seconds: float = 0.0

    def print_summary(self):
        print("=" * 60)
        print("NIVAAS CORE PIPELINE")
        print("=" * 60)
        print(f"Records Read        : {self.total_read}")
        print(f"Properties Created  : {self.total_properties_created}")
        print(f"Properties Reused   : {self.total_properties_reused}")
        print(f"Listings Created    : {self.total_listings_created}")
        print(f"Failed              : {self.total_failed}")
        print(f"Elapsed             : {self.elapsed_seconds:.2f}s")
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

                property_hash = PropertyMatcher.compute_hash(
                    locality=record.locality,
                    property_type=record.property_type,
                    bhk=record.bhk,
                    area_sqft=record.area_sqft,
                )

                property_result, listing_result = (
                    self.repository.process_staging_record(
                        record,
                        property_hash,
                    )
                )

                if property_result.was_created:
                    stats.total_properties_created += 1
                else:
                    stats.total_properties_reused += 1

                if listing_result.was_created:
                    stats.total_listings_created += 1

            except Exception as exc:

                stats.total_failed += 1
                print(exc)

        stats.elapsed_seconds = perf_counter() - start

        return stats
