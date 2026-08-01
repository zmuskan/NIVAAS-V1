-- =====================================================
-- NIVAAS
-- Core Domain Tables
-- =====================================================

-- Tables implemented in this file:

-- core.locality
-- =====================================================
-- NIVAAS
-- Core Domain Tables
-- =====================================================

-- =====================================================
-- TABLE: core.locality
-- =====================================================

CREATE TABLE IF NOT EXISTS core.locality (

    locality_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(150) NOT NULL,

    city VARCHAR(100) NOT NULL,

    state VARCHAR(100) NOT NULL,

    country VARCHAR(100) NOT NULL DEFAULT 'India',

    pincode VARCHAR(10),

    boundary GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,

    centroid GEOMETRY(POINT, 4326) NOT NULL,

    area_sqkm NUMERIC(10,2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_locality UNIQUE (name, city)
);
-- core.property

-- =====================================================
-- TABLE: core.property
-- =====================================================

CREATE TABLE IF NOT EXISTS core.property (

    property_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    locality_id UUID NOT NULL
        REFERENCES core.locality(locality_id)
        ON DELETE RESTRICT,

    property_type VARCHAR(50) NOT NULL,

    address_line1 TEXT,

    address_line2 TEXT,

    postal_code VARCHAR(10),

    bhk SMALLINT NOT NULL,

    bathrooms SMALLINT,

    area_sqft NUMERIC(10,2) NOT NULL,

    floor_number SMALLINT,

    total_floors SMALLINT,

    furnishing_status VARCHAR(30),

    property_age INTEGER,

    latitude NUMERIC(9,6) NOT NULL,

    longitude NUMERIC(9,6) NOT NULL,

    geometry GEOMETRY(POINT,4326) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_property_bhk
        CHECK (bhk > 0),

    CONSTRAINT chk_property_area
        CHECK (area_sqft > 0),

    CONSTRAINT chk_property_lat
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT chk_property_lon
        CHECK (longitude BETWEEN -180 AND 180)

);
-- core.listing

-- =====================================================
-- TABLE: core.listing
-- =====================================================

CREATE TABLE IF NOT EXISTS core.listing (

    listing_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    scrape_source_id UUID,

    external_listing_id TEXT,

    listing_url TEXT,

    title TEXT,

    description TEXT,

    rent_amount NUMERIC(12,2) NOT NULL,

    deposit_amount NUMERIC(12,2),

    maintenance_amount NUMERIC(12,2),

    available_from DATE,

    listing_status VARCHAR(30) NOT NULL DEFAULT 'active',

    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_listing_rent
        CHECK (rent_amount > 0),

    CONSTRAINT chk_listing_deposit
        CHECK (
            deposit_amount IS NULL
            OR deposit_amount >= 0
        )

);
-- core.amenity

-- =====================================================
-- TABLE: core.amenity
-- =====================================================

CREATE TABLE IF NOT EXISTS core.amenity (

    amenity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    locality_id UUID NOT NULL
        REFERENCES core.locality(locality_id)
        ON DELETE CASCADE,

    osm_type VARCHAR(20),

    osm_id BIGINT,

    amenity_type VARCHAR(50) NOT NULL,

    name TEXT,

    address TEXT,

    latitude NUMERIC(9,6),

    longitude NUMERIC(9,6),

    geometry GEOMETRY(POINT,4326) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_osm UNIQUE(osm_type, osm_id)

);
-- core.price_history

-- =====================================================
-- TABLE: core.price_history
-- =====================================================

CREATE TABLE IF NOT EXISTS core.price_history (

    price_history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    listing_id UUID NOT NULL
        REFERENCES core.listing(listing_id)
        ON DELETE CASCADE,

    rent_amount NUMERIC(12,2) NOT NULL,

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_price_positive
        CHECK (rent_amount > 0)

);


-- core.availability_history

-- =====================================================
-- TABLE: core.availability_history
-- =====================================================

CREATE TABLE IF NOT EXISTS core.availability_history (

    availability_history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    listing_id UUID NOT NULL
        REFERENCES core.listing(listing_id)
        ON DELETE CASCADE,

    availability_status VARCHAR(30) NOT NULL,

    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
-- core.image

-- =====================================================
-- TABLE: core.image
-- =====================================================

CREATE TABLE IF NOT EXISTS core.image (

    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    image_url TEXT NOT NULL,

    image_source VARCHAR(100),

    image_type VARCHAR(30) DEFAULT 'photo',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
-- core.image_analysis

-- =====================================================
-- TABLE: core.image_analysis
-- =====================================================

CREATE TABLE IF NOT EXISTS core.image_analysis (

    image_analysis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    image_id UUID NOT NULL
        REFERENCES core.image(image_id)
        ON DELETE CASCADE,

    model_name VARCHAR(100),

    model_version VARCHAR(50),

    room_type VARCHAR(50),

    image_quality_score NUMERIC(5,2),

    duplicate_score NUMERIC(5,2),

    furnishing_detected BOOLEAN,

    greenery_score NUMERIC(5,2),

    detected_labels JSONB DEFAULT '[]'::JSONB,

    analyzed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
