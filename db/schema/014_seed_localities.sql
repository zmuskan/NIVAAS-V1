INSERT INTO core.locality
(
    name,
    city,
    state,
    boundary,
    centroid
)
SELECT DISTINCT
    locality,
    'Bengaluru',
    'Karnataka',
    ST_GeomFromText(
        'MULTIPOLYGON EMPTY',
        4326
    ),
    ST_GeomFromText(
        'POINT EMPTY',
        4326
    )
FROM staging.staging_listing
WHERE locality IS NOT NULL
AND TRIM(locality) <> ''
ON CONFLICT (name, city)
DO NOTHING;
