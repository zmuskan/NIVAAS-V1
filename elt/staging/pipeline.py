from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from .repository import StagingRepository
from .transformer import ListingTransformer, StagingListing
from .validator import RawListingValidator, ValidationResult

DEFAULT_BATCH_SIZE = 500


@dataclass
class PipelineStats:
    total_read: int = 0
    total_valid: int = 0
    total_invalid: int = 0
    total_inserted: int = 0
    total_batches: int = 0
    elapsed_seconds: float = 0.0
    field_error_counts: dict[str, int] = field(default_factory=dict)

    def record_validation_result(self, result: ValidationResult):
        if result.is_valid:
            self.total_valid += 1
        else:
            self.total_invalid += 1
            for issue in result.issues:
                self.field_error_counts[issue.field_name] = (
                    self.field_error_counts.get(issue.field_name, 0) + 1
                )


class StagingPipeline:

    def __init__(self):
        self.repository = StagingRepository()

    def run(self):

        stats = PipelineStats()

        start = perf_counter()

        raw_records = self.repository.fetch_raw_listings()

        stats.total_read = len(raw_records)

        valid_records: list[StagingListing] = []

        for row in raw_records:

            validation = RawListingValidator.validate(
                row["raw_listing_id"],
                row["payload"],
            )

            stats.record_validation_result(validation)

            if not validation.is_valid:

                self.repository.save_invalid(
                    row["raw_listing_id"],
                    validation.issues,
                )

                continue

            listing = ListingTransformer.transform(
                raw_listing_id=row["raw_listing_id"],
                scrape_run_id=row["scrape_run_id"],
                payload=row["payload"],
            )

            valid_records.append(listing)

        if valid_records:

            stats.total_inserted = len(valid_records)

            for listing in valid_records:
                self.repository.save(listing)

            stats.total_batches = 1

        stats.elapsed_seconds = perf_counter() - start

        self.repository.close()

        print("=" * 60)
        print("NIVAAS STAGING PIPELINE")
        print("=" * 60)
        print(f"Records Read      : {stats.total_read}")
        print(f"Valid Records     : {stats.total_valid}")
        print(f"Invalid Records   : {stats.total_invalid}")
        print(f"Inserted Records  : {stats.total_inserted}")
        print(f"Elapsed Time      : {stats.elapsed_seconds:.2f}s")
        print("=" * 60)

        return stats
