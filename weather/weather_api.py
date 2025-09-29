import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Base URL for the OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    """
    Fetch weather data for a given city from the OpenWeatherMap API.

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
    # Define query parameters for the API request
    params = {
        "q": city,  # The city name to query
        "appid": os.getenv("WEATHER_API_KEY"),  # API key for authentication
        "units": "metric"  # Use metric units (Celsius for temperature)
    }

    # Send a GET request to the OpenWeatherMap API
    response = requests.get(BASE_URL, params=params)

    # Check if the response status code indicates an error
    if response.status_code != 200:
        raise Exception(f"Error fetching weather: {response.text}")  # Raise an exception with the error message

    # Parse the JSON response from the API
    data = response.json()

    # Extract and structure the relevant weather data
    weather = {
        "city": data["name"],  # The name of the city
        "temp": data["main"]["temp"],  # The current temperature in Celsius
        "description": data["weather"][0]["description"].capitalize(),  # Capitalized weather description
    }

    return weather  # Return the structured weather data
