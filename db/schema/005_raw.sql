-- =====================================================
-- NIVAAS
-- Raw Layer
-- =====================================================

CREATE TABLE IF NOT EXISTS raw.raw_listing (

    raw_listing_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    scrape_run_id UUID NOT NULL
        REFERENCES metadata.scrape_run(scrape_run_id)
        ON DELETE CASCADE,

    external_listing_id TEXT,

    source_url TEXT,

    payload JSONB NOT NULL,

    scraped_at TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
