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
    Fetches the top headlines from a specified subreddit.

    Args:
        subreddit (str): The name of the subreddit to fetch headlines from. Defaults to "worldnews".
        limit (int): The maximum number of posts to retrieve. Defaults to 5.

    Returns:
        list: A list of dictionaries, each containing the title, URL, and an optional image URL of a post.

    The function retrieves posts from the specified subreddit, skipping stickied posts. It attempts to extract an
    image URL from the post, prioritizing direct image links, gallery posts, preview images, and finally thumbnails.
    """
    headlines = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        if submission.stickied:
            continue  # Skip pinned posts if you want

        image_url = None

        # Case 1: Direct link to an image
        if submission.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            image_url = submission.url

        # Case 2: Gallery posts → just take the first image (ignore resolutions)
        elif hasattr(submission, "media_metadata") and submission.media_metadata:
            media_id, media_data = next(iter(submission.media_metadata.items()))
            if "s" in media_data:
                image_url = media_data["s"]["u"]   # Just use "s" (usually full-size)
            elif "p" in media_data and media_data["p"]:
                image_url = media_data["p"][0]["u"]  # Fallback: first preview size

        # Case 3: Preview images (non-gallery)
        elif hasattr(submission, "preview"):
            images = submission.preview.get("images")
            if images:
                image_url = images[0]["source"]["url"]

        # Case 4: Fallback thumbnail
        if not image_url and submission.thumbnail and submission.thumbnail.startswith("http"):
            image_url = submission.thumbnail

        headlines.append({
            "title": submission.title,
            "url": submission.url,
            "image": image_url
        })

    return headlines
