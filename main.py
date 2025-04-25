import os
import datetime
from dotenv import load_dotenv
from GetRedditPost import get_top_reddit_posts
from tts import tts_output

POST_LIMIT = 1
ELEVEN_LABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"

load_dotenv('eleven_labs.env')
load_dotenv('reddit.env')

if __name__ == "__main__":

    subreddit = input("subreddit: ")

    posts = get_top_reddit_posts(subreddit, limit=POST_LIMIT)


    if not posts:
        print("No posts found in the subreddit or there was an issue.")
    else:
        print(f"Found {len(posts)} posts in subreddit '{subreddit}'")
        for i, (title, selftext) in enumerate(posts):
            print(f"Post {i + 1}:")
            print(f"Title: {title}")
            print(f"Selftext: {selftext}\n")

        text_to_convert = "\n\n".join([f"Title: {title}\n{selftext}" for title, selftext in posts])

        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        output_filename = f"output_{subreddit}_{current_time}.mp3"
        tts_output(text_to_convert, voice_id=ELEVEN_LABS_VOICE_ID, filename=output_filename)
        
        print(f"Audio saved as {output_filename}")


