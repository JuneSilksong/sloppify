from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip
from typing import List, Tuple
import textwrap
import random
import pysrt
from moviepy.config import change_settings
import os

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

def stitch_video(
    video_file: str = None,
    music_file: str = None,
    tts_audio_file: str = None,
    tts_srt_file: str = None,
    content_video_file: str = None,
    content_image_file: str = None,
    title: str = None
):
    # General parameters
    height=1440
    width=810
    content_height=1120
    content_width=630

    # Check if we have background video
    if not video_file:
        raise ValueError("video_file_name is required.")
        
    if content_video_file and content_image_file:
        raise ValueError("content conflict between video and image")

    # Process video to 9:16
    video = VideoFileClip(f"input/bg_video/{video_file}")
    resized = video.resize(height=height)
    cropped = resized.crop(x_center=resized.w/2, width=width)

    # Load music
    if music_file:
        music = AudioFileClip(f"input/bg_audio/{music_file}")
    else:
        music = None
    
    # Load TTS audio
    if tts_audio_file:
        tts_audio = AudioFileClip(f"input/tts/{tts_audio_file}")
    else:
        tts_audio = None

    # Process audio
    if tts_audio and music:
        music = music.set_duration(tts_audio.duration)
        audio = CompositeAudioClip([music.volumex(0.05),tts_audio.volumex(0.6)])
    elif tts_audio:
        audio = tts_audio.volumex(0.6) 
    elif music:
        audio = music.volumex(0.5)
    else:
        audio = None

    # Process content video
    if content_video_file:
        content_video = VideoFileClip(f"input/content_video/{content_video_file}")
        if content_video.h/16 >= content_video.w/9:
            content_resized = content_video.resize(height=content_height)
        else:
            content_resized = content_video.resize(width=content_width)
    
    # Set background video to start at random point and attach any audio
    duration = max(content_video.duration if content_video_file else 0, tts_audio.duration if tts_audio else 0)
    if duration == 0:
        duration = 10
    start_time = random.randint(1,int(video.duration-duration-10))
    cropped = cropped.subclip(start_time)
    if audio:
        cropped = cropped.set_audio(audio)

    # Add subtitles
    if tts_srt_file:
        subs = pysrt.open(f"input/srt/{tts_srt_file}")
        subtitles = []
        for sub in subs:
            txt = TextClip(sub.text, fontsize=72, color='yellow', stroke_color='black', stroke_width=5, font='Segoe-UI-Black')
            txt = txt.set_start(sub.start.ordinal / 1000).set_duration(sub.duration.seconds + sub.duration.milliseconds / 1000)
            txt = txt.set_position(('center', 0.6), relative=True)
            subtitles.append(txt)
        final = CompositeVideoClip(([cropped] + subtitles))

    # Alternatively, add the content (no subtitles)
    elif content_resized:
        txt_to_wrap = os.path.splitext(content_video_file)[0]
        if len(txt_to_wrap) > 60:
            fontsize=40
            stroke_width=2
            wrap_width=30
        else:
            fontsize=54
            stroke_width=3
            wrap_width=20
        wrapped_txt = textwrap.fill(txt_to_wrap,width=wrap_width)
        print(wrapped_txt, wrapped_txt.count('\n'))
        txt_height = ((wrapped_txt.count('\n') + 1) * (fontsize*1.4))
        txt_pos = (height - txt_height - content_resized.h) / 2 / height
        content_pos = ((height - txt_height - content_resized.h) / 2 + txt_height + 20) / height
        txt = TextClip(wrapped_txt, fontsize=fontsize, color='yellow', stroke_color='black', stroke_width=stroke_width, font='Segoe-UI-Black', method='caption', size=(width, None))
        txt = txt.set_start(0).set_duration(cropped.duration)
        txt = txt.set_position(('center', txt_pos), relative=True)
        print(txt_height, content_resized.h, txt_pos, content_pos, height)
        final = CompositeVideoClip(([cropped] + [content_resized.set_position(('center', content_pos), relative=True)] + [txt]))
    
    # Crop video to duration length and write
    final = final.subclip(0, duration)
    final.write_videofile(f"output/{title if title else content_video_file if content_video_file else None}", codec="libx264", audio_codec="aac", fps=60)