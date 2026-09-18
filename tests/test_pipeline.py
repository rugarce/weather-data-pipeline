import pytest

from src.pipeline import transform_weather, validate_observations


def test_transform_weather():
    data = {
        "hourly": {
            "time": ["2026-09-17T00:00", "2026-09-17T01:00"],
            "temperature_2m": [18.3, 17.8],
            "relative_humidity_2m": [47, 50],
            "precipitation": [0.0, 0.2],
            "wind_speed_10m": [18.4, 20.1],
        }
    }

    observations = transform_weather(data)

    assert len(observations) == 2
    assert observations[0]["temperature_c"] == 18.3
    assert observations[1]["humidity_pct"] == 50


def test_validate_observations_valid():
    observations = [
        {
            "observed_at": "2026-09-17T00:00",
            "temperature_c": 18.3,
            "humidity_pct": 47,
            "precipitation_mm": 0.0,
            "wind_speed_kmh": 18.4,
        }
    ]

    validate_observations(observations)


def test_validate_observations_invalid_humidity():
    observations = [
        {
            "observed_at": "2026-09-17T00:00",
            "temperature_c": 18.3,
            "humidity_pct": 120,
            "precipitation_mm": 0.0,
            "wind_speed_kmh": 18.4,
        }
    ]

    with pytest.raises(ValueError):
        validate_observations(observations)


def test_validate_observations_invalid_temperature():
    observations = [
        {
            "observed_at": "2026-09-17T00:00",
            "temperature_c": 100,
            "humidity_pct": 50,
            "precipitation_mm": 0,
            "wind_speed_kmh": 10,
        }
    ]

    with pytest.raises(ValueError):
        validate_observations(observations)


def test_validate_observations_invalid_wind():
    observations = [
        {
            "observed_at": "2026-09-17T00:00",
            "temperature_c": 20,
            "humidity_pct": 50,
            "precipitation_mm": 0,
            "wind_speed_kmh": -5,
        }
    ]

    with pytest.raises(ValueError):
        validate_observations(observations)