-- ============================================================
-- NIVAAS
-- Locality Feature Store
-- ============================================================

CREATE TABLE IF NOT EXISTS feature_store.locality_feature (
    locality_feature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    locality_id UUID NOT NULL,

    feature_name VARCHAR(150) NOT NULL,
    feature_value DOUBLE PRECISION NOT NULL,

    calculation_version VARCHAR(50) NOT NULL DEFAULT '1.0',
    calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_locality_feature_locality
        FOREIGN KEY (locality_id)
        REFERENCES core.locality(locality_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_locality_feature
        UNIQUE (
            locality_id,
            feature_name,
            calculation_version
        ),

    CONSTRAINT chk_locality_feature_name
        CHECK (LENGTH(TRIM(feature_name)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_locality_feature_locality
    ON feature_store.locality_feature(locality_id);

CREATE INDEX IF NOT EXISTS idx_locality_feature_name
    ON feature_store.locality_feature(feature_name);
