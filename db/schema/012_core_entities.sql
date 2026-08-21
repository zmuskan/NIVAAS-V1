CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS history;

--------------------------------------------------
-- CORE PROPERTY
--------------------------------------------------

CREATE TABLE IF NOT EXISTS core.property
(
    property_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_hash TEXT NOT NULL UNIQUE,

    property_type VARCHAR(100),

    bhk INTEGER,

    bathrooms INTEGER,

    area_sqft NUMERIC(10,2),

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    locality VARCHAR(150),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

--------------------------------------------------
-- CORE LISTING
--------------------------------------------------

CREATE TABLE IF NOT EXISTS core.listing
(
    listing_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    raw_listing_id UUID
        REFERENCES raw.raw_listing(raw_listing_id)
        ON DELETE CASCADE,

    scrape_run_id UUID
        REFERENCES metadata.scrape_run(scrape_run_id)
        ON DELETE SET NULL,

    rent_amount NUMERIC(12,2),

    deposit_amount NUMERIC(12,2),

    maintenance_amount NUMERIC(12,2),

    listing_url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

--------------------------------------------------
-- PRICE HISTORY
--------------------------------------------------

CREATE TABLE IF NOT EXISTS history.price_history
(
    price_history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    rent_amount NUMERIC(12,2),

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

--------------------------------------------------
-- AVAILABILITY HISTORY
--------------------------------------------------

CREATE TABLE IF NOT EXISTS history.availability_history
(
    availability_history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    status VARCHAR(30),

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

