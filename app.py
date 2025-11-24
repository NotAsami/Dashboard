"""
AJAX Auto-Refresh Implementation for Flask Weather & News Dashboard
====================================================================

This implementation provides smooth, non-intrusive updates without page refresh.
Users can continue interacting with the page while data updates in the background.
"""

from flask import Flask, render_template, jsonify
from flask_caching import Cache
from weather.weather_api import get_weather
from news.news_api import get_headlines
from datetime import datetime

app = Flask(__name__)

# Configure caching
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 600
cache = Cache(app)

# ============================================================================
# API ENDPOINTS FOR AJAX REQUESTS
# ============================================================================

@app.route("/api/weather")
def api_weather():
    """
    JSON endpoint for weather data.

    Returns weather data in JSON format for AJAX requests.
    Cached for 10 minutes to reduce API calls.
    """
    weather = get_cached_weather()

    if weather:
        return jsonify({
            "success": True,
            "data": {
                "city": weather.get("city", "Unknown"),
                "temp": weather.get("temp", 0),
                "description": weather.get("description", "No data"),
                "last_updated": datetime.now().strftime("%H:%M:%S")
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": "Unable to fetch weather data"
        }), 503

@app.route("/api/news")
@app.route("/api/news/<subreddit>")
@app.route("/api/news/<subreddit>/<int:limit>")
def api_news(subreddit="cyberpunkgame", limit=5):
    """
    JSON endpoint for news data.

    Parameters:
        subreddit: Reddit subreddit name
        limit: Number of posts to fetch

    Returns news posts in JSON format for AJAX requests.
    Cached for 5 minutes.
    """
    news = get_cached_news(subreddit, limit)

    if news:
        # Format news data for JSON response
        news_data = [{
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "image": article.get("image", None)
        } for article in news]

        return jsonify({
            "success": True,
            "data": news_data,
            "count": len(news_data),
            "last_updated": datetime.now().strftime("%H:%M:%S")
        })
    else:
        return jsonify({
            "success": False,
            "error": "Unable to fetch news data"
        }), 503

@app.route("/api/refresh-all")
def api_refresh_all():
    """
    Endpoint to refresh all data at once.

    Useful for manual refresh button.
    Returns both weather and news data.
    """
    weather = get_cached_weather()
    news = get_cached_news("cyberpunkgame", 5)

    return jsonify({
        "success": True,
        "weather": {
            "city": weather.get("city", "Unknown") if weather else None,
            "temp": weather.get("temp", 0) if weather else None,
            "description": weather.get("description", "No data") if weather else None
        },
        "news": [{
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "image": article.get("image", None)
        } for article in news] if news else [],
        "last_updated": datetime.now().strftime("%H:%M:%S")
    })

# ============================================================================
# CACHED DATA FUNCTIONS
# ============================================================================

@cache.memoize(timeout=600)
def get_cached_weather():
    """Fetch weather with 10-minute cache"""
    try:
        return get_weather("Považská Bystrica, SK")
    except Exception as e:
        print(f"Weather API error: {e}")
        return None

@cache.memoize(timeout=300)
def get_cached_news(subreddit, limit):
    """Fetch news with 5-minute cache"""
    try:
        return get_headlines(subreddit, limit)
    except Exception as e:
        print(f"Reddit API error: {e}")
        return None

# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route("/")
def home():
    """
    Home page with initial data.

    JavaScript will handle auto-refresh after page load.
    """
    weather = get_cached_weather()
    news = get_cached_news("cyberpunkgame", 5)

    return render_template("index.html", weather=weather, news=news)

@app.route("/news")
def news_page():
    """News page with initial data"""
    news = get_cached_news("cyberpunkgame", 10)
    return render_template("news.html", news=news)

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.route("/api/status")
def api_status():
    """
    Health check endpoint.

    Returns server status and last update times.
    """
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "cache_enabled": True
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
API ENDPOINTS SUMMARY:
======================

GET /api/weather          - Get current weather data
GET /api/news             - Get news (default: cyberpunkgame, limit=5)
GET /api/news/<subreddit> - Get news from specific subreddit
GET /api/news/<subreddit>/<limit> - Get specific number of posts
GET /api/refresh-all      - Get all data at once
GET /api/status           - Server health check

RESPONSE FORMAT:
================

Success Response:
{
    "success": true,
    "data": { ... },
    "last_updated": "14:30:25"
}

Error Response:
{
    "success": false,
    "error": "Error message"
}
"""