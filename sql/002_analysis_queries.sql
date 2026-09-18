-- 1. Average temperature by city
SELECT
    l.city,
    ROUND(AVG(w.temperature_c), 2) AS avg_temperature_c
FROM weather_observations w
JOIN locations l
    ON l.id = w.location_id
GROUP BY l.city
ORDER BY avg_temperature_c DESC;


-- 2. Maximum temperature by city
SELECT
    l.city,
    MAX(w.temperature_c) AS max_temperature_c
FROM weather_observations w
JOIN locations l
    ON l.id = w.location_id
GROUP BY l.city
ORDER BY max_temperature_c DESC;


-- 3. Total precipitation by city
SELECT
    l.city,
    ROUND(SUM(w.precipitation_mm), 2) AS total_precipitation_mm
FROM weather_observations w
JOIN locations l
    ON l.id = w.location_id
GROUP BY l.city
ORDER BY total_precipitation_mm DESC;


-- 4. Average wind speed by city
SELECT
    l.city,
    ROUND(AVG(w.wind_speed_kmh), 2) AS avg_wind_speed_kmh
FROM weather_observations w
JOIN locations l
    ON l.id = w.location_id
GROUP BY l.city
ORDER BY avg_wind_speed_kmh DESC;


-- 5. Number of observations by city
SELECT
    l.city,
    COUNT(w.id) AS observation_count
FROM weather_observations w
JOIN locations l
    ON l.id = w.location_id
GROUP BY l.city
ORDER BY l.city;