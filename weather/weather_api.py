import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # Base URL for the OpenWeatherMap API

def get_weather(city: str):
    """
    Fetch weather data for a given city from OpenWeatherMap.

    Args:
        city (str): The name of the city to fetch weather data for.

    Returns:
        dict: A dictionary containing the weather data, including:
            - city (str): The name of the city.
            - temp (float): The current temperature in Celsius.
            - description (str): A short description of the weather conditions.

    Raises:
        Exception: If the API request fails or returns a non-200 status code.
    """
    params = {
        "q": city,  # Query parameter for the city name
        "appid": os.getenv("WEATHER_API_KEY"),  # API key for authentication
        "units": "metric"  # Units for temperature (Celsius)
    }

    response = requests.get(BASE_URL, params=params)  # Send a GET request to the API

    if response.status_code != 200:
        # Raise an exception if the API response indicates an error
        raise Exception(f"Error fetching weather: {response.text}")

    data = response.json()  # Parse the JSON response

    # Extract relevant weather data from the API response
    weather = {
        "city": data["name"],  # City name
        "temp": data["main"]["temp"],  # Current temperature
        "description": data["weather"][0]["description"].capitalize(),  # Weather description (capitalized)
    }

    return weather  # Return the extracted weather data
