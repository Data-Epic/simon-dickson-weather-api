import requests
from typing import List, Optional
from datetime import datetime, timezone
from models import WeatherData

class WeatherAPIError(Exception):
    """Custom exception raised for errors encountered while interacting with the OpenWeatherMap API.

    This exception is used to wrap HTTP errors (excluding 404) and network-related issues,
    providing a clear indication of API-specific problems.

    Attributes:
        message (str): A description of the error (e.g., "HTTP error occurred: 500 Server Error").
    """

class WeatherAPIService:
    """A service class to fetch weather data from the OpenWeatherMap API.

    This class provides methods to retrieve current weather and 5-day forecast data for a specified city.
    It handles API requests, converts data into a structured format, and manages errors gracefully.

    Attributes:
        api_key (str): The API key required for authenticating requests to OpenWeatherMap.
        base_url (str): The base URL for the OpenWeatherMap API (version 2.5).
    """

    def __init__(self, api_key: str):
        """Initialize the WeatherAPIService with an API key.

        Args:
            api_key (str): The API key obtained from OpenWeatherMap for accessing weather data.
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def _kelvin_to_celsius(self, kelvin: float) -> float:
        """Convert a temperature from Kelvin to Celsius.

        This is a private helper method used internally to transform the temperature
        values returned by the OpenWeatherMap API (in Kelvin) to Celsius.

        Args:
            kelvin (float): The temperature in Kelvin.

        Returns:
            float: The temperature in Celsius, calculated as Kelvin - 273.15.
        """
        return kelvin - 273.15

    def fetch_current_weather(self, city: str) -> Optional[WeatherData]:
        """Fetch the current weather data for a specified city.

        This method sends a request to the OpenWeatherMap API's /weather endpoint,
        retrieves the current weather data, and returns it as a WeatherData object.
        If the city is not found (HTTP 404), it returns None.

        Args:
            city (str): The name of the city for which to fetch weather data (e.g., "London").

        Returns:
            Optional[WeatherData]: A WeatherData object containing the current weather details,
                                  or None if the city is not found.

        Raises:
            WeatherAPIError: If an HTTP error (other than 404) or a network error occurs during the request.
        """
        url = f"{self.base_url}/weather?q={city}&appid={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises HTTPError for non-200 status codes
            data = response.json()

            return WeatherData(
                city_name=data["name"],
                temperature=round(self._kelvin_to_celsius(data["main"]["temp"]), 1),
                condition=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                timestamp=datetime.fromtimestamp(data["dt"], timezone.utc)
            )
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return None  # City not found
            raise WeatherAPIError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Error fetching weather data: {e}")

    def fetch_forecast(self, city: str) -> List[WeatherData]:
        """Fetch a 5-day weather forecast for a specified city, with 3-hour intervals.

        This method queries the OpenWeatherMap API's /forecast endpoint to retrieve
        weather data for the next 5 days, sampled every 3 hours. Each forecast point
        is returned as a WeatherData object in a list. If the city is not found (HTTP 404),
        an empty list is returned.

        Args:
            city (str): The name of the city for which to fetch the forecast (e.g., "London").

        Returns:
            List[WeatherData]: A list of WeatherData objects, each representing a 3-hour
                              forecast interval over 5 days, or an empty list if the city is not found.

        Raises:
            WeatherAPIError: If an HTTP error (other than 404) or a network error occurs during the request.
        """
        url = f"{self.base_url}/forecast?q={city}&appid={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises HTTPError for non-200 status codes
            data = response.json()

            forecast_list = []
            for item in data["list"]:
                forecast_list.append(WeatherData(
                    city_name=data["city"]["name"],
                    temperature=round(self._kelvin_to_celsius(item["main"]["temp"]), 1),
                    condition=item["weather"][0]["description"],
                    humidity=item["main"]["humidity"],
                    wind_speed=item["wind"]["speed"],
                    timestamp=datetime.fromtimestamp(item["dt"], timezone.utc)
                ))
            return forecast_list
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return []  # City not found
            raise WeatherAPIError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Error fetching forecast data: {e}")