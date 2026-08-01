from psycopg import connect

from elt.common.config import settings
from .models import RawRentalListing


class RentalRepository:

    def __init__(self):
        self.conn = connect(
            settings.database_url,
            autocommit=False,
        )

    def create_scrape_run(self):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                SELECT scrape_source_id
                FROM metadata.scrape_source
                WHERE source_name = %s;
                """,
                ("bangalore_rent_dataset",),
            )

            scrape_source_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO metadata.scrape_run
                (
                    scrape_source_id,
                    started_at,
                    status
                )
                VALUES
                (
                    %s,
                    NOW(),
                    'RUNNING'
                )
                RETURNING scrape_run_id;
                """,
                (scrape_source_id,),
            )

            scrape_run_id = cur.fetchone()[0]

        self.conn.commit()

        return scrape_run_id

    def save(
        self,
        scrape_run_id,
        listing: RawRentalListing,
    ):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO raw.raw_listing
                (
                    scrape_run_id,
                    external_listing_id,
                    source_url,
                    payload,
                    scraped_at
                )
                VALUES
                (
                    %s,
                    %s,
                    NULL,
                    %s,
                    NOW()
                );
                """,
                (
                    scrape_run_id,
                    listing.external_listing_id,
                    listing.model_dump_json(),
                ),
            )

        self.conn.commit()

    def finish_scrape_run(
        self,
        scrape_run_id,
        inserted,
    ):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                UPDATE metadata.scrape_run
                SET
                    completed_at = NOW(),
                    status = 'COMPLETED',
                    records_scraped = %s,
                    records_inserted = %s
                WHERE scrape_run_id = %s;
                """,
                (
                    inserted,
                    inserted,
                    scrape_run_id,
                ),
            )

        self.conn.commit()
