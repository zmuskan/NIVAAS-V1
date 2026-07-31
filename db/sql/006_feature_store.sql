-- ============================================================
-- NIVAAS
-- Feature Store Layer
-- ============================================================

CREATE TABLE feature_store.feature (
    feature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    feature_name VARCHAR(150) NOT NULL,
    feature_value DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_feature_property
        FOREIGN KEY (property_id)
        REFERENCES core.property(property_id)
);
