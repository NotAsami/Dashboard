import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    """Fetch weather data for a given city from OpenWeatherMap."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Error fetching weather: {response.text}")

    data = response.json()

    weather = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"].capitalize(),
    }

    return weather
