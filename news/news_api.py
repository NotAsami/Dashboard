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
    """
    Fetch top headlines from a specified subreddit, including an image URL if available.

    Args:
        subreddit (str): The name of the subreddit to fetch headlines from. Defaults to "worldnews".
        limit (int): The maximum number of headlines to fetch. Defaults to 5.

    Returns:
        list[dict]: A list of dictionaries, each containing the following keys:
            - "title" (str): The title of the Reddit post.
            - "url" (str): The URL of the Reddit post.
            - "image" (str or None): The URL of an associated image, if available.
    """
    headlines = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        image_url = None

        # Check if the submission URL is a direct image link
        if submission.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            image_url = submission.url

        # Check if Reddit generated a preview with images
        elif hasattr(submission, "preview"):
            images = submission.preview.get("images")
            if images:
                image_url = images[0]["source"]["url"]

        # Fallback to the thumbnail if it's a valid URL
        elif submission.thumbnail and submission.thumbnail.startswith("http"):
            image_url = submission.thumbnail

        # Append the headline data to the list
        headlines.append({
            "title": submission.title,
            "url": submission.url,
            "image": image_url
        })

    return headlines
