CREATE SCHEMA IF NOT EXISTS feature_store;

CREATE TABLE IF NOT EXISTS feature_store.locality_feature (

    locality_id UUID NOT NULL,

    feature_name VARCHAR(100) NOT NULL,

    feature_value DOUBLE PRECISION NOT NULL,

    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_locality_feature
        PRIMARY KEY (
            locality_id,
            feature_name
        ),

    CONSTRAINT fk_locality_feature_locality
        FOREIGN KEY (locality_id)
        REFERENCES core.locality(locality_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_locality_feature_locality
ON feature_store.locality_feature(locality_id);

CREATE INDEX IF NOT EXISTS idx_locality_feature_name
ON feature_store.locality_feature(feature_name);
