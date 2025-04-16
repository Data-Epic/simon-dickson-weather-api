import pytest
from src.weather_client import WeatherClient
from models import WeatherData
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file at module startup
load_dotenv()

# --- Fixtures ---

@pytest.fixture
def weather_client():
    """Provide a WeatherClient instance for testing.

    Then, initializes a WeatherClient object using an API key loaded from the environment variable

    Returns:
        WeatherClient: An instance of WeatherClient configured with the API key.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY not found in environment or .env file")
    return WeatherClient(api_key=api_key)

# --- Tests ---

def test_display_weather(capsys, weather_client):
    """Test the display_weather method with a sample WeatherData object.

    Verifies that display_weather correctly formats and prints weather details to the
    console, including city name, temperature, condition, humidity, wind speed, and
    timestamp in UTC. Uses the capsys fixture to capture and check console output.

    Args:
        capsys: Pytest fixture to capture console output (stdout/stderr).
        weather_client (WeatherClient): The WeatherClient instance from the fixture.
    """
    weather = WeatherData(
        city_name="London",
        temperature=10.0,
        condition="clear sky",
        humidity=80,
        wind_speed=5.0,
        timestamp=datetime(2023, 11, 1, 12, 0)
    )
    weather_client.display_weather(weather)
    captured = capsys.readouterr()
    assert "Weather for London" in captured.out, "City name should be displayed"
    assert "Temperature: 10.0°C" in captured.out, "Temperature should be in Celsius"
    assert "Condition: clear sky" in captured.out, "Weather condition should match input"
    assert "Humidity: 80%" in captured.out, "Humidity should be displayed as percentage"
    assert "Wind Speed: 5.0 m/s" in captured.out, "Wind speed should be in m/s"
    assert "Time: 2023-11-01 12:00:00 UTC" in captured.out, "Timestamp should be in UTC"

def test_display_forecast(capsys, weather_client):
    """Test the display_forecast method with a sample forecast list.

    Ensures that display_forecast prints a header with the city name and the weather
    details for each WeatherData object in the list. Checks only key parts of the output
    for simplicity, using capsys to capture console output.

    Args:
        capsys: Pytest fixture to capture console output (stdout/stderr).
        weather_client (WeatherClient): The WeatherClient instance from the fixture.
    """
    forecast = [
        WeatherData(
            city_name="London",
            temperature=10.0,
            condition="clear sky",
            humidity=80,
            wind_speed=5.0,
            timestamp=datetime(2023, 11, 1, 12, 0)
        )
    ]
    weather_client.display_forecast(forecast)
    captured = capsys.readouterr()
    assert "5-Day Forecast for London" in captured.out, "Forecast header should include city name"
    assert "Temperature: 10.0°C" in captured.out, "Temperature should appear in forecast output"