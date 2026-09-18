import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m"
        ),
        "timezone": "Europe/Madrid",
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            f"Timeout requesting weather for {city['city']}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Error requesting weather for {city['city']}: {exc}"
        ) from exc

    return response.json()