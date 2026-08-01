import re

from .models import RawRentalListing


class RentalParser:
    """Parse Bangalore rental CSV rows into RawRentalListing."""

    @staticmethod
    def _to_int(value):
        if value is None:
            return None

        match = re.search(r"\d+", str(value))
        return int(match.group()) if match else None

    @staticmethod
    def _to_float(value):
        if value is None:
            return None

        value = str(value).replace(",", "").strip()

        if value == "":
            return None

        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def parse(row: dict) -> RawRentalListing:

        return RawRentalListing(

            source_name="bangalore_rent_dataset",

            external_listing_id="",

            title=None,

            description=None,

            property_type=row.get("property_type"),

            bhk=RentalParser._to_int(row.get("bedroom")),

            bathrooms=RentalParser._to_int(row.get("bathroom")),

            rent_amount=RentalParser._to_float(row.get("price")),

            deposit_amount=None,

            maintenance_amount=None,

            furnishing_status=row.get("furnish_type"),

            area_sqft=RentalParser._to_float(row.get("area")),

            locality=row.get("locality"),

            latitude=None,

            longitude=None,

            listing_url=None,
        )
