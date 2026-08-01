
-- =====================================================
-- NIVAAS
-- Metadata Tables
-- =====================================================

CREATE TABLE IF NOT EXISTS metadata.scrape_source (

    scrape_source_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_name VARCHAR(100) NOT NULL UNIQUE,

    source_type VARCHAR(50) NOT NULL,

    base_url TEXT,

    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);

CREATE TABLE IF NOT EXISTS metadata.scrape_run (

    scrape_run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    scrape_source_id UUID NOT NULL
        REFERENCES metadata.scrape_source(scrape_source_id)
        ON DELETE RESTRICT,

    started_at TIMESTAMPTZ NOT NULL,

    completed_at TIMESTAMPTZ,

    status VARCHAR(20) NOT NULL,

    records_scraped INTEGER DEFAULT 0,

    records_inserted INTEGER DEFAULT 0,

    records_failed INTEGER DEFAULT 0,

    error_message TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

);
