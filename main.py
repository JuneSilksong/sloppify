import os
import datetime
from dotenv import load_dotenv
from tts import tts_output
from utils.get_reddit_post import get_top_reddit_posts
from utils.text_preprocessor import preprocess_text, text_to_chunks
from utils.subtitles import transcriber, generate_srt

POST_LIMIT = 1
ELEVEN_LABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
AUDIO_OUTPUT_FOLDER = "audio output"

load_dotenv('eleven_labs.env')
load_dotenv('reddit.env')

if __name__ == "__main__":

    subreddit = input("subreddit: r/")

    posts = get_top_reddit_posts(subreddit, limit=POST_LIMIT)


    if not posts:
        print("No posts found in the subreddit or there was an issue.")
    else:
        print(f"Found {len(posts)} posts in subreddit '{subreddit}'")
        for i, (title, selftext) in enumerate(posts):
            print(f"Processing Post {i + 1}:")
            print(f"Title: {title}")
            print(f"Selftext: {selftext}\n")

            text_to_convert = f"{title}\n{selftext}"

            text_to_convert = preprocess_text(text_to_convert)
            text_chunks = text_to_chunks(text_to_convert)
                       
            current_time = datetime.datetime.now().strftime("%Y-%m-%d")
            if not os.path.exists(AUDIO_OUTPUT_FOLDER):
                os.makedirs(AUDIO_OUTPUT_FOLDER)

            for chunk_index, chunk in enumerate(text_chunks):
                output_filename = os.path.join(AUDIO_OUTPUT_FOLDER, f"{subreddit}_{current_time}_part{chunk_index + 1}.mp3")
                print(f"Audio will be saved as {output_filename}")
                tts_output(chunk, voice_id=ELEVEN_LABS_VOICE_ID, filename=output_filename)

                transcription, segments = transcriber(output_filename)
                print(f"Transcription: {transcription}")
                generate_srt(segments, output_file=f"{subreddit}_{current_time}_post{i + 1}_subtitles.srt")
    


