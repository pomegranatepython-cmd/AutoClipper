import whisper
import json
import sys
from pathlib import Path

from config import WHISPER_MODEL, DEVICE, TRANSCRIPTS_DIR

def transcribe_video(video_path):
    video_path = Path(video_path)

    print("Loading Whisper model...")

    model = whisper.load_model(
        WHISPER_MODEL,
        device=DEVICE
    )

    print("Transcribing video...")

    result = model.transcribe(
    str(video_path),
    language="hi",
    fp16=False
)

    output = TRANSCRIPTS_DIR / f"{video_path.stem}.json"

    output.write_text(
        json.dumps(result["segments"], indent=2),
        encoding="utf-8"
    )

    print(f"Transcription complete!")
    print(f"Saved: {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py video.mp4")
    else:
        transcribe_video(sys.argv[1])