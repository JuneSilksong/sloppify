import os
from dotenv import load_dotenv
from utils.get_reddit_post import get_top_reddit_posts, sanitize_filename
from pipeline import process_post
from config import (POST_LIMIT, 
                    TIME_FRAME
)

load_dotenv("eleven_labs.env")
load_dotenv("reddit.env")

if __name__ == "__main__":
    subreddit = input("Subreddit: r/")
    posts,_,_ = get_top_reddit_posts(subreddit, limit=POST_LIMIT, time_filter=TIME_FRAME)

    if not posts:
        print("No posts found or error.")
    else:
        for i, (title, body) in enumerate(posts):
            safe_title = sanitize_filename(title)
            post_id = f"{subreddit}_{safe_title[:10]}_{i+1}"
            print(f"\nProcessing Post {i+1} — {post_id}:")
            process_post(subreddit, safe_title, body, post_id)