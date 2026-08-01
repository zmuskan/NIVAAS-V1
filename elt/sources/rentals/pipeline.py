from .client import RentalSourceClient
from .parser import RentalParser
from .normalizer import RentalNormalizer
from .repository import RentalRepository


class RentalPipeline:

    def __init__(self, client: RentalSourceClient):
        self.client = client
        self.repository = RentalRepository()

    def run(self):

        raw_records = self.client.fetch()

        for record in raw_records:
            listing = RentalParser.parse(
                record,
                self.client.__class__.__name__,
            )

            listing = RentalNormalizer.normalize(listing)

            self.repository.save(listing)
