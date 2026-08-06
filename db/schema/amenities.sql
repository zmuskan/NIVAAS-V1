CREATE TABLE IF NOT EXISTS core.metro_station (

    metro_station_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    osm_id BIGINT UNIQUE,

    name TEXT,

    latitude NUMERIC(9,6),

    longitude NUMERIC(9,6),

    geometry geometry(Point,4326),

    created_at TIMESTAMPTZ DEFAULT now()

);

CREATE INDEX IF NOT EXISTS idx_metro_geom
ON core.metro_station
USING GIST(geometry);
