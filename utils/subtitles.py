# test_subtitles.py
import os
import datetime
import torch
import whisper

TEST_FILE = r"audio_output\nosleep_2025-04-25_part1.mp3"

def transcriber(audio_file: str, model_size: str = "small"):
    """
    Transcribe the given audio file using OpenAI Whisper.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_size).to(device)

    result = model.transcribe(audio_file)
    return result["text"], result["segments"]

def generate_srt(segments, audio_file: str, output_folder: str = "subtitles_output"):
    """
    Generate an .srt subtitle file from Whisper segments.
    """
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    srt_path = os.path.join(output_folder, f"{base_name}.srt")

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments, start=1):
            start_ts = datetime.timedelta(seconds=segment["start"])
            end_ts   = datetime.timedelta(seconds=segment["end"])
            text     = segment["text"].strip()

            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{text}\n\n")

    print(f"Subtitles saved to {srt_path}")