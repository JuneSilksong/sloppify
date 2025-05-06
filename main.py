import os
from dotenv import load_dotenv
from utils.get_reddit_post import get_top_reddit_posts
from pipeline import process_post

load_dotenv("eleven_labs.env")
load_dotenv("reddit.env")

if __name__ == "__main__":
    subreddit = input("Subreddit: r/")
    posts = get_top_reddit_posts(subreddit, limit=1)

    if not posts:
        print("No posts found or error.")
    else:
        for i, (title, body, post_id) in enumerate(posts):
            print(f"\nProcessing Post {i+1} — {post_id}:")
            process_post(subreddit, title, body, post_id)