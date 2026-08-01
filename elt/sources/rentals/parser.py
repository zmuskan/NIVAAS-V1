from .models import RawRentalListing


class RentalParser:
    """Convert raw API responses into RawRentalListing objects."""

    @staticmethod
    def parse(data: dict, source_name: str) -> RawRentalListing:
        return RawRentalListing(
            source_name=source_name,
            external_listing_id=str(data.get("id", "")),
            title=data.get("title"),
            description=data.get("description"),
            property_type=data.get("property_type"),
            bhk=data.get("bhk"),
            rent_amount=data.get("rent"),
            deposit_amount=data.get("deposit"),
            maintenance_amount=data.get("maintenance"),
            furnishing_status=data.get("furnishing"),
            area_sqft=data.get("area_sqft"),
            locality=data.get("locality"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            listing_url=data.get("url"),
        )
