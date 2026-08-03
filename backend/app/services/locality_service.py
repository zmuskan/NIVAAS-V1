from __future__ import annotations

from uuid import UUID

from backend.app.repositories.locality_repository import (
    LocalityRepository,
)
from backend.app.schemas.locality import (
    LocalityListResponse,
    LocalityResponse,
)


class LocalityService:

    def __init__(
        self,
        repository: LocalityRepository,
    ):

        self.repository = repository

    def list_localities(
        self,
        limit: int,
        offset: int,
    ) -> LocalityListResponse:

        rows = self.repository.list_localities(limit, offset)

        total = self.repository.count_localities()

        return LocalityListResponse(

            items=[
                LocalityResponse.model_validate(row)
                for row in rows
            ],

            total=total,
            limit=limit,
            offset=offset,
        )

    def get_locality(
        self,
        locality_id: UUID,
    ) -> LocalityResponse:

        row = self.repository.get_locality(locality_id)

        if row is None:

            raise ValueError("Locality not found.")

        return LocalityResponse.model_validate(row)
