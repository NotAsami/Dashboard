import os
import praw
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize a Reddit instance using credentials from environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),  # Reddit API client ID
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),  # Reddit API client secret
    user_agent="WeatherNewsDashboard:v1.0 (by u/PlateNational8253)"  # User agent for the Reddit API
)

def get_headlines(subreddit="worldnews", limit=5):
    """Fetch top headlines + image if available."""
    headlines = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        image_url = None

        # If it's a direct image
        if submission.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            image_url = submission.url

        # Or if Reddit generated a preview
        elif hasattr(submission, "preview"):
            images = submission.preview.get("images")
            if images:
                image_url = images[0]["source"]["url"]

        # Or fallback to thumbnail (if it's a valid URL)
        elif submission.thumbnail and submission.thumbnail.startswith("http"):
            image_url = submission.thumbnail

        headlines.append({
            "title": submission.title,
            "url": submission.url,
            "image": image_url
        })

    return headlines
