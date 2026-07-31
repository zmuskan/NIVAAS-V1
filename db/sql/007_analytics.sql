-- ============================================================
-- NIVAAS
-- Analytics / ML / CV Layer
-- ============================================================

CREATE TABLE analytics.prediction (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    prediction_type VARCHAR(100) NOT NULL,
    prediction_value DOUBLE PRECISION NOT NULL,
    confidence_score NUMERIC(5,4),
    predicted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_prediction_property
        FOREIGN KEY (property_id)
        REFERENCES core.property(property_id),

    CONSTRAINT chk_prediction_confidence
        CHECK (
            confidence_score IS NULL
            OR confidence_score BETWEEN 0 AND 1
        )
);


CREATE TABLE analytics.image_analysis (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_id UUID NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    objects_detected JSONB,
    cleanliness_score NUMERIC(5,4),
    furnishing_score NUMERIC(5,4),
    quality_score NUMERIC(5,4),
    analysis_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_image_analysis_image
        FOREIGN KEY (image_id)
        REFERENCES core.image(image_id),

    CONSTRAINT chk_image_analysis_cleanliness
        CHECK (
            cleanliness_score IS NULL
            OR cleanliness_score BETWEEN 0 AND 1
        ),

    CONSTRAINT chk_image_analysis_furnishing
        CHECK (
            furnishing_score IS NULL
            OR furnishing_score BETWEEN 0 AND 1
        ),

    CONSTRAINT chk_image_analysis_quality
        CHECK (
            quality_score IS NULL
            OR quality_score BETWEEN 0 AND 1
        )
);
