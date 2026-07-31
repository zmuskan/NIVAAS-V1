-- ============================================================
-- NIVAAS
-- Metadata Layer
-- ============================================================

-- ------------------------------------------------------------
-- Scrape Sources
-- ------------------------------------------------------------

CREATE TABLE metadata.scrape_source (
    scrape_source_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    website TEXT,
    base_url TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- Scrape Runs
-- ------------------------------------------------------------

CREATE TABLE metadata.scrape_run (
    scrape_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scrape_source_id UUID NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL,
    listings_found INTEGER,
    duration_seconds NUMERIC(12,3),

    CONSTRAINT fk_scrape_run_source
        FOREIGN KEY (scrape_source_id)
        REFERENCES metadata.scrape_source(scrape_source_id),

    CONSTRAINT chk_scrape_run_completed_at
        CHECK (
            completed_at IS NULL
            OR completed_at >= started_at
        ),

    CONSTRAINT chk_scrape_run_listings_found
        CHECK (
            listings_found IS NULL
            OR listings_found >= 0
        ),

    CONSTRAINT chk_scrape_run_duration
        CHECK (
            duration_seconds IS NULL
            OR duration_seconds >= 0
        )
);

-- ------------------------------------------------------------
-- Pipeline Runs
-- ------------------------------------------------------------

CREATE TABLE metadata.pipeline_run (
    pipeline_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_name VARCHAR(150) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL,
    duration_seconds NUMERIC(12,3),

    CONSTRAINT chk_pipeline_run_completed_at
        CHECK (
            completed_at IS NULL
            OR completed_at >= started_at
        ),

    CONSTRAINT chk_pipeline_run_duration
        CHECK (
            duration_seconds IS NULL
            OR duration_seconds >= 0
        )
);

-- ------------------------------------------------------------
-- Data Sources
-- ------------------------------------------------------------

CREATE TABLE metadata.data_source (
    data_source_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name VARCHAR(150) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL,
    api_endpoint TEXT,
    license VARCHAR(200),
    refresh_frequency VARCHAR(50)
);
