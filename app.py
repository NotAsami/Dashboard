from flask import Flask, render_template
from weather.weather_api import get_weather
from news.news_api import get_headlines

app = Flask(__name__)

@app.route("/")
def home():
    # Change this to your city or load from config later
    weather = get_weather("Považská Bystrica, SK")
    news = get_headlines("cyberpunkgame", limit=5)  # you can change subreddit

    return render_template("index.html", weather=weather, news=news)


if __name__ == "__main__":
    app.run(debug=True)
