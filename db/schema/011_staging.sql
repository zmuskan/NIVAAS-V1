-- =====================================================
-- NIVAAS
-- Staging Schema
-- =====================================================

CREATE TABLE IF NOT EXISTS staging.staging_listing (

    staging_listing_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    raw_listing_id UUID NOT NULL,

    scrape_run_id UUID,

    external_listing_id TEXT,

    property_type VARCHAR(100),

    bhk INTEGER,

    bathrooms INTEGER,

    rent_amount NUMERIC(12,2),

    deposit_amount NUMERIC(12,2),

    maintenance_amount NUMERIC(12,2),

    furnishing_status VARCHAR(50),

    area_sqft NUMERIC(10,2),

    locality VARCHAR(150),

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    listing_url TEXT,

    validation_status VARCHAR(20) NOT NULL DEFAULT 'VALID',

    validation_errors JSONB,

    transformed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_raw_listing
        FOREIGN KEY (raw_listing_id)
        REFERENCES raw.raw_listing(raw_listing_id)
        ON DELETE CASCADE
);
