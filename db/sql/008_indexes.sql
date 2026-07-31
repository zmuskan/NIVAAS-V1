-- ============================================================
-- NIVAAS
-- Database Indexes
-- ============================================================

-- ------------------------------------------------------------
-- Metadata
-- ------------------------------------------------------------

CREATE INDEX idx_scrape_source_active
    ON metadata.scrape_source(active);

CREATE INDEX idx_scrape_run_source
    ON metadata.scrape_run(scrape_source_id);

CREATE INDEX idx_scrape_run_status
    ON metadata.scrape_run(status);

CREATE INDEX idx_scrape_run_started_at
    ON metadata.scrape_run(started_at);

CREATE INDEX idx_pipeline_run_name
    ON metadata.pipeline_run(pipeline_name);

CREATE INDEX idx_pipeline_run_status
    ON metadata.pipeline_run(status);

CREATE INDEX idx_pipeline_run_started_at
    ON metadata.pipeline_run(started_at);

CREATE INDEX idx_data_source_type
    ON metadata.data_source(source_type);


-- ------------------------------------------------------------
-- Core Domain
-- ------------------------------------------------------------

CREATE INDEX idx_locality_geometry
    ON core.locality
    USING GIST (geometry);

CREATE INDEX idx_property_locality
    ON core.property(locality_id);

CREATE INDEX idx_property_type
    ON core.property(property_type);

CREATE INDEX idx_property_geometry
    ON core.property
    USING GIST (geometry);

CREATE INDEX idx_listing_property
    ON core.listing(property_id);

CREATE INDEX idx_listing_source
    ON core.listing(scrape_source_id);

CREATE INDEX idx_listing_status
    ON core.listing(listing_status);

CREATE INDEX idx_listing_rent
    ON core.listing(rent);

CREATE INDEX idx_listing_last_seen
    ON core.listing(last_seen);

CREATE INDEX idx_amenity_locality
    ON core.amenity(locality_id);

CREATE INDEX idx_amenity_type
    ON core.amenity(amenity_type);

CREATE INDEX idx_amenity_geometry
    ON core.amenity
    USING GIST (geometry);

CREATE INDEX idx_amenity_osm_id
    ON core.amenity(osm_id)
    WHERE osm_id IS NOT NULL;

CREATE INDEX idx_image_property
    ON core.image(property_id);

CREATE INDEX idx_image_hash
    ON core.image(image_hash)
    WHERE image_hash IS NOT NULL;


-- ------------------------------------------------------------
-- Historical Data
-- ------------------------------------------------------------

CREATE INDEX idx_price_history_listing_time
    ON core.price_history(listing_id, recorded_at);

CREATE INDEX idx_price_history_recorded_at
    ON core.price_history(recorded_at);

CREATE INDEX idx_availability_history_listing_time
    ON core.availability_history(listing_id, recorded_at);

CREATE INDEX idx_availability_history_status
    ON core.availability_history(status);

CREATE INDEX idx_availability_history_recorded_at
    ON core.availability_history(recorded_at);


-- ------------------------------------------------------------
-- Raw Ingestion
-- ------------------------------------------------------------

CREATE INDEX idx_raw_listing_scrape_run
    ON raw.raw_listing(scrape_run_id);

CREATE INDEX idx_raw_listing_processed
    ON raw.raw_listing(processed);

CREATE INDEX idx_raw_listing_scraped_at
    ON raw.raw_listing(scraped_at);


-- ------------------------------------------------------------
-- RAG
-- ------------------------------------------------------------

CREATE INDEX idx_document_type
    ON rag.document(document_type);

CREATE INDEX idx_document_chunk_document
    ON rag.document_chunk(document_id);


-- ------------------------------------------------------------
-- Feature Store
-- ------------------------------------------------------------

CREATE INDEX idx_feature_property
    ON feature_store.feature(property_id);

CREATE INDEX idx_feature_name
    ON feature_store.feature(feature_name);

CREATE INDEX idx_feature_property_name
    ON feature_store.feature(property_id, feature_name);

CREATE INDEX idx_feature_created_at
    ON feature_store.feature(created_at);


-- ------------------------------------------------------------
-- Analytics / ML
-- ------------------------------------------------------------

CREATE INDEX idx_prediction_property
    ON analytics.prediction(property_id);

CREATE INDEX idx_prediction_model
    ON analytics.prediction(model_name);

CREATE INDEX idx_prediction_type
    ON analytics.prediction(prediction_type);

CREATE INDEX idx_prediction_property_type_time
    ON analytics.prediction(
        property_id,
        prediction_type,
        predicted_at
    );

CREATE INDEX idx_image_analysis_image
    ON analytics.image_analysis(image_id);

CREATE INDEX idx_image_analysis_model
    ON analytics.image_analysis(model_name);

CREATE INDEX idx_image_analysis_timestamp
    ON analytics.image_analysis(analysis_timestamp);
