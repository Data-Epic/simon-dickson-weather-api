from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WeatherData:
    city_name: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float
    timestamp: Optional[datetime] = None

"""This is a data class that represents weather information for a specific city at a given time.

    This class uses the `@dataclass` decorator to automatically generate an initializer,
    string representation, and equality comparison methods. It structures weather data
    fetched from the OpenWeatherMap API, as processed by the WeatherAPIService class.

    Attributes:
        city_name (str): The name of the city (e.g., "London", "New York").
        temperature (float): The temperature in Celsius, typically rounded to one decimal place.
        condition (str): A brief description of the weather (e.g., "clear sky", "light rain").
        humidity (int): The relative humidity as a percentage (e.g., 80 for 80%).
        wind_speed (float): The wind speed in meters per second (m/s).
        timestamp (Optional[datetime]): The time the weather data was recorded, in UTC,
                                       or None if not available. Defaults to None.
    """