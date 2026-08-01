from .client import RentalSourceClient
from .parser import RentalParser
from .normalizer import RentalNormalizer
from .repository import RentalRepository


class RentalPipeline:

    def __init__(self, client: RentalSourceClient):
        self.client = client
        self.repository = RentalRepository()

    def run(self):

        # Create a new scrape run
        scrape_run_id = self.repository.create_scrape_run()

        # Read dataset
        raw_records = self.client.fetch()

        print("=" * 60)
        print("NIVAAS Rental Ingestion")
        print("=" * 60)
        print(f"Loaded {len(raw_records)} rental records.")

        inserted = 0

        for record in raw_records:

            listing = RentalParser.parse(record)

            listing = RentalNormalizer.normalize(listing)

            self.repository.save(
                scrape_run_id,
                listing,
            )

            inserted += 1

        self.repository.finish_scrape_run(
            scrape_run_id,
            inserted,
        )

        print(f"Inserted {inserted} records.")
        print("Status: SUCCESS")
        print("=" * 60)
