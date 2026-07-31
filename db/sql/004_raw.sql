-- ============================================================
-- NIVAAS
-- Raw Ingestion Layer
-- ============================================================

CREATE TABLE raw.raw_listing (
    raw_listing_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scrape_run_id UUID NOT NULL,
    raw_payload JSONB NOT NULL,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_raw_listing_scrape_run
        FOREIGN KEY (scrape_run_id)
        REFERENCES metadata.scrape_run(scrape_run_id)
);
