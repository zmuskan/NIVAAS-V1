-- =====================================================
-- NIVAAS
-- Feature Store
-- =====================================================

CREATE TABLE IF NOT EXISTS feature_store.property_feature (

    feature_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    property_id UUID NOT NULL
        REFERENCES core.property(property_id)
        ON DELETE CASCADE,

    metro_distance_m DOUBLE PRECISION,

    bus_stop_distance_m DOUBLE PRECISION,

    hospitals_2km INTEGER,

    schools_2km INTEGER,

    restaurants_500m INTEGER,

    parks_2km INTEGER,

    supermarkets_1km INTEGER,

    gyms_1km INTEGER,

    rent_per_sqft NUMERIC(10,2),

    amenity_density NUMERIC(10,2),

    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
