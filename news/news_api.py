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
    headlines = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        if submission.stickied:
            continue  # skip pinned posts if you want

        image_url = None

        # Case 1: Direct link to an image
        if submission.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            image_url = submission.url

        # Case 2: Gallery posts → just take the first image (ignore resolutions)
        elif hasattr(submission, "media_metadata") and submission.media_metadata:
            media_id, media_data = next(iter(submission.media_metadata.items()))
            if "s" in media_data:
                image_url = media_data["s"]["u"]   # just use "s" (usually full-size)
            elif "p" in media_data and media_data["p"]:
                image_url = media_data["p"][0]["u"]  # fallback: first preview size

        # Case 3: Preview images (non-gallery)
        elif hasattr(submission, "preview"):
            images = submission.preview.get("images")
            if images:
                image_url = images[0]["source"]["url"]

        # Case 4: fallback thumbnail
        if not image_url and submission.thumbnail and submission.thumbnail.startswith("http"):
            image_url = submission.thumbnail

        headlines.append({
            "title": submission.title,
            "url": submission.url,
            "image": image_url
        })

    return headlines
