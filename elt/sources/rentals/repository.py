from .models import RawRentalListing


class RentalRepository:
    """Repository for persisting rental listings."""

    def save(self, listing: RawRentalListing) -> None:
        # Database insertion will be implemented later.
        print(f"Saving listing: {listing.external_listing_id}")
