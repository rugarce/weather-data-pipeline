CREATE TABLE locations (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude NUMERIC(8,5) NOT NULL,
    longitude NUMERIC(8,5) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_locations_city_country
        UNIQUE (city, country)
);


CREATE TABLE raw_weather (
    id BIGSERIAL PRIMARY KEY,
    location_id BIGINT NOT NULL,
    retrieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload JSONB NOT NULL,

    CONSTRAINT fk_raw_weather_location
        FOREIGN KEY (location_id)
        REFERENCES locations(id)
);


CREATE TABLE weather_observations (
    id BIGSERIAL PRIMARY KEY,
    location_id BIGINT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_c NUMERIC(5,2),
    humidity_pct NUMERIC(5,2),
    precipitation_mm NUMERIC(7,2),
    wind_speed_kmh NUMERIC(7,2),
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_weather_observations_location
        FOREIGN KEY (location_id)
        REFERENCES locations(id),

    CONSTRAINT uq_weather_observation
        UNIQUE (location_id, observed_at)
);


CREATE INDEX idx_raw_weather_location_id
ON raw_weather (location_id);


CREATE INDEX idx_weather_observations_observed_at
ON weather_observations (observed_at);