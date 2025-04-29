import os
import praw
from dotenv import load_dotenv
from typing import List, Tuple

def get_top_reddit_posts(
    subreddit: str,
    time_filter: str = "day",
    limit: int = 10
) -> List[Tuple[str, str]]:
    
    """
    Fetches the top text-based reddit posts from a specific subreddit

    Args:
        subreddit (str): The name of the subreddit (e.g., 'tifu', 'aitah').
        time_filter (str): The time filter for top posts (e.g., 'hour', 'day', 'week', 'month', etc.).
        limit (int): The number of top posts to fetch.
    
    Returns:
        top_reddit_posts (List[Tuple[str, str]]): A list of tuples, each containing the title and selftext of a post.
    """
    
    load_dotenv("reddit_api.env")
    client_id = os.getenv("reddit_client_id")
    client_secret = os.getenv("reddit_client_secret")
    user_agent = os.getenv("reddit_user_agent")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    posts = reddit.subreddit(subreddit).top(time_filter=time_filter,limit=limit)
    
    top_reddit_posts: List[Tuple[str, str]] = []

    for p in posts:
        if p.is_self and not p.stickied:
            top_reddit_posts.append((p.title, p.selftext, p.url))
    
    return top_reddit_posts