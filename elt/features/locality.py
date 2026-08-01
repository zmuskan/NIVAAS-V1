from __future__ import annotations

import logging
from dataclasses import dataclass

from elt.common.config import Settings
from elt.common.database import get_connection


logger = logging.getLogger(__name__)


AMENITY_TYPES = (
    "restaurant",
    "hospital",
    "school",
    "supermarket",
    "park",
    "gym",
    "bus_stop",
    "metro_station",
)

CALCULATION_VERSION = "1.0"


@dataclass(frozen=True, slots=True)
class FeaturePipelineResult:
    localities_processed: int
    features_written: int


def _feature_rows_for_locality(
    connection,
    locality_id: str,
) -> list[tuple[str, float]]:
    row = connection.execute(
        """
        SELECT
            ST_Area(geometry::geography) / 1000000.0
        FROM core.locality
        WHERE locality_id = %s
        """,
        (locality_id,),
    ).fetchone()

    if row is None:
        raise ValueError(f"Unknown locality: {locality_id}")

    area_km2 = float(row[0])

    if area_km2 <= 0:
        raise ValueError(
            f"Locality has invalid area: {locality_id}"
        )

    counts = {
        amenity_type: 0
        for amenity_type in AMENITY_TYPES
    }

    rows = connection.execute(
        """
        SELECT
            amenity_type,
            COUNT(*)
        FROM core.amenity
        WHERE locality_id = %s
        GROUP BY amenity_type
        """,
        (locality_id,),
    ).fetchall()

    for amenity_type, count in rows:
        if amenity_type in counts:
            counts[amenity_type] = int(count)

    total = sum(counts.values())

    features: list[tuple[str, float]] = [
        ("area_km2", area_km2),
        ("amenity_total", float(total)),
        (
            "amenity_density_per_km2",
            float(total) / area_km2,
        ),
    ]

    for amenity_type in AMENITY_TYPES:
        count = counts[amenity_type]

        features.append(
            (
                f"{amenity_type}_count",
                float(count),
            )
        )

        features.append(
            (
                f"{amenity_type}_density_per_km2",
                float(count) / area_km2,
            )
        )

    metro_row = connection.execute(
        """
        SELECT MIN(
            ST_Distance(
                l.geometry::geography,
                a.geometry::geography
            )
        )
        FROM core.locality l
        CROSS JOIN core.amenity a
        WHERE l.locality_id = %s
          AND a.amenity_type = 'metro_station'
        """,
        (locality_id,),
    ).fetchone()

    if metro_row is not None and metro_row[0] is not None:
        features.append(
            (
                "nearest_metro_distance_m",
                float(metro_row[0]),
            )
        )

    return features


def _upsert_feature(
    connection,
    locality_id: str,
    feature_name: str,
    feature_value: float,
) -> None:
    connection.execute(
        """
        INSERT INTO feature_store.locality_feature (
            locality_id,
            feature_name,
            feature_value,
            calculation_version,
            calculated_at
        )
        VALUES (%s, %s, %s, %s, NOW())

        ON CONFLICT (
            locality_id,
            feature_name,
            calculation_version
        )
        DO UPDATE SET
            feature_value = EXCLUDED.feature_value,
            calculated_at = NOW()
        """,
        (
            locality_id,
            feature_name,
            feature_value,
            CALCULATION_VERSION,
        ),
    )


def run_locality_feature_pipeline(
    settings: Settings,
) -> FeaturePipelineResult:
    logger.info(
        "Starting NIVAAS locality feature engineering"
    )

    with get_connection(settings) as connection:
        localities = connection.execute(
            """
            SELECT locality_id
            FROM core.locality
            WHERE geometry IS NOT NULL
            ORDER BY name
            """
        ).fetchall()

        features_written = 0

        for (locality_id,) in localities:
            features = _feature_rows_for_locality(
                connection,
                str(locality_id),
            )

            for feature_name, feature_value in features:
                _upsert_feature(
                    connection,
                    str(locality_id),
                    feature_name,
                    feature_value,
                )
                features_written += 1

    result = FeaturePipelineResult(
        localities_processed=len(localities),
        features_written=features_written,
    )

    logger.info(
        (
            "Locality feature engineering completed: "
            "localities=%s features=%s"
        ),
        result.localities_processed,
        result.features_written,
    )

    return result
