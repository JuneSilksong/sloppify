from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip
from typing import List, Tuple
import random
import pysrt
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

def stitch_video(
    video_file_name: str = None,
    music_file_name: str = None,
    tts_audio_file_name: str = None,
    tts_srt_file_name: str = None,
    title: str = None
):
    
    # Check if we have background video
    if not video_file_name:
        raise ValueError("video_file_name is required.")

    # Process video to 9:16
    video_file = f"input/webm/{video_file_name}"
    video = VideoFileClip(video_file)
    resized = video.resize(height=1440)
    cropped = resized.crop(x_center=resized.w/2, width=810)

    # Load music
    if music_file_name:
        music_file = f"input/mp3/{music_file_name}"
        music = AudioFileClip(music_file).volumex(0.05)
    else:
        music = None
    
    # Load TTS audio
    if tts_audio_file_name:
        tts_audio_file = f"input/tts/{tts_audio_file_name}"
        tts_audio = AudioFileClip(tts_audio_file).volumex(0.6) 
    else:
        tts_audio = None

    # Process audio
    if tts_audio and music:
        music = music.set_duration(tts_audio.duration)
        audio = CompositeAudioClip([music,tts_audio])
    elif tts_audio:
        audio = tts_audio
    elif music:
        audio = music
    else:
        audio = None
    
    # Set background video to start at random point and attach any audio
    duration = min(audio.duration if audio else cropped.duration, cropped.duration, 5)
    start_time = random.randint(1,int(video.duration-duration-10))
    cropped = cropped.subclip(start_time)
    if audio:
        cropped = cropped.set_audio(audio)

    # Add subtitles
    if tts_srt_file_name:
        tts_srt_file = f"input/srt/{tts_srt_file_name}"
        subs = pysrt.open(tts_srt_file)
        subtitles = []
        for sub in subs:
            txt = TextClip(sub.text, fontsize=72, color='yellow', stroke_color='black', stroke_width=5, font='Segoe-UI-Black')
            txt = txt.set_start(sub.start.ordinal / 1000).set_duration(sub.duration.seconds + sub.duration.milliseconds / 1000)
            txt = txt.set_position(('center', 0.6), relative=True)
            subtitles.append(txt)
        final = CompositeVideoClip(([cropped] + subtitles))
    else:
        final = cropped

    # Crop video to duration length and write
    final = final.subclip(0, duration)
    final.write_videofile(f"output/{title}.mp4", codec="libx264", audio_codec="aac", fps=60)