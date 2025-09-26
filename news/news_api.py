import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="WeatherNewsDashboard:v1.0 (by u/PlateNational8253)"
)

def get_headlines(subreddit="worldnews", limit=5):
    """Fetch top headlines from a subreddit."""
    headlines = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        headlines.append({
            "title": submission.title,
            "url": submission.url
        })
    return headlines
