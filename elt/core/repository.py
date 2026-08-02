"""
elt/core/repository.py

Persistence layer for the NIVAAS core pipeline.

Responsible for:
    - Reading valid, unprocessed rows from staging.staging_listing.
    - Getting-or-creating deduplicated properties in core.property
      (keyed by a pre-computed property_hash).
    - Inserting listings into core.listing.
    - Recording rent snapshots into history.price_history.
    - Recording availability snapshots into history.availability_history.

Uses psycopg3 exclusively (no ORM). Property hashing is computed
externally by the matcher and passed in; this module performs no
hashing itself.

Only the following columns/tables are used, exactly as specified:

staging.staging_listing:
    raw_listing_id, scrape_run_id, external_listing_id, property_type,
    bhk, bathrooms, rent_amount, deposit_amount, maintenance_amount,
    furnishing_status, area_sqft, locality, latitude, longitude,
    listing_url, validation_status, validation_errors, transformed_at

core.property:
    property_id, property_hash, property_type, bhk, bathrooms,
    area_sqft, latitude, longitude, locality, created_at, updated_at

core.listing:
    listing_id, property_id, raw_listing_id, scrape_run_id, rent_amount,
    deposit_amount, maintenance_amount, listing_url, created_at

history.price_history:
    price_history_id, property_id, rent_amount, recorded_at

history.availability_history:
    availability_history_id, property_id, status, recorded_at
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

from elt.common.database import get_connection
from elt.common.config import settings


@dataclass
class StagingListingRecord:
    raw_listing_id: UUID
    scrape_run_id: Optional[UUID]
    external_listing_id: Optional[str]
    property_type: str
    bhk: int
    bathrooms: Optional[int]
    rent_amount: float
    deposit_amount: Optional[float]
    maintenance_amount: Optional[float]
    furnishing_status: Optional[str]
    area_sqft: float
    locality: str
    latitude: Optional[float]
    longitude: Optional[float]
    listing_url: Optional[str]
    validation_status: str
    validation_errors: Optional[Any]
    transformed_at: Optional[datetime]


@dataclass
class PropertyResult:
    property_id: UUID
    was_created: bool


@dataclass
class ListingResult:
    listing_id: UUID
    was_created: bool


class CoreRepository:
    """Handles all database access for the core (property/listing) pipeline."""

    FETCH_STAGING_RECORDS_SQL = """
        SELECT
            sl.raw_listing_id,
            sl.scrape_run_id,
            sl.external_listing_id,
            sl.property_type,
            sl.bhk,
            sl.bathrooms,
            sl.rent_amount,
            sl.deposit_amount,
            sl.maintenance_amount,
            sl.furnishing_status,
            sl.area_sqft,
            sl.locality,
            sl.latitude,
            sl.longitude,
            sl.listing_url,
            sl.validation_status,
            sl.validation_errors,
            sl.transformed_at
        FROM staging.staging_listing sl
        WHERE sl.validation_status = 'VALID'
          AND NOT EXISTS (
            SELECT 1
            FROM core.listing cl
            WHERE cl.external_listing_id = sl.external_listing_id
        )
        ORDER BY sl.transformed_at ASC NULLS LAST, sl.raw_listing_id ASC
        LIMIT %(limit)s
    """

    SELECT_PROPERTY_BY_HASH_SQL = """
        SELECT property_id
        FROM core.property
        WHERE property_hash = %(property_hash)s
    """

    INSERT_PROPERTY_SQL = """
        INSERT INTO core.property (
            property_hash,
            property_type,
            bhk,
            bathrooms,
            area_sqft,
            latitude,
            longitude,
            locality,
            created_at,
            updated_at
        )
        VALUES (
            %(property_hash)s,
            %(property_type)s,
            %(bhk)s,
            %(bathrooms)s,
            %(area_sqft)s,
            %(latitude)s,
            %(longitude)s,
            %(locality)s,
            now(),
            now()
        )
        ON CONFLICT (property_hash) DO NOTHING
        RETURNING property_id
    """

    INSERT_LISTING_SQL = """
        INSERT INTO core.listing (
            property_id,
            raw_listing_id,
            scrape_run_id,
            rent_amount,
            deposit_amount,
            maintenance_amount,
            listing_url,
            created_at
        )
        VALUES (
            %(property_id)s,
            %(raw_listing_id)s,
            %(scrape_run_id)s,
            %(rent_amount)s,
            %(deposit_amount)s,
            %(maintenance_amount)s,
            %(listing_url)s,
            now()
        )
        ON CONFLICT (raw_listing_id) DO NOTHING
        RETURNING listing_id
    """

    SELECT_LISTING_BY_RAW_LISTING_ID_SQL = """
        SELECT listing_id
        FROM core.listing
        WHERE raw_listing_id = %(raw_listing_id)s
    """

    INSERT_PRICE_HISTORY_SQL = """
        INSERT INTO history.price_history (
            property_id,
            rent_amount,
            recorded_at
        )
        VALUES (
            %(property_id)s,
            %(rent_amount)s,
            %(recorded_at)s
        )
    """

    INSERT_AVAILABILITY_HISTORY_SQL = """
        INSERT INTO history.availability_history (
            property_id,
            status,
            recorded_at
        )
        VALUES (
            %(property_id)s,
            %(status)s,
            %(recorded_at)s
        )
    """

    def __init__(self, connection: Optional[psycopg.Connection] = None) -> None:
        self._external_connection = connection

    def _connection(self) -> psycopg.Connection:
        if self._external_connection is not None:
            return self._external_connection
        return get_connection(settings)

    def fetch_staging_records(self, limit: int) -> list[StagingListingRecord]:
        """Fetch a batch of valid staging listings not yet present in core.listing."""
        records: list[StagingListingRecord] = []

        with self._connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(self.FETCH_STAGING_RECORDS_SQL, {"limit": limit})
                rows = cur.fetchall()

        for row in rows:
            records.append(
                StagingListingRecord(
                    raw_listing_id=row["raw_listing_id"],
                    scrape_run_id=row["scrape_run_id"],
                    external_listing_id=row["external_listing_id"],
                    property_type=row["property_type"],
                    bhk=row["bhk"],
                    bathrooms=row["bathrooms"],
                    rent_amount=row["rent_amount"],
                    deposit_amount=row["deposit_amount"],
                    maintenance_amount=row["maintenance_amount"],
                    furnishing_status=row["furnishing_status"],
                    area_sqft=row["area_sqft"],
                    locality=row["locality"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    listing_url=row["listing_url"],
                    validation_status=row["validation_status"],
                    validation_errors=row["validation_errors"],
                    transformed_at=row["transformed_at"],
                )
            )

        return records

    def get_or_create_property(
        self,
        cur: psycopg.Cursor[Any],
        record: StagingListingRecord,
        property_hash: str,
    ) -> PropertyResult:
        """
        Get the existing property_id for property_hash, or create a new
        property if none exists. Must be called within an active
        transaction owned by the caller.
        """
        cur.execute(
            self.INSERT_PROPERTY_SQL,
            {
                "property_hash": property_hash,
                "property_type": record.property_type,
                "bhk": record.bhk,
                "bathrooms": record.bathrooms,
                "area_sqft": record.area_sqft,
                "latitude": record.latitude,
                "longitude": record.longitude,
                "locality": record.locality,
            },
        )
        inserted_row = cur.fetchone()

        if inserted_row is not None:
            return PropertyResult(property_id=inserted_row["property_id"], was_created=True)

        cur.execute(
            self.SELECT_PROPERTY_BY_HASH_SQL,
            {"property_hash": property_hash},
        )
        existing_row = cur.fetchone()
        assert existing_row is not None, (
            f"property_hash={property_hash} not found after failed insert; "
            "concurrent transaction may have rolled back."
        )
        return PropertyResult(property_id=existing_row["property_id"], was_created=False)

    def create_listing(
        self,
        cur: psycopg.Cursor[Any],
        record: StagingListingRecord,
        property_id: UUID,
    ) -> ListingResult:
        """
        Insert a listing for the given staging record and property_id.
        Idempotent per raw_listing_id. Must be called within an active
        transaction owned by the caller.
        """
        cur.execute(
            self.INSERT_LISTING_SQL,
            {
                "property_id": property_id,
                "raw_listing_id": record.raw_listing_id,
                "scrape_run_id": record.scrape_run_id,
                "rent_amount": record.rent_amount,
                "deposit_amount": record.deposit_amount,
                "maintenance_amount": record.maintenance_amount,
                "listing_url": record.listing_url,
            },
        )
        inserted_row = cur.fetchone()

        if inserted_row is not None:
            return ListingResult(listing_id=inserted_row["listing_id"], was_created=True)

        cur.execute(
            self.SELECT_LISTING_BY_RAW_LISTING_ID_SQL,
            {"raw_listing_id": record.raw_listing_id},
        )
        existing_row = cur.fetchone()
        assert existing_row is not None, (
            f"raw_listing_id={record.raw_listing_id} not found after "
            "failed listing insert; concurrent transaction may have rolled back."
        )
        return ListingResult(listing_id=existing_row["listing_id"], was_created=False)

    def create_price_history(
        self,
        cur: psycopg.Cursor[Any],
        property_id: UUID,
        record: StagingListingRecord,
        recorded_at: datetime,
    ) -> None:
        """
        Insert a rent snapshot for the given property. Must be called
        within an active transaction owned by the caller.
        """
        cur.execute(
            self.INSERT_PRICE_HISTORY_SQL,
            {
                "property_id": property_id,
                "rent_amount": record.rent_amount,
                "recorded_at": recorded_at,
            },
        )

    def create_availability_history(
        self,
        cur: psycopg.Cursor[Any],
        property_id: UUID,
        recorded_at: datetime,
        status: str = "ACTIVE",
    ) -> None:
        """
        Insert an availability snapshot for the given property. Must be
        called within an active transaction owned by the caller.
        """
        cur.execute(
            self.INSERT_AVAILABILITY_HISTORY_SQL,
            {
                "property_id": property_id,
                "status": status,
                "recorded_at": recorded_at,
            },
        )

    def process_staging_record(
        self,
        record: StagingListingRecord,
        property_hash: str,
    ) -> tuple[PropertyResult, ListingResult]:
        """
        Process a single staging record end-to-end inside one transaction:
            1. Get-or-create the property (deduplicated by property_hash).
            2. Create the listing (idempotent per raw_listing_id).
            3. Record price history (only if the listing was newly created).
            4. Record availability history (only if the listing was newly created).

        Rolls back the entire unit of work on any failure.
        """
        from datetime import timezone

        recorded_at = (
            record.transformed_at
            if record.transformed_at is not None
            else datetime.now(timezone.utc)
        )

        with self._connection() as conn:
            try:
                with conn.cursor(row_factory=dict_row) as cur:
                    property_result = self.get_or_create_property(cur, record, property_hash)
                    listing_result = self.create_listing(cur, record, property_result.property_id)

                    if listing_result.was_created:
                        self.create_price_history(cur, property_result.property_id, record, recorded_at)
                        self.create_availability_history(cur, property_result.property_id, recorded_at)

                conn.commit()
                return property_result, listing_result
            except Exception:
                conn.rollback()
                raise
