import pytest
import requests

from src.api_client import get_weather


def test_get_weather_success(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"hourly": {"time": []}}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    city = {
        "city": "Madrid",
        "latitude": 40.4168,
        "longitude": -3.7038,
    }

    result = get_weather(city)

    assert result == {"hourly": {"time": []}}


def test_get_weather_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr(requests, "get", mock_get)

    city = {
        "city": "Madrid",
        "latitude": 40.4168,
        "longitude": -3.7038,
    }

    with pytest.raises(RuntimeError, match="Timeout"):
        get_weather(city)