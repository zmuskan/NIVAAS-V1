-- ============================================================
-- NIVAAS
-- Historical Data Layer
-- ============================================================

CREATE TABLE core.price_history (
    price_history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL,
    rent NUMERIC(12,2) NOT NULL,
    deposit NUMERIC(12,2),
    maintenance NUMERIC(12,2),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_price_history_listing
        FOREIGN KEY (listing_id)
        REFERENCES core.listing(listing_id),

    CONSTRAINT uq_price_history_observation
        UNIQUE (listing_id, recorded_at),

    CONSTRAINT chk_price_history_rent
        CHECK (rent > 0),

    CONSTRAINT chk_price_history_deposit
        CHECK (deposit IS NULL OR deposit >= 0),

    CONSTRAINT chk_price_history_maintenance
        CHECK (maintenance IS NULL OR maintenance >= 0)
);


CREATE TABLE core.availability_history (
    availability_history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL,
    status VARCHAR(30) NOT NULL,
    available_from DATE,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_availability_history_listing
        FOREIGN KEY (listing_id)
        REFERENCES core.listing(listing_id),

    CONSTRAINT uq_availability_history_observation
        UNIQUE (listing_id, recorded_at)
);
