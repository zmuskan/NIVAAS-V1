from .models import RawRentalListing


class RentalNormalizer:
    """Normalize rental listing values."""

    @staticmethod
    def normalize(listing: RawRentalListing) -> RawRentalListing:

        if listing.furnishing_status:
            listing.furnishing_status = (
                listing.furnishing_status.strip().lower()
            )

        if listing.locality:
            listing.locality = listing.locality.strip().title()

        return listing
