import os
import datetime
import torch
import whisper

# Path to a test file (avoid stray backslashes on Windows)
TEST_FILE = os.path.join("audio_output", "nosleep_2025-04-25_part1.mp3")

def transcriber(audio_file: str, model_size: str = "base.en"):
    """
    Transcribe the given audio file using OpenAI Whisper with word-level timestamps.
    Returns full transcription text plus segments with per-word timing.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(model_size).to(device)
    result = model.transcribe(audio_file, word_timestamps=True)
    return result["text"], result["segments"]

def generate_srt(
    segments,
    audio_file: str,
    output_folder: str = "subtitles_output",
    max_words: int = 2
):
    """
    Generate an .srt subtitle file from Whisper word-level segments.
    - Flush a subtitle when a word ends in .,!? or when max_words is reached.
    """
    os.makedirs(output_folder, exist_ok=True)
    base = os.path.splitext(os.path.basename(audio_file))[0]
    srt_path = os.path.join(output_folder, f"{base}.srt")

    def fmt(sec: float) -> str:
        total_ms = int(sec * 1000)
        ms = total_ms % 1000
        total_s = total_ms // 1000
        hh = total_s // 3600
        mm = (total_s % 3600) // 60
        ss = total_s % 60
        return f"{hh:02}:{mm:02}:{ss:02},{ms:03}"

    # flatten all words
    words = [w for seg in segments for w in seg.get("words", [])]

    subs = []
    chunk = []
    for w in words:
        chunk.append(w)
        word_text = w.get("word", "")
        if word_text.endswith(('.', ',', '!', '?')) or len(chunk) >= max_words:
            subs.append(chunk)
            chunk = []
    if chunk:
        subs.append(chunk)

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(subs, start=1):
            start_ts = fmt(chunk[0]["start"])
            end_ts   = fmt(chunk[-1]["end"])
            text     = " ".join(w.get("word", "").strip() for w in chunk)
            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{text}\n\n")

    print(f"Subtitles saved to {srt_path}")