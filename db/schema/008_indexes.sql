-- =====================================================
-- NIVAAS
-- Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_property_geometry
ON core.property
USING GIST(geometry);

CREATE INDEX IF NOT EXISTS idx_locality_boundary
ON core.locality
USING GIST(boundary);

CREATE INDEX IF NOT EXISTS idx_locality_centroid
ON core.locality
USING GIST(centroid);

CREATE INDEX IF NOT EXISTS idx_amenity_geometry
ON core.amenity
USING GIST(geometry);

CREATE INDEX IF NOT EXISTS idx_listing_property
ON core.listing(property_id);

CREATE INDEX IF NOT EXISTS idx_price_history_listing
ON core.price_history(listing_id);

CREATE INDEX IF NOT EXISTS idx_document_locality
ON rag.document(locality_id);

CREATE INDEX IF NOT EXISTS idx_chunk_document
ON rag.document_chunk(document_id);
