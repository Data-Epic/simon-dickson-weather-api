import pytest
import requests
from unittest.mock import Mock, patch
from src.api_service import WeatherAPIService, WeatherAPIError
from models import WeatherData
import os
from dotenv import load_dotenv

# Load environment variables from .env file at module startup
load_dotenv()

# --- Fixtures ---

@pytest.fixture
def weather_service():
    """Provide a WeatherAPIService instance for testing.

    This fixture initializes a WeatherAPIService object using an API key loaded from
    the environment variable

    Returns:
        WeatherAPIService: An instance of WeatherAPIService configured with the API key.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY not found in environment or .env file")
    return WeatherAPIService(api_key=api_key)

# --- Tests for fetch_current_weather ---

def test_fetch_current_weather_success(weather_service):
    """Test fetch_current_weather with a successful API response.

    Verifies that fetch_current_weather correctly processes a valid API response,
    returning a WeatherData object with the expected attributes for the city "London".
    Mocks the HTTP request to avoid real API calls.

    Args:
        weather_service (WeatherAPIService): The WeatherAPIService instance from the fixture.
    """
    mock_response = {
        "name": "London",
        "main": {"temp": 283.15, "humidity": 80},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 5.0},
        "dt": 1635778800  # Unix timestamp for 2021-11-01 15:00:00 UTC
    }
    with patch("requests.get") as mock_get:
        # Configure the mock to return a successful response
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        result = weather_service.fetch_current_weather("London")

        # Assertions to verify the returned WeatherData object
        assert isinstance(result, WeatherData), "Result should be a WeatherData instance"
        assert result.city_name == "London", "City name should match input"
        assert result.temperature == pytest.approx(10.0, 0.1), "Temperature should be ~10°C (from 283.15K)"
        assert result.condition == "clear sky", "Condition should match API response"
        assert result.humidity == 80, "Humidity should match API response"
        assert result.wind_speed == 5.0, "Wind speed should match API response"

def test_fetch_current_weather_city_not_found(weather_service):
    """Test fetch_current_weather when the city is not found (404 error).

    Ensures that fetch_current_weather returns None when the API returns a 404 status,
    indicating the city doesn’t exist. Uses mocking to simulate the API response.

    Args:
        weather_service (WeatherAPIService): The WeatherAPIService instance from the fixture.
    """
    with patch("requests.get") as mock_get:
        # Configure the mock to simulate a 404 error
        mock_response = Mock(status_code=404)
        mock_response.json.return_value = {"message": "city not found"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        result = weather_service.fetch_current_weather("InvalidCity")

        assert result is None, "Result should be None for a 404 error"

def test_fetch_current_weather_http_error(weather_service):
    """Test fetch_current_weather with a server error (500 status).

    Verifies that fetch_current_weather raises a WeatherAPIError when the API returns
    a 500 status code, indicating a server-side issue. Then, this uses mocking to simulate the error.

    Args:
        weather_service (WeatherAPIService): The WeatherAPIService instance from the fixture.
    """
    with patch("requests.get") as mock_get:
        # Configure the mock to simulate a 500 error
        mock_response = Mock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(WeatherAPIError):
            weather_service.fetch_current_weather("London")

# --- Tests for fetch_forecast ---

def test_fetch_forecast_success(weather_service):
    """Test fetch_forecast with a successful API response.

    Ensures that fetch_forecast correctly processes a valid forecast response,
    returning a list of WeatherData objects. Tests only the first item for simplicity.
    Mocks the HTTP request to avoid real API calls.

    Args:
        weather_service (WeatherAPIService): The WeatherAPIService instance from the fixture.
    """
    mock_response = {
        "city": {"name": "London"},
        "list": [
            {
                "main": {"temp": 283.15, "humidity": 80},
                "weather": [{"description": "clear sky"}],
                "wind": {"speed": 5.0},
                "dt": 1635778800  # Unix timestamp for 2021-11-01 15:00:00 UTC
            }
        ]
    }
    with patch("requests.get") as mock_get:
        # Configure the mock to return a successful response
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response

        result = weather_service.fetch_forecast("London")

        # Assertions to verify the returned forecast list
        assert len(result) == 1, "Forecast list should contain one item"
        assert isinstance(result[0], WeatherData), "First item should be a WeatherData instance"
        assert result[0].city_name == "London", "City name should match input"
        assert result[0].temperature == pytest.approx(10.0, 0.1), "Temperature should be ~10°C (from 283.15K)"