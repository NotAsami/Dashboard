from flask import Flask, render_template
from weather.weather_api import get_weather
from news.news_api import get_headlines

# Initialize the Flask application
app = Flask(__name__)

@app.route("/")
def home():
    """
    Handle the root route ("/") of the web application.

    Fetches weather data for a specified city and top headlines from a subreddit,
    then renders the "index.html" template with the fetched data.

    Returns:
        str: Rendered HTML content for the home page.
    """
    # Fetch weather data for the specified city
    weather = get_weather("Považská Bystrica, SK")  # Replace with your city or load dynamically

    # Fetch top headlines from the specified subreddit
    news = get_headlines("cyberpunkgame", limit=5)  # Replace with another subreddit if needed

    # Render the "index.html" template with the fetched weather and news data
    return render_template("index.html", weather=weather, news=news)

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
