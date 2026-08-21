from .osm_client import OSMClient
from .repository import EnrichmentRepository


class EnrichmentPipeline:

    def __init__(self):
        self.client = OSMClient()
        self.repository = EnrichmentRepository()

    def run(self):

        print("=" * 60)
        print("NIVAAS ENRICHMENT")
        print("=" * 60)

        localities = self.repository.fetch_localities()

        total = 0

        for locality in localities:

            pois = self.client.fetch_pois(locality["name"])

            self.repository.save_pois(pois)

            total += len(pois)

            print(
                f"{locality['name']:<30} {len(pois):>5} POIs"
            )

        print("=" * 60)
        print(f"Saved {total} POIs")
        print("=" * 60)

        self.repository.close()
