from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip
from moviepy.config import change_settings
import textwrap
import random
import pysrt
import os
import praw
import yt_dlp
from dotenv import load_dotenv
from typing import List, Tuple

from utils.get_reddit_post import get_top_reddit_posts
from utils.video_stitcher import stitch_video

# content_file_path = 'input/content_video/downloaded_files.txt'

def generate_video(subreddit: str="funnyanimals", limit: int=1, time_filter: str="day"):
    top_reddit_posts, downloaded_files = get_top_reddit_posts(subreddit=subreddit,limit=limit,time_filter=time_filter)

    if subreddit == "funnyanimals":
        video_file = "nature_drone.mkv"
        music_file = "ambient_music.mp3"
    else:
        video_file = "youtube_minecraft_parkour_1440p.webm"
        music_file = "youtube_joyful_chess.mp3"

    for content_video_file in downloaded_files:
        stitch_video(video_file=video_file,music_file=music_file,content_video_file=content_video_file)

generate_video(subreddit="funnyanimals", limit=10, time_filter="year")