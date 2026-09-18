from datetime import datetime, timezone
from src.api_client import get_weather
from src.config import CITIES
from src.database import (
    get_connection,
    get_or_create_location,
    save_raw_weather,
    save_observations,
)


def transform_weather(data: dict) -> list[dict]:
    hourly = data["hourly"]

    observations = []

    for i, timestamp in enumerate(hourly["time"]):
        observations.append(
            {
                "observed_at": datetime.fromisoformat(
                    timestamp
                ).replace(tzinfo=timezone.utc),
                "temperature_c": hourly["temperature_2m"][i],
                "humidity_pct": hourly["relative_humidity_2m"][i],
                "precipitation_mm": hourly["precipitation"][i],
                "wind_speed_kmh": hourly["wind_speed_10m"][i],
            }
        )

    return observations


def validate_observations(observations: list[dict]) -> None:
    for obs in observations:
        if obs["observed_at"] is None:
            raise ValueError("observed_at cannot be None")

        if not -80 <= obs["temperature_c"] <= 60:
            raise ValueError("Invalid temperature")

        if not 0 <= obs["humidity_pct"] <= 100:
            raise ValueError("Invalid humidity")

        if obs["precipitation_mm"] < 0:
            raise ValueError("Invalid precipitation")

        if obs["wind_speed_kmh"] < 0:
            raise ValueError("Invalid wind speed")


def run_pipeline() -> None:
    conn = get_connection()

    try:
        for city in CITIES:
            print(f"Processing {city['city']}...")

            data = get_weather(city)

            observations = transform_weather(data)

            validate_observations(observations)

            location_id = get_or_create_location(conn, city)
            save_raw_weather(conn, location_id, data)

            save_observations(
                conn,
                location_id,
                observations,
            )

            print(
                f"{city['city']}: "
                f"{len(observations)} observations processed"
            )

    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline()