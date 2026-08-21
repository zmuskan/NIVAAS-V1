from __future__ import annotations

from uuid import UUID

from backend.app.repositories.property_repository import PropertyRepository
from backend.app.schemas.property import (
    PropertyListResponse,
    PropertyResponse,
)

class PropertyService:

    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def list_properties(
        self,
        limit: int,
        offset: int,
    ) -> PropertyListResponse:

        rows = self.repository.list_properties(limit, offset)

        return PropertyListResponse(
            items=[
                PropertyResponse.model_validate(row)
                for row in rows
            ],
            total=self.repository.count_properties(),
        )

    def get_property(
        self,
        property_id: UUID,
    ) -> PropertyResponse:

        row = self.repository.get_property(property_id)

        if row is None:
            raise ValueError("Property not found.")

        return PropertyResponse.model_validate(row)

    def properties_by_locality(
        self,
        locality_id: UUID,
    ) -> PropertyListResponse:

        rows = self.repository.get_by_locality(locality_id)

        return PropertyListResponse(
            items=[
                PropertyResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )

    def search(
        self,
        min_rent: float | None,
        max_rent: float | None,
        bhk: int | None,
    ) -> PropertyListResponse:

        rows = self.repository.search(
            min_rent=min_rent,
            max_rent=max_rent,
            bhk=bhk,
        )

        return PropertyListResponse(
            items=[
                PropertyResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )

    def get_recommendations(
        self,
        budget: float,
        bhk: int | None,
        limit: int,
    ) -> PropertyListResponse:

        rows = self.repository.get_recommendations(
            budget=budget,
            bhk=bhk,
            limit=limit,
        )

        return PropertyListResponse(
            items=[
                PropertyResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )
