"""
elt/core/repository.py

Core repository layer for the ELT pipeline.

Reads validated rows from staging.staging_listing and promotes them into
the core/history schema tables (core.property, core.listing,
history.price_history, history.availability_history) using plain
psycopg3 SQL. No ORM, no SQLAlchemy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

from elt.common.config import settings
from elt.common.database import get_connection
from elt.core.matcher import PropertyMatcher


@dataclass
class StagingRecord:
    staging_listing_id: UUID
    raw_listing_id: Optional[UUID]
    scrape_run_id: UUID
    external_listing_id: Optional[str]
    property_type: Optional[str]
    bhk: Optional[int]
    bathrooms: Optional[int]
    rent_amount: Optional[float]
    deposit_amount: Optional[float]
    maintenance_amount: Optional[float]
    furnishing_status: Optional[str]
    area_sqft: Optional[float]
    locality: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    listing_url: Optional[str]
    validation_status: str
    validation_errors: Optional[str]
    transformed_at: Any


class CoreRepository:
    """Encapsulates all SQL access needed to promote staging listings
    into the core/history schema."""

    def __init__(self) -> None:
        self._ctx = get_connection(settings)
        self._conn = self._ctx.__enter__()

    def close(self) -> None:
        self._ctx.__exit__(None, None, None)

    # ------------------------------------------------------------------
    # Staging reads
    # ------------------------------------------------------------------
    def fetch_staging_records(self, limit: int) -> list[StagingRecord]:
        query = """
            SELECT staging_listing_id, raw_listing_id, scrape_run_id,
                   external_listing_id, property_type, bhk, bathrooms,
                   rent_amount, deposit_amount, maintenance_amount,
                   furnishing_status, area_sqft, locality, latitude,
                   longitude, listing_url, validation_status,
                   validation_errors, transformed_at
            FROM staging.staging_listing
            WHERE validation_status = 'VALID'
            ORDER BY staging_listing_id
            LIMIT %s
        """
        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

        return [StagingRecord(**row) for row in rows]

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------
    def lookup_locality_id(self, name: str) -> Optional[UUID]:
        query = """
            SELECT locality_id
            FROM core.locality
            WHERE LOWER(name) = LOWER(%s)
        """
        with self._conn.cursor() as cur:
            cur.execute(query, (name,))
            row = cur.fetchone()

        if row is None:
            return None
        return row[0]

    def lookup_scrape_source_id(self, scrape_run_id: UUID) -> Optional[UUID]:
        query = """
            SELECT scrape_source_id
            FROM metadata.scrape_run
            WHERE scrape_run_id = %s
        """
        with self._conn.cursor() as cur:
            cur.execute(query, (scrape_run_id,))
            row = cur.fetchone()

        if row is None:
            return None
        return row[0]

    # ------------------------------------------------------------------
    # Property
    # ------------------------------------------------------------------
    def get_or_create_property(
        self,
        locality_name: str,
        locality_id: UUID,
        property_type: Optional[str],
        bhk: Optional[int],
        bathrooms: Optional[int],
        area_sqft: Optional[float],
        furnishing_status: Optional[str],
        latitude: Optional[float],
        longitude: Optional[float],
    ) -> UUID:

        property_hash = PropertyMatcher.compute_hash(
            locality=locality_name,
            property_type=property_type or "",
            bhk=bhk or 0,
            area_sqft=float(area_sqft or 0),
        )

        select_query = """
            SELECT property_id
            FROM core.property
            WHERE property_hash = %s
        """
        insert_query = """
            INSERT INTO core.property (
                locality_id, property_type, bhk, bathrooms,
                area_sqft, furnishing_status, latitude, longitude,
                geometry, property_hash
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s
            )
            RETURNING property_id
        """

        with self._conn.cursor() as cur:
            cur.execute(select_query, (property_hash,))
            row = cur.fetchone()
            if row is not None:
                return row[0]

            cur.execute(
                insert_query,
                (
                    locality_id,
                    property_type,
                    bhk,
                    bathrooms,
                    area_sqft,
                    furnishing_status,
                    latitude,
                    longitude,
                    longitude,
                    latitude,
                    property_hash,
                ),
            )
            new_row = cur.fetchone()

        return new_row[0]

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------
    def insert_listing(
        self,
        raw_listing_id: UUID,
        property_id: UUID,
        scrape_source_id: UUID,
        external_listing_id: Optional[str],
        listing_url: Optional[str],
        rent_amount: Optional[float],
        deposit_amount: Optional[float],
        maintenance_amount: Optional[float],
    ) -> Optional[UUID]:

        query = """
            INSERT INTO core.listing (
                raw_listing_id,
                property_id,
                scrape_source_id,
                external_listing_id,
                listing_url,
                title,
                description,
                rent_amount,
                deposit_amount,
                maintenance_amount,
                available_from,
                listing_status
            )
            SELECT
                %s,
                %s,
                %s,
                %s,
                %s,
                NULL,
                NULL,
                %s,
                %s,
                %s,
                NULL,
                'active'
            WHERE NOT EXISTS (
                SELECT 1
                FROM core.listing
                WHERE raw_listing_id = %s
            )
            RETURNING property_id;
        """

        with self._conn.cursor() as cur:

            cur.execute(
                query,
                (
                    raw_listing_id,
                    property_id,
                    scrape_source_id,
                    external_listing_id,
                    listing_url,
                    rent_amount,
                    deposit_amount,
                    maintenance_amount,
                    raw_listing_id,
                ),
            )

            row = cur.fetchone()


        if row is None:
            return None

        return row[0]

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------
    def insert_price_history(
        self, property_id: UUID, rent_amount: Optional[float]
    ) -> None:
        query = """
            INSERT INTO history.price_history (property_id, rent_amount)
            VALUES (%s, %s)
        """
        with self._conn.cursor() as cur:
            cur.execute(query, (property_id, rent_amount))

    def insert_availability_history(self, property_id: UUID) -> None:
        query = """
            INSERT INTO history.availability_history (property_id, status)
            VALUES (%s, 'active')
        """
        with self._conn.cursor() as cur:
            cur.execute(query, (property_id,))

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def process_record(self, record: StagingRecord) -> bool:
        """Processes one validated staging record."""

        try:
            if not record.locality:
                raise ValueError(
                    f"Missing locality for staging_listing_id="
                    f"{record.staging_listing_id}"
                )


            locality_id = self.lookup_locality_id(record.locality)
            if locality_id is None:
                raise ValueError(
                    f"Locality not found for staging_listing_id="
                    f"{record.staging_listing_id}: {record.locality!r}"
                )

            scrape_source_id = self.lookup_scrape_source_id(
                record.scrape_run_id
            )
            if scrape_source_id is None:
                raise ValueError(
                    f"Scrape source not found for scrape_run_id="
                    f"{record.scrape_run_id}"
                )

            if record.latitude is None:
                record.latitude = 0.0

            if record.longitude is None:
                record.longitude = 0.0



            property_id = self.get_or_create_property(
                locality_name=record.locality,
                locality_id=locality_id,
                property_type=record.property_type,
                bhk=record.bhk,
                bathrooms=record.bathrooms,
                area_sqft=record.area_sqft,
                furnishing_status=record.furnishing_status,
                latitude=record.latitude,
                longitude=record.longitude,
            )

            # print("RAW LISTING ID =", record.raw_listing_id)
            inserted_property_id = self.insert_listing(
                raw_listing_id=record.raw_listing_id,
                property_id=property_id,
                scrape_source_id=scrape_source_id,
                external_listing_id=record.external_listing_id,
                listing_url=record.listing_url,
                rent_amount=record.rent_amount,
                deposit_amount=record.deposit_amount,
                maintenance_amount=record.maintenance_amount,
            )

            if inserted_property_id is not None:
                self.insert_price_history(
                    property_id,
                    record.rent_amount,
                )
                self.insert_availability_history(property_id)


            self._conn.commit()
            return True

        except Exception:
            import traceback
            traceback.print_exc()
            self._conn.rollback()
            raise
