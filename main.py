import os
import datetime
from pydub import AudioSegment
from dotenv import load_dotenv
from utils.tts import tts_output
from utils.get_reddit_post import get_top_reddit_posts
from utils.text_preprocessor import preprocess_text, text_to_chunks
from utils.subtitles import transcriber, generate_srt
from utils.post_track import is_post_processed, mark_post_as_processed

POST_LIMIT = 1
ELEVEN_LABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
AUDIO_OUTPUT_FOLDER = "audio_output"
SUBTITLES_OUTPUT_FOLDER = "subtitles_output"

load_dotenv('eleven_labs.env')
load_dotenv('reddit_api.env')

if __name__ == "__main__":

    subreddit = input("subreddit: r/")
    posts = get_top_reddit_posts(subreddit, limit=POST_LIMIT)

    if not posts:
        print("No posts found in the subreddit or there was an issue.")
    else:
        print(f"Found {len(posts)} posts in subreddit '{subreddit}'")

        for i, (title, selftext) in enumerate(posts):
            print(f"\nProcessing Post {i + 1}:")
            print(f"Title: {title}")
            print(f"Selftext: {selftext}")

            post_id     = f"{subreddit}_{title[:10]}_{i+1}"
            current_time = datetime.datetime.now().strftime("%Y-%m-%d")
            final_audio  = os.path.join(AUDIO_OUTPUT_FOLDER, f"{subreddit}_{current_time}_post{i+1}.mp3")

            if is_post_processed(post_id) and os.path.exists(final_audio):
                print(f"Audio for post {post_id} already processed; skipping TTS.")
            else:
                if is_post_processed(post_id):
                    print(f"Post {post_id} was marked processed but {final_audio} is missing—regenerating.")
                else:
                    print(f"Generating TTS for post {post_id}…")

                text = f"Title: {title}\n{selftext}"
                text = preprocess_text(text)
                chunks = text_to_chunks(text)

                os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)
                part_files = []

                for idx, chunk in enumerate(chunks, start=1):
                    part_path = os.path.join(
                        AUDIO_OUTPUT_FOLDER,
                        f"{subreddit}_{current_time}_post{i+1}_part{idx}.mp3"
                    )
                    print(f" • generating {part_path}")
                    tts_output(chunk, voice_id=ELEVEN_LABS_VOICE_ID, filename=part_path)
                    part_files.append(part_path)

                combined = AudioSegment.empty()
                for pf in part_files:
                    combined += AudioSegment.from_file(pf)
                combined.export(final_audio, format="mp3")
                print(f"→ merged into {final_audio}")

                mark_post_as_processed(post_id)

            transcription, segments = transcriber(final_audio)
            print(f"Transcription: {transcription}")

            os.makedirs(SUBTITLES_OUTPUT_FOLDER, exist_ok=True)
            generate_srt(segments, final_audio, output_folder=SUBTITLES_OUTPUT_FOLDER)

        print("\nAll audio files and subtitles saved successfully.")
