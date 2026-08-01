from .models import RawRentalListing


class RentalNormalizer:

    @staticmethod
    def normalize(
        listing: RawRentalListing,
    ) -> RawRentalListing:

        if listing.locality:
            listing.locality = (
                listing.locality.strip().title()
            )

        if listing.furnishing_status:
            listing.furnishing_status = (
                listing.furnishing_status
                .strip()
                .title()
            )

        if listing.property_type:
            listing.property_type = (
                listing.property_type
                .strip()
                .title()
            )

        return listing
