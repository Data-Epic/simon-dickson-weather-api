import os
from dotenv import load_dotenv
from typing import List
from api_service import WeatherAPIService, WeatherAPIError
from models import WeatherData

class WeatherClient:
    """This is a client class for interacting with weather data and displaying it to the user.

    This class uses WeatherAPIService to fetch weather data from the OpenWeatherMap API
    and provides methods to display current weather and forecasts in a user-friendly format.
    It serves as the main interface for a command-line weather application.

    Attributes:
        api_service (WeatherAPIService): An instance of WeatherAPIService used to fetch weather data.
    """

    def __init__(self, api_key: str):
        """Initialize the WeatherClient with an API key.

        Args:
            api_key (str): The API key for accessing the OpenWeatherMap API, loaded from an environment variable.
        """
        self.api_service = WeatherAPIService(api_key)

    def display_weather(self, weather: WeatherData) -> None:
        """Display current weather data for a city in a formatted manner.

        Prints the weather details (city name, temperature, condition, humidity, wind speed,
        and timestamp) to the console. The timestamp, if present, is formatted in UTC.

        Args:
            weather (WeatherData): A WeatherData object containing the current weather information.

        Returns:
            None: This method only prints to the console and does not return a value.
        """
        print(f"\nWeather for {weather.city_name}:")
        print(f"Temperature: {weather.temperature}°C")
        print(f"Condition: {weather.condition}")
        print(f"Humidity: {weather.humidity}%")
        print(f"Wind Speed: {weather.wind_speed} m/s")
        if weather.timestamp:
            print(f"Time: {weather.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC")  # Updated to UTC

    def display_forecast(self, forecast: List[WeatherData]) -> None:
        """Display a 5-day weather forecast for a city, with 3-hour intervals.

        Prints a header with the city name followed by the weather details for each
        3-hour forecast interval over 5 days, separated by dashed lines.

        Args:
            forecast (List[WeatherData]): A list of WeatherData objects representing the forecast.

        Returns:
            None: This method only prints to the console and does not return a value.
        """
        print(f"\n5-Day Forecast for {forecast[0].city_name}:")
        for weather in forecast:
            print("-" * 40)
            self.display_weather(weather)

    def get_weather_for_cities(self) -> None:
        """Interact with the user to fetch and display weather data for multiple cities.

        Prompts the user to enter city names (comma-separated) or "quit" to exit.
        For each valid city, it fetches and displays the current weather and 5-day forecast.
        Handles errors gracefully, including city not found, API errors, and user interrupts.

        Returns:
            None: This method runs an interactive loop and prints to the console.

        """
        print("Enter city names (separated by commas) or 'quit' to exit.")
        while True:
            try:
                user_input = input("Cities: ").strip()
                if user_input.lower() == "quit":
                    print("Exiting...")
                    break

                cities = [city.strip() for city in user_input.split(",")]

                for city in cities:
                    if not city:
                        continue  # Skip empty city names

                    print(f"\nFetching weather for {city}...")
                    # Fetch and display current weather
                    current_weather = self.api_service.fetch_current_weather(city)
                    if current_weather:
                        self.display_weather(current_weather)
                    else:
                        print(f"City '{city}' not found.")

                    # Fetch and display forecast
                    forecast = self.api_service.fetch_forecast(city)
                    if forecast:
                        self.display_forecast(forecast)
                    else:
                        print(f"No forecast available for '{city}'.")

            except WeatherAPIError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

def main():
    """Entry point for the weather client application.

    Loads the API key from the environment (optionally from a .env file),
    initializes the WeatherClient, and starts the interactive weather retrieval loop.
    """
    load_dotenv()  # Load environment variables from .env file
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        raise ValueError("Please set the WEATHER_API_KEY environment variable or include it in a .env file.")
    client = WeatherClient(API_KEY)
    client.get_weather_for_cities()

if __name__ == "__main__":
    """Run the main function if this script is executed directly."""
    main()