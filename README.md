# Weather Client Application

A Python application that fetches and displays weather data for multiple cities using the OpenWeatherMap API.

## Setup

1. **Obtain an API Key**:
   - Register at [OpenWeatherMap](https://openweathermap.org/api) to get a free API key.
   - Replace `WEATHER_API_KEY` in `src/weather_client.py` with your actual API key.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python src/weather_client.py
   ```

## Usage
   - Enter city names separated by commas (e.g., London, Paris, Tokyo).
   - Type quit to exit.
   - The application displays current weather and a 5-day forecast for each city.

## Running Unit tests using Pytest
   - Open the directory
   - Run 
   ```bash
   PYTHONPATH=src pytest tests/
   ```# simon-dickson-weather-api
