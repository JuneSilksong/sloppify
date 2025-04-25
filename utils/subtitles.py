import whisper
import datetime
import torch

def transcriber(audio_file):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisper.load_model("large").to(device)
    

    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    

    result = model.transcribe(audio)
    

    return result['text'], result['segments']  # segments gives you start and end times for subtitles

def generate_srt(segments, output_file="output_subtitles.srt"):
   
    with open(output_file, 'w') as f:
        for idx, segment in enumerate(segments):

            start_time = str(datetime.timedelta(seconds=segment['start']))
            end_time = str(datetime.timedelta(seconds=segment['end']))
            
            f.write(f"{idx + 1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{segment['text']}\n\n")

    print(f"Subtitles saved to {output_file}")
