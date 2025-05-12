import os
import praw
import yt_dlp
import emoji
from dotenv import load_dotenv
from typing import List, Tuple
import re

def sanitize_filename(text: str) -> str:
    # Remove illegal characters and limit length
    return re.sub(r'[\\/*?:"<>|]', "", text).strip()   

def get_top_reddit_posts(
    subreddit: str,
    time_filter: str = "day",
    limit: int = 10
) -> Tuple[List[Tuple[str, str]], List[str]]:
    
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

    downloaded_files: List[str] = []

    titles: List[str] = []

    for p in posts:
        if not p.stickied:
            if p.is_self:
                top_reddit_posts.append((p.title, p.selftext))
                print(p.title)
            if p.is_video:
                title = p.title.replace('\r', '').replace('\n', '')
                title_noemoji = emoji.replace_emoji(title, replace='')

                # temp fix for emoji only titles
                if title_noemoji != "":
                    title = title_noemoji
                if title == "": # probably unnecessary but will check later
                    title = "."
                sanitized_title = sanitize_filename(title)
                    
                titles.append(sanitized_title)
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': f'input/content_video/{title}.%(ext)s',
                    'merge_output_format': 'mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    if not os.path.exists(f'output/{sanitized_title}.mp4'):
                        info = ydl.extract_info(p.url, download=True)
                        filename = ydl.prepare_filename(info)
                        downloaded_files.append(os.path.basename(filename))

    return top_reddit_posts, downloaded_files, titles