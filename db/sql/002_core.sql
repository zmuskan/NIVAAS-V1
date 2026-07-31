-- ============================================================
-- NIVAAS
-- Core Domain Layer
-- ============================================================

-- ------------------------------------------------------------
-- Locality
-- ------------------------------------------------------------

CREATE TABLE core.locality (
    locality_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(80) NOT NULL,
    pincode VARCHAR(10),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geometry GEOMETRY(MULTIPOLYGON, 4326),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_locality_name_city_state
        UNIQUE (name, city, state),

    CONSTRAINT chk_locality_latitude
        CHECK (
            latitude IS NULL
            OR latitude BETWEEN -90 AND 90
        ),

    CONSTRAINT chk_locality_longitude
        CHECK (
            longitude IS NULL
            OR longitude BETWEEN -180 AND 180
        )
);

-- ------------------------------------------------------------
-- Property
-- ------------------------------------------------------------

CREATE TABLE core.property (
    property_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    locality_id UUID NOT NULL,
    property_name VARCHAR(200),
    address TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geometry GEOMETRY(POINT, 4326) NOT NULL,
    property_type VARCHAR(50) NOT NULL,
    bhk SMALLINT,
    furnishing VARCHAR(30),
    parking BOOLEAN,
    bathrooms SMALLINT,
    area_sqft NUMERIC(10,2),
    floor SMALLINT,
    total_floors SMALLINT,
    facing VARCHAR(20),
    age_of_property SMALLINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_property_locality
        FOREIGN KEY (locality_id)
        REFERENCES core.locality(locality_id),

    CONSTRAINT chk_property_latitude
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT chk_property_longitude
        CHECK (longitude BETWEEN -180 AND 180),

    CONSTRAINT chk_property_bhk
        CHECK (bhk IS NULL OR bhk > 0),

    CONSTRAINT chk_property_bathrooms
        CHECK (bathrooms IS NULL OR bathrooms >= 0),

    CONSTRAINT chk_property_area
        CHECK (area_sqft IS NULL OR area_sqft > 0),

    CONSTRAINT chk_property_floor
        CHECK (floor IS NULL OR floor >= 0),

    CONSTRAINT chk_property_total_floors
        CHECK (total_floors IS NULL OR total_floors >= 0),

    CONSTRAINT chk_property_age
        CHECK (
            age_of_property IS NULL
            OR age_of_property >= 0
        ),

    CONSTRAINT chk_property_floor_consistency
        CHECK (
            floor IS NULL
            OR total_floors IS NULL
            OR floor <= total_floors
        )
);

-- ------------------------------------------------------------
-- Listing
-- ------------------------------------------------------------

CREATE TABLE core.listing (
    listing_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    scrape_source_id UUID NOT NULL,
    external_listing_id VARCHAR(255) NOT NULL,
    listing_url TEXT NOT NULL,
    title VARCHAR(300),
    description TEXT,
    rent NUMERIC(12,2) NOT NULL,
    deposit NUMERIC(12,2),
    maintenance NUMERIC(12,2),
    available_from DATE,
    furnishing_status VARCHAR(30),
    listing_status VARCHAR(30) NOT NULL,
    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_listing_property
        FOREIGN KEY (property_id)
        REFERENCES core.property(property_id),

    CONSTRAINT fk_listing_scrape_source
        FOREIGN KEY (scrape_source_id)
        REFERENCES metadata.scrape_source(scrape_source_id),

    CONSTRAINT uq_listing_source_external_id
        UNIQUE (scrape_source_id, external_listing_id),

    CONSTRAINT chk_listing_rent
        CHECK (rent > 0),

    CONSTRAINT chk_listing_deposit
        CHECK (deposit IS NULL OR deposit >= 0),

    CONSTRAINT chk_listing_maintenance
        CHECK (maintenance IS NULL OR maintenance >= 0),

    CONSTRAINT chk_listing_seen_dates
        CHECK (last_seen >= first_seen)
);

-- ------------------------------------------------------------
-- Amenity
-- ------------------------------------------------------------

CREATE TABLE core.amenity (
    amenity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    locality_id UUID,
    name VARCHAR(255) NOT NULL,
    amenity_type VARCHAR(50) NOT NULL,
    address TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geometry GEOMETRY(POINT, 4326) NOT NULL,
    osm_id BIGINT,
    rating NUMERIC(3,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_amenity_locality
        FOREIGN KEY (locality_id)
        REFERENCES core.locality(locality_id),

    CONSTRAINT chk_amenity_latitude
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT chk_amenity_longitude
        CHECK (longitude BETWEEN -180 AND 180),

    CONSTRAINT chk_amenity_rating
        CHECK (
            rating IS NULL
            OR rating BETWEEN 0 AND 5
        )
);

-- ------------------------------------------------------------
-- Property Images
-- ------------------------------------------------------------

CREATE TABLE core.image (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    image_url TEXT NOT NULL,
    image_hash VARCHAR(128),
    source VARCHAR(100),
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_image_property
        FOREIGN KEY (property_id)
        REFERENCES core.property(property_id)
);
