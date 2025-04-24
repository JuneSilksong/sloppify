import os
import praw
from dotenv import load_dotenv

def get_top_reddit_posts(subreddit,time_filter="day",limit=10):
    load_dotenv("reddit_api.env")
    client_id = os.getenv("reddit_client_id")
    client_secret = os.getenv("reddit_client_secret")
    user_agent = os.getenv("reddit_user_agent")
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    top_reddit_posts = []
    for submission in reddit.subreddit(subreddit).top(time_filter="day",limit=limit):
        post = []
        if submission.is_self and not submission.stickied:
            post.append(submission.title)
            post.append(submission.selftext)
            top_reddit_posts.append(post)
    
    print(top_reddit_posts)