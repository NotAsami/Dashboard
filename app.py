from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Dummy data for now
    weather = {
        "city": "London",
        "temp": 18,
        "description": "Partly cloudy"
    }

    news = [
        {"title": "Python 3.13 Released!", "url": "https://www.python.org"},
        {"title": "Flask Framework Growing Strong", "url": "https://flask.palletsprojects.com"},
        {"title": "APIs Make Life Easier", "url": "https://example.com"}
    ]

    return render_template("index.html", weather=weather, news=news)


if __name__ == "__main__":
    app.run(debug=True)