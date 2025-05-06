import os
import datetime
from utils.get_reddit_post import get_top_reddit_posts
from utils.text_preprocessor import preprocess_text, text_to_chunks
from utils.tts import tts_output
from utils.subtitles import transcriber, generate_srt
from utils.post_track import is_post_processed, mark_post_as_processed
from utils.video_stitcher import stitch_video

AUDIO_OUTPUT_FOLDER = "audio_output"
SUBTITLE_OUTPUT_FOLDER = "subtitles_output"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"

BACKGROUND_VIDEO = "input/bg_video/youtube_minecraft_parkour_1440p-001.mp4"
VIDEO_OUTPUT_FOLDER = "video_output"

def process_post(subreddit: str, title: str, body: str, post_id: str):
    if is_post_processed(post_id):
        print(f"Post {post_id} already processed. Skipping...")
        return

    text = f"{title}\n{body}"
    preprocessed = preprocess_text(text)
    chunks = text_to_chunks(preprocessed)

    os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(SUBTITLE_OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    for i, chunk in enumerate(chunks):
        base_filename = f"{subreddit}_{date_str}_part{i+1}"
        audio_file = os.path.join(AUDIO_OUTPUT_FOLDER, f"{base_filename}.mp3")
        srt_file   = os.path.join(SUBTITLE_OUTPUT_FOLDER, f"{base_filename}.srt")
        final_video = os.path.join(VIDEO_OUTPUT_FOLDER, f"{base_filename}.mp4")

        tts_output(chunk, voice_id=VOICE_ID, filename=audio_file)
        transcript, segments = transcriber(audio_file)
        generate_srt(segments, audio_file=audio_file, output_folder=SUBTITLE_OUTPUT_FOLDER)

        stitch_video(
            audio_path=audio_file,
            subtitle_path=srt_file,
            output_path=final_video,
            background_video_path=BACKGROUND_VIDEO
        )

    mark_post_as_processed(post_id)