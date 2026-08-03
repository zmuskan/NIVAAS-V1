from __future__ import annotations

from uuid import UUID

from backend.app.repositories.analytics_repository import AnalyticsRepository
from backend.app.schemas.analytics import (
    AnalyticsListResponse,
    AnalyticsResponse,
)


class AnalyticsService:

    def __init__(
        self,
        repository: AnalyticsRepository,
    ):
        self.repository = repository

    def list_all(self) -> AnalyticsListResponse:

        rows = self.repository.list_all()

        return AnalyticsListResponse(
            items=[
                AnalyticsResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )

    def get_by_locality(
        self,
        locality_id: UUID,
    ) -> AnalyticsResponse:

        row = self.repository.get_by_locality(locality_id)

        if row is None:
            raise ValueError("Analytics not found.")

        return AnalyticsResponse.model_validate(row)

    def top_rent(
        self,
        limit: int,
    ) -> AnalyticsListResponse:

        rows = self.repository.top_rent(limit)

        return AnalyticsListResponse(
            items=[
                AnalyticsResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )

    def top_listing_count(
        self,
        limit: int,
    ) -> AnalyticsListResponse:

        rows = self.repository.top_listing_count(limit)

        return AnalyticsListResponse(
            items=[
                AnalyticsResponse.model_validate(row)
                for row in rows
            ],
            total=len(rows),
        )
