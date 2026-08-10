CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.locality_mapping
(
    locality_id UUID PRIMARY KEY,

    locality_name TEXT,

    canonical_locality TEXT
);
