import os
import datetime
import re

from utils.get_reddit_post import get_top_reddit_posts
from utils.text_preprocessor import preprocess_text, text_to_chunks
from utils.tts import tts_output
from utils.subtitles import transcriber, generate_srt
from utils.post_track import is_post_processed, mark_post_as_processed
from utils.video_stitcher import stitch_video

# Import all constants from config.py
from config import (
    VOICE_ID,
    AUDIO_OUTPUT_FOLDER,
    SUBTITLE_OUTPUT_FOLDER,
    BACKGROUND_VIDEO,
    BACKGROUND_MUSIC,
)

def sanitize_filename(text: str) -> str:
    # Remove illegal characters and limit length
    return re.sub(r'[\\/*?:"<>|]', "", text).strip()

def process_post(subreddit: str, title: str, body: str, post_id: str):
    if is_post_processed(post_id):
        print(f"Post {post_id} already processed. Skipping...")
        return

    print(f"→ Processing post: {post_id}")
    text = f"{title}\n{body}"
    preprocessed = preprocess_text(text)
    chunks = text_to_chunks(preprocessed)

    os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(SUBTITLE_OUTPUT_FOLDER, exist_ok=True)

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    final_audio_file = f"{subreddit}_{date_str}_{post_id}.mp3"
    final_audio_path = os.path.join(AUDIO_OUTPUT_FOLDER, final_audio_file)
    final_srt_file = f"{subreddit}_{date_str}_{post_id}.srt"
    final_srt_path = os.path.join(SUBTITLE_OUTPUT_FOLDER, final_srt_file)

    # Merge all TTS chunks into one audio file
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(AUDIO_OUTPUT_FOLDER, f"{subreddit}_{date_str}_part{i+1}.mp3")
        print(f"→ Generating TTS: {chunk_path}")
        tts_output(chunk, voice_id=VOICE_ID, filename=chunk_path)
        chunk_paths.append(chunk_path)

    # Concatenate audio parts
    print(f"→ Merging audio into: {final_audio_path}")
    
    # ffmpeg command to concatenate audio files, sys = terminal
    os.system(f"ffmpeg -y -i \"concat:{'|'.join(chunk_paths)}\" -acodec copy \"{final_audio_path}\"") 

    # Transcribe merged audio and generate subtitles
    print(f"→ Transcribing and generating subtitles for: {final_audio_path}")
    transcript, segments = transcriber(final_audio_path)
    print(f"Transcript:\n{transcript}\n")
    generate_srt(
        segments,
        audio_file=final_audio_path,
        output_folder=SUBTITLE_OUTPUT_FOLDER,
        max_words=2
    )

    # Stitch final video
    safe_title = sanitize_filename(title)
    print("→ Stitching final video...")
    stitch_video(
        video_file=BACKGROUND_VIDEO,
        music_file=BACKGROUND_MUSIC,
        tts_audio_file=final_audio_file,
        tts_srt_file=final_srt_file,
        title=safe_title,
    )

    mark_post_as_processed(post_id)
