import os

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb


load_dotenv()


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def get_or_create_location(conn, city: dict) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO locations (city, country, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city, country)
            DO NOTHING
            RETURNING id;
            """,
            (
                city["city"],
                city["country"],
                city["latitude"],
                city["longitude"],
            ),
        )

        row = cur.fetchone()

        if row is None:
            cur.execute(
                """
                SELECT id
                FROM locations
                WHERE city = %s AND country = %s;
                """,
                (city["city"], city["country"]),
            )
            row = cur.fetchone()

    conn.commit()

    return row[0]

def save_raw_weather(conn, location_id: int, payload: dict) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw_weather (location_id, payload)
            VALUES (%s, %s);
            """,
            (location_id, Jsonb(payload)),
        )

    conn.commit()

def save_observations(
    conn,
    location_id: int,
    observations: list[dict],
) -> None:
    with conn.cursor() as cur:
        for obs in observations:
            cur.execute(
                """
                INSERT INTO weather_observations (
                    location_id,
                    observed_at,
                    temperature_c,
                    humidity_pct,
                    precipitation_mm,
                    wind_speed_kmh
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (location_id, observed_at)
                DO NOTHING;
                """,
                (
                    location_id,
                    obs["observed_at"],
                    obs["temperature_c"],
                    obs["humidity_pct"],
                    obs["precipitation_mm"],
                    obs["wind_speed_kmh"],
                ),
            )

    conn.commit()