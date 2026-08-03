from __future__ import annotations

from psycopg.rows import dict_row

from elt.common.config import settings
from elt.common.database import get_connection


class AnalyticsRepository:

    def __init__(self):
        self._ctx = get_connection(settings)
        self._conn = self._ctx.__enter__()

    # ------------------------------------------------------------------
    # Fetch all locality metrics
    # ------------------------------------------------------------------

    def fetch_locality_metrics(self):

        query = """
        SELECT

            p.locality_id,

            COUNT(*)::INTEGER AS listing_count,

            ROUND(
                AVG(l.rent_amount)::numeric,
                2
            ) AS avg_rent,

            PERCENTILE_CONT(0.5)
            WITHIN GROUP
            (
                ORDER BY l.rent_amount
            ) AS median_rent,

            ROUND(
                AVG(
                    l.rent_amount /
                    NULLIF(p.area_sqft,0)
                )::numeric,
                2
            ) AS avg_rent_per_sqft,

            ROUND(
                AVG(p.area_sqft)::numeric,
                2
            ) AS avg_area_sqft,

            ROUND(
                AVG(p.bhk)::numeric,
                2
            ) AS avg_bhk,

            MIN(l.rent_amount) AS min_rent,

            MAX(l.rent_amount) AS max_rent,

            ROUND(
                AVG(l.deposit_amount)::numeric,
                2
            ) AS avg_deposit,

            PERCENTILE_CONT(0.5)
            WITHIN GROUP
            (
                ORDER BY l.deposit_amount
            ) AS median_deposit,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.property_type='APARTMENT'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS apartment_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.property_type='INDEPENDENT HOUSE'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS independent_house_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.property_type='INDEPENDENT FLOOR'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS independent_floor_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.property_type='STUDIO APARTMENT'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS studio_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.property_type='VILLA'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS villa_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.furnishing_status='FULLY FURNISHED'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS furnished_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.furnishing_status='SEMI FURNISHED'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS semi_furnished_pct,

            ROUND(
                100.0 *
                AVG(
                    CASE
                        WHEN p.furnishing_status='UNFURNISHED'
                        THEN 1
                        ELSE 0
                    END
                ),
                2
            ) AS unfurnished_pct

        FROM core.listing l

        JOIN core.property p
          ON l.property_id = p.property_id

        GROUP BY p.locality_id

        ORDER BY p.locality_id;
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query)

            return cur.fetchall()


    # ------------------------------------------------------------------
    # Save metrics
    # ------------------------------------------------------------------

    def save_metrics(self, rows):

        query = """
        INSERT INTO analytics.locality_metrics
        (
            locality_id,
            listing_count,
            avg_rent,
            median_rent,
            avg_rent_per_sqft,
            avg_area_sqft,
            avg_bhk,
            min_rent,
            max_rent,
            avg_deposit,
            median_deposit,
            apartment_pct,
            independent_house_pct,
            independent_floor_pct,
            studio_pct,
            villa_pct,
            furnished_pct,
            semi_furnished_pct,
            unfurnished_pct
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
            %s,
            %s,
            %s,
            %s
        )

        ON CONFLICT (locality_id)

        DO UPDATE SET

            listing_count            = EXCLUDED.listing_count,
            avg_rent                 = EXCLUDED.avg_rent,
            median_rent              = EXCLUDED.median_rent,
            avg_rent_per_sqft        = EXCLUDED.avg_rent_per_sqft,
            avg_area_sqft            = EXCLUDED.avg_area_sqft,
            avg_bhk                  = EXCLUDED.avg_bhk,
            min_rent                 = EXCLUDED.min_rent,
            max_rent                 = EXCLUDED.max_rent,
            avg_deposit              = EXCLUDED.avg_deposit,
            median_deposit           = EXCLUDED.median_deposit,
            apartment_pct            = EXCLUDED.apartment_pct,
            independent_house_pct    = EXCLUDED.independent_house_pct,
            independent_floor_pct    = EXCLUDED.independent_floor_pct,
            studio_pct               = EXCLUDED.studio_pct,
            villa_pct                = EXCLUDED.villa_pct,
            furnished_pct            = EXCLUDED.furnished_pct,
            semi_furnished_pct       = EXCLUDED.semi_furnished_pct,
            unfurnished_pct          = EXCLUDED.unfurnished_pct,
            generated_at             = NOW();
        """

        with self._conn.cursor() as cur:

            for row in rows:

                cur.execute(
                    query,
                    (
                        row["locality_id"],
                        row["listing_count"],
                        row["avg_rent"],
                        row["median_rent"],
                        row["avg_rent_per_sqft"],
                        row["avg_area_sqft"],
                        row["avg_bhk"],
                        row["min_rent"],
                        row["max_rent"],
                        row["avg_deposit"],
                        row["median_deposit"],
                        row["apartment_pct"],
                        row["independent_house_pct"],
                        row["independent_floor_pct"],
                        row["studio_pct"],
                        row["villa_pct"],
                        row["furnished_pct"],
                        row["semi_furnished_pct"],
                        row["unfurnished_pct"],
                    ),
                )

        self._conn.commit()

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self):

        self._ctx.__exit__(None, None, None)
