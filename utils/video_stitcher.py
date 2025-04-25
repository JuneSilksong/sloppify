from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip
from typing import List, Tuple
import random
# import pysrt

def stitch_video(video_file_name: str, music_file_name: str, tts_audio_file_name: str, title: str ="TIFU xyz"): #add tts_srt: str later

    video_file = f"input/webm/{video_file_name}"
    music_file = f"input/mp3/{music_file_name}"
    tts_audio_file = f"input/tts/{tts_audio_file_name}"
    # tts_srt_file = f"input/srt/{tts_srt_file_name}"
    
    # Initialise, resize, and crop video to fit 9:16 aspect ratio
    video = VideoFileClip(video_file)
    resized = video.resize(height=1440)
    cropped = resized.crop(x_center=resized.w/2, width=810)

    # Initialise and combine tts audio and music
    tts_audio = AudioFileClip(tts_audio_file).volumex(0.6)
    music = AudioFileClip(music_file).volumex(0.05)
    music = music.set_duration(tts_audio.duration).audio_fadeout(1)
    audio = CompositeAudioClip([music,tts_audio])

    duration = min(audio.duration, cropped.duration, 15)

    start_time = random.randint(1,int(video.duration-duration-10))
    cropped = cropped.subclip(start_time)
    final = cropped.set_audio(audio)   # remove this line once srt is ready
    """
    subs = pysrt.open(tts_srt)
    subtitles = []

    for sub in subs:
    txt = TextClip(sub.text, fontsize=48, color'white', stroke_color='black', stroke_width=2, font='Arial-Bold')
    txt = txt.set_start(sub.start.ordinal / 1000).set_duration(sub.duration.seconds + sub.duration.milliseconds / 1000)
    txt = txt.set_position(('center', 'bottom'))
    subtitles.append(txt)

    final = CompositeVideoClip(cropped.set_audio(audio) + subtitles)

    """

    final = final.subclip(0, duration)

    final.write_videofile(f"output/{title}.mp4", codec="libx264", audio_codec="aac", fps=60)

"""
video_file = "youtube_minecraft_parkour_1440p.webm"
music_file = "youtube_joyful_chess.mp3"
tts_audio_file = "TIFU_TIFU by asking what a guy who hates me said about me in a group chat_part1.mp3"

stitch_video(video_file,music_file,tts_audio_file)
"""