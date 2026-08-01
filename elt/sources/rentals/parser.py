import re

from .models import RawRentalListing


class RentalParser:
    """Parse Bangalore rental CSV rows."""

    @staticmethod
    def parse(row: dict) -> RawRentalListing:

        rent = float(str(row["price"]).replace(",", ""))

        bathrooms = int(
            re.search(r"\d+", row["bathroom"]).group()
        )

        return RawRentalListing(

            source_name="bangalore_rent_dataset",

            external_listing_id="",

            title=None,

            description=None,

            property_type=row["property_type"],

            bhk=int(row["bedroom"]),

            rent_amount=rent,

            deposit_amount=None,

            maintenance_amount=None,

            furnishing_status=row["furnish_type"],

            area_sqft=float(row["area"]),

            locality=row["locality"],

            latitude=None,

            longitude=None,

            listing_url=None,
        )
