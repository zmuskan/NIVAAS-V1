-- ===========================================================
-- 013_core_constraints.sql
-- Core pipeline constraints
-- ===========================================================

-- Property deduplication
ALTER TABLE core.property
ADD COLUMN IF NOT EXISTS property_hash CHAR(64);

CREATE UNIQUE INDEX IF NOT EXISTS uq_property_hash
ON core.property(property_hash);

-- Listing deduplication
CREATE UNIQUE INDEX IF NOT EXISTS uq_listing_source_external
ON core.listing(scrape_source_id, external_listing_id)
WHERE external_listing_id IS NOT NULL;
