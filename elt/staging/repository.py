from __future__ import annotations

import json
from typing import Any

from psycopg import connect
from psycopg.rows import dict_row

from elt.common.config import settings
from .transformer import StagingListing


class StagingRepository:
    def __init__(self):
        self.conn = connect(settings.database_url)

    def fetch_raw_listings(self) -> list[dict[str, Any]]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    raw_listing_id,
                    scrape_run_id,
                    payload
                FROM raw.raw_listing
                ORDER BY scraped_at;
                """
            )

            return cur.fetchall()

    def save(self, listing: StagingListing):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO staging.staging_listing
                (
                    raw_listing_id,
                    scrape_run_id,
                    external_listing_id,
                    property_type,
                    bhk,
                    bathrooms,
                    rent_amount,
                    deposit_amount,
                    maintenance_amount,
                    furnishing_status,
                    area_sqft,
                    locality,
                    latitude,
                    longitude,
                    listing_url,
                    validation_status,
                    validation_errors,
                    transformed_at
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    'VALID',
                    NULL,
                    %s
                )
                ON CONFLICT (raw_listing_id)
                DO NOTHING;
                """,
                (
                    listing.raw_listing_id,
                    listing.scrape_run_id,
                    listing.external_listing_id,
                    listing.property_type,
                    listing.bhk,
                    listing.bathrooms,
                    listing.rent_amount,
                    listing.deposit_amount,
                    listing.maintenance_amount,
                    listing.furnishing_status,
                    listing.area_sqft,
                    listing.locality,
                    listing.latitude,
                    listing.longitude,
                    listing.listing_url,
                    listing.transformed_at,
                ),
            )

        self.conn.commit()

    def save_invalid(
        self,
        raw_listing_id,
        issues,
    ):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO staging.staging_listing
                (
                    raw_listing_id,
                    validation_status,
                    validation_errors
                )
                VALUES
                (
                    %s,
                    'INVALID',
                    %s
                )
                ON CONFLICT (raw_listing_id)
                DO UPDATE
                SET
                    validation_status = EXCLUDED.validation_status,
                    validation_errors = EXCLUDED.validation_errors;
                """,
                (
                    raw_listing_id,
                    json.dumps(
                        [
                            {
                                "field": i.field_name,
                                "code": i.code.value,
                                "message": i.message,
                            }
                            for i in issues
                        ]
                    ),
                ),
            )

        self.conn.commit()

    def close(self):
        self.conn.close()
