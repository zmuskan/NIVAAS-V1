ALTER TABLE core.locality
    ADD COLUMN IF NOT EXISTS boundary_source VARCHAR(100),
    ADD COLUMN IF NOT EXISTS boundary_source_type VARCHAR(30),
    ADD COLUMN IF NOT EXISTS boundary_source_id BIGINT,
    ADD COLUMN IF NOT EXISTS boundary_quality VARCHAR(30);

CREATE UNIQUE INDEX IF NOT EXISTS uq_locality_boundary_source
    ON core.locality (
        boundary_source,
        boundary_source_type,
        boundary_source_id
    )
    WHERE boundary_source_id IS NOT NULL;

ALTER TABLE core.locality
    DROP CONSTRAINT IF EXISTS chk_locality_boundary_quality;

ALTER TABLE core.locality
    ADD CONSTRAINT chk_locality_boundary_quality
    CHECK (
        boundary_quality IS NULL
        OR boundary_quality IN (
            'verified',
            'osm_boundary',
            'approximate'
        )
    );
