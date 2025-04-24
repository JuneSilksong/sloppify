import os
import praw
from dotenv import load_dotenv

load_dotenv("api.env")

client_id = os.getenv("reddit_client_id")
client_secret = os.getenv("reddit_client_secret")
user_agent = os.getenv("reddit_user_agent")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

print(reddit.read_only)

for submission in reddit.subreddit("tifu").hot(limit=2):
    if submission.is_self and not submission.stickied:
        print(submission.title)
        print(submission.selftext)