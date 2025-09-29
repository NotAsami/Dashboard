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
    Fetch top headlines from a specified subreddit.

    Args:
        subreddit (str): The name of the subreddit to fetch headlines from. Defaults to "worldnews".
        limit (int): The maximum number of headlines to fetch. Defaults to 5.

    Returns:
        list[dict]: A list of dictionaries, each containing:
            - title (str): The title of the Reddit post.
            - url (str): The URL of the Reddit post.
    """
    headlines = []  # Initialize an empty list to store the headlines
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        # Append a dictionary with the title and URL of each submission to the headlines list
        headlines.append({
            "title": submission.title,
            "url": submission.url
        })
    return headlines  # Return the list of headlines
