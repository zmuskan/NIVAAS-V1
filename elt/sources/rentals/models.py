from typing import Optional

from pydantic import BaseModel


class RawRentalListing(BaseModel):

    source_name: str
    external_listing_id: str

    title: Optional[str] = None
    description: Optional[str] = None

    property_type: Optional[str] = None

    bhk: Optional[int] = None
    bathrooms: Optional[int] = None

    rent_amount: Optional[float] = None
    deposit_amount: Optional[float] = None
    maintenance_amount: Optional[float] = None

    furnishing_status: Optional[str] = None

    area_sqft: Optional[float] = None

    locality: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    listing_url: Optional[str] = None
