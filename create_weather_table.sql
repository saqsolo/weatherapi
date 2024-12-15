CREATE TABLE weather_data (
    -- Location details
    city VARCHAR(100),
    region VARCHAR(200),
    country VARCHAR(100),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    timezone VARCHAR(50),
    local_time TIMESTAMP,
    
    -- Current weather details
    timestamp TIMESTAMP,
    last_updated TIMESTAMP,
    temperature_c DECIMAL(5, 2),
    temperature_f DECIMAL(5, 2),
    is_day SMALLINT,
    condition VARCHAR(100),
    condition_icon VARCHAR(200),
    condition_code INTEGER,
    
    -- Wind information
    wind_mph DECIMAL(5, 2),
    wind_kph DECIMAL(5, 2),
    wind_degree INTEGER,
    wind_dir VARCHAR(5),
    gust_mph DECIMAL(5, 2),
    gust_kph DECIMAL(5, 2),
    
    -- Atmospheric conditions
    pressure_mb DECIMAL(7, 2),
    pressure_in DECIMAL(5, 2),
    precip_mm DECIMAL(5, 2),
    precip_in DECIMAL(5, 2),
    humidity INTEGER,
    cloud INTEGER,
    
    -- Comfort metrics
    feels_like_c DECIMAL(5, 2),
    feels_like_f DECIMAL(5, 2),
    windchill_c DECIMAL(5, 2),
    windchill_f DECIMAL(5, 2),
    heatindex_c DECIMAL(5, 2),
    heatindex_f DECIMAL(5, 2),
    
    -- Visibility and other metrics
    dewpoint_c DECIMAL(5, 2),
    dewpoint_f DECIMAL(5, 2),
    vis_km DECIMAL(5, 2),
    vis_miles DECIMAL(5, 2),
    uv DECIMAL(4, 1)
);

-- Create indexes for common query patterns
CREATE INDEX idx_weather_city ON weather_data(city);
CREATE INDEX idx_weather_timestamp ON weather_data(timestamp);
CREATE INDEX idx_weather_location ON weather_data(city, country); 