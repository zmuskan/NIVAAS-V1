import psycopg
from psycopg.rows import dict_row


class SimilarRepository:

    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def fetch_property(self, property_id):

        query = """
        SELECT

            p.property_id,
            p.locality_id,
            p.property_type,
            p.bhk,
            p.area_sqft,
            li.rent_amount

        FROM core.property p

        JOIN core.listing li
        ON li.property_id=p.property_id

        WHERE p.property_id=%s
        """

        with self.conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (property_id,))

            return cur.fetchone()

    def fetch_candidates(self, property_id):

        query = """
        SELECT

            p.property_id,

            l.name locality_name,

            p.property_type,

            p.bhk,

            p.area_sqft,

            li.rent_amount

        FROM core.property p

        JOIN core.locality l
        ON l.locality_id=p.locality_id

        JOIN core.listing li
        ON li.property_id=p.property_id

        WHERE p.property_id<>%s
        """

        with self.conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (property_id,))

            return cur.fetchall()
