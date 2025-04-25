from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip
from typing import List, Tuple

def stitch_video(video_file: str, music_file: str, tts_audio_file: str): #add tts_srt: str later
    
    video = VideoFileClip(video_file)
    resized = video.resize(height=1080)
    cropped = resized.crop(x_center=resized.w/2, width=607)

    tts = AudioFileClip(tts_audio_file).volumex(0.6)
    music = AudioFileClip(music_file).volumex(0.07)
    music = music.set_duration(tts.duration).audio_fadeout(1)

    audio = CompositeAudioClip([music,tts])

    final = cropped.set_audio(audio)
    duration = min(audio.duration, cropped.duration, 15)
    final = final.subclip(0, duration)

    final.write_videofile("output_9x16.mp4", codec="libx264", audio_codec="aac", fps=30)

video_file = "youtube_minecraft_parkour.mp4"
music_file = "youtube_joyful_chess.mp3"
tts_audio_file = "TIFU_TIFU by asking what a guy who hates me said about me in a group chat_part1.mp3"

stitch_video(video_file,music_file,tts_audio_file)